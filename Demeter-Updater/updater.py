import pymongo
import requests
import time
from datetime import datetime, timedelta
import threading as th
import signal
from abc import abstractmethod

MAX_ATTEMPTS = 10
SLEEP_TIME_FOR_REQUEST = 0.5


class Updater:
    '''
    Description:
    - This class is used to retrieve data from openweathermap 
    and store them in mongodb database
    '''

    def __init__(self, connection_string: str, dbname: str):
        '''
        Parameters:
        - connection_string: MongoDB connection string
        - dbname: name of the database

        Description:
        - Establish connection to MongoDB server
        '''
        self._db = None
        client = pymongo.MongoClient(connection_string)
        self._db = client.get_database(dbname)
        self._api_key = '4ce6dbd5661bd1a387f31884de79b6c2'

    def _transform_api(self, jsondata: dict, region_name: str, modified_time: str):
        '''
        This function will convert raw json data to a formatted one 
        '''
        return {
            'Time': modified_time,
            'Temperature': round(jsondata['main']['temp'] - 272.15, 0),
            'Wind': jsondata['wind']['speed'],
            'Humidity': jsondata['main']['humidity'],
            'Pressure': jsondata['main']['pressure'],
            'Place': region_name
        }

    @abstractmethod
    def _query_func(self, collection, **kwargs):
        pass

    def update(self, collname: str):
        '''
        Parameters:
        - collname: collection name

        Description:
        - Based on data from region_data collection
        collect data from openweather api and update the data
        in the provided collectionl name

        Returns:
        - bool: update status
        '''

        # Check for region_data existence
        if 'region_data' not in self._db.list_collection_names():
            raise Exception('region_data did not exists')

        # Set cursors
        region_data_collection = self._db.get_collection('region_data')

        # Filter data
        regions_data = region_data_collection.find(
            {}, {'_id': False, 'id': True, 'Place': True})

        # Get current time
        now = (datetime.now() + timedelta(hours=7)).replace(second=0).strftime("%Y-%m-%dT%H:%M:%S")

        data = []
        for region in regions_data:
            api_url = f'https://api.openweathermap.org/data/2.5/weather?id={region["id"]}&appid={self._api_key}'
            
            nb_attempts = 0
            jsondata = None
            
            while nb_attempts < MAX_ATTEMPTS:
                nb_attempts += 1
                time.sleep(SLEEP_TIME_FOR_REQUEST)

                response = requests.get(api_url)
                if response.ok == True:
                    try:
                        jsondata = response.json()
                        # Transform data
                        jsondata = self._transform_api(
                        jsondata,
                        region['Place'],
                        now)
                        # Store data
                        data.append(jsondata)
                        break
                    except: 
                        continue
            
            # Stop and wait for next api call
            if nb_attempts == MAX_ATTEMPTS:
                return False

        # Nothing was crawled
        if len(data) == 0:
            return False

        # Update data
        self._query_func(collname=collname,
                         data=data, region=region)

        return True


class UpdaterRealtime(Updater):
    '''
    Description:
    - This clas is used to update weather data every 1 minute
    '''

    def __init__(self, connection_string: str, dbname: str):
        super().__init__(connection_string, dbname)

    def _query_func(self, collname, **kwargs):
        '''
        Description:
        - Drop collection, create and re-create indices
        '''
        self._db.drop_collection(collname)
        collection = self._db.get_collection(collname)
        collection.insert_many(kwargs['data'])
        collection.create_index('Place')


class UpdaterInterval(Updater):
    '''
    Description:
    - This clas is used to update weather data every 30 minutes
    '''
    def __init__(self, connection_string: str, dbname: str):
        super().__init__(connection_string, dbname)

    def _query_func(self, collname, **kwargs):
        collection = self._db.get_collection(collname)
        return collection.insert_many(kwargs['data'])


class Job(th.Thread):
    '''
    Description:
    - Create thread job that run forever
    '''

    def __init__(self, name, worker, runner, interval=0.5, **kwargs):
        '''
        Parameters:
        - worker: function where the code should be run in the thread
        - interval: amount of time between executions
        - runner: function that wrap the worker with additional code
        '''
        th.Thread.__init__(self)

        self.shutdown_flag = th.Event()
        self.worker = worker
        self.interval = interval
        self.runner = runner
        self.kwargs = kwargs
        self.name = name

    def run(self):
        while not self.shutdown_flag.is_set():
            # Job code
            self.runner(self.worker, self.interval, **self.kwargs)


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def service_shutdown(signum, frame):
    '''Raise exception to stop the program when a terminate signal received'''
    raise ServiceExit


def interval_runner(worker, interval, **kwargs):
    '''Only start at minute 0 or 30'''
    cur_min, cur_sec = datetime.now().strftime(r'%M-%S').split('-')
    if (cur_min == '00' or cur_min == '30') and int(cur_sec) <= 0.5:
        worker(kwargs['collname'])


def realtime_runner(worker, interval, **kwargs):
    '''Collect data, keep the interval accuracy'''
    worker(kwargs['collname'])
    time.sleep(interval)


if __name__ == '__main__':

    connection_str = 'mongodb+srv://root:12345ADMIN@cluster0.5qjhz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    # connection_str = 'mongodb://demeterdb:27017'
    # connection_str = 'mongodb://localhost:27017'

    # This below part is used to created threads for parallel
    # realtime and interval processes

    realtime_object = UpdaterRealtime(connection_str, 'demeter')
    interval_object = UpdaterInterval(connection_str, 'demeter')

    # Register signals
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    try:
        realtime = Job(
            'realtime',
            realtime_object.update,
            realtime_runner,
            300, # Change this to change the time between api calls for real time
            collname='realtime_data'
        )

        interval_30 = Job(
            'interval',
            interval_object.update,
            interval_runner,
            0,
            collname='historical_data'
        )

        realtime.start()
        interval_30.start()

        # Keep the program alive
        while True:
            time.sleep(0.5)

    except ServiceExit:
        realtime.shutdown_flag.set()
        interval_30.shutdown_flag.set()

        # Wait for the threads to close...
        realtime.join()
        interval_30.join()