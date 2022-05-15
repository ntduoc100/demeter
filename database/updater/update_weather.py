import pymongo
import requests
import time
from datetime import datetime, timedelta
import threading as th
import signal

MAX_ATTEMPTS = 10
SLEEP_TIME_FOR_REQUEST = 0.05


class RealtimeWeather:
    '''
    Description:
    - This class is used to retrieve data from openweathermap 
    and store them in mongodb database
    '''

    def __init__(self):
        self._db = None
    
    def connect(self, connection_string: str, dbname: str):
        '''
        Parameters:
        - connection_string: MongoDB connection string
        - dbname: name of the database

        Description:
        - Establish connection to MongoDB server
        '''
        client = pymongo.MongoClient(connection_string)
        self._db = client.get_database(dbname)
        self._api_key = '4ce6dbd5661bd1a387f31884de79b6c2'

    def _transform_api(self, jsondata: dict, region_name: str, modified_time: str):

        return {
            'Time': modified_time,
            'Temperature': round(jsondata['main']['temp'] - 272.15, 0),
            'Wind': jsondata['wind']['speed'],
            'Humidity': jsondata['main']['humidity'],
            'Pressure': jsondata['main']['pressure'],
            'Place': region_name
        }

    def update_current_weather(self):
        '''
        Description:
        - Based on data from region_data collection
        collect data from openweather api and update the data
        in realtime_weather collection
        '''
        if self._db == None:
            raise Exception('No connection to database')

        # Set cursors
        region_data_collection = self._db.get_collection('region_data')
        realtime_data_collection = self._db.get_collection('realtime_data')

        regions_data = region_data_collection.find(
            {}, {'_id': False, 'id': True, 'region': True})

        # Get current time
        now = (datetime.now() + timedelta(hours=7)).strftime("%Y-%m-%dT%H:%M:%S")

        for region in regions_data:
            api_url = f'https://api.openweathermap.org/data/2.5/weather?id={region["id"]}&appid={self._api_key}'

            for _ in range(MAX_ATTEMPTS):
                time.sleep(SLEEP_TIME_FOR_REQUEST)
                response = requests.get(api_url)
                if response.ok == True:
                    break

            # Transform data
            jsondata = response.json()
            jsondata = self._transform_api(
                jsondata,
                region['region'],
                now
            )

            # Update
            realtime_data_collection.find_one_and_update(
                {'Place': region['region']},
                {'$set': jsondata},
                upsert=True,
            )

    def insert_weather_30_min(self):
        '''
        Description:
        This function is used for inserting weather data on the 30 minutes interval
        This works similar to update_current_weather
        '''
        # Set cursors
        region_data_collection = self._db.get_collection('region_data')
        historical_data_collection = self._db.get_collection('historical_data')

        regions_data = region_data_collection.find(
            {}, {'_id': False, 'id': True, 'region': True})

        # Get current time
        now = (datetime.now() + timedelta(hours=7)).strftime("%Y-%m-%dT%H:%M:%S")

        #############
        for region in regions_data:
            api_url = f'https://api.openweathermap.org/data/2.5/weather?id={region["id"]}&appid={self._api_key}'

            for _ in range(MAX_ATTEMPTS):
                time.sleep(SLEEP_TIME_FOR_REQUEST)
                response = requests.get(api_url)
                if response.ok == True:
                    break

            # Transform data
            jsondata = response.json()
            jsondata = self._transform_api(
                jsondata,
                region['region'],
                now
            )

            # Insert data
            historical_data_collection.insert_one(jsondata)


class Job(th.Thread):
    '''
    Description:
    - Create thread job that run forever
    '''
    def __init__(self, worker, runner, interval=0.5):
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
    
    def run(self):
        print('Thread #%s started' % self.ident)
 
        while not self.shutdown_flag.is_set():
            # Job code
            self.runner(self.worker, self.interval)
            
    
        print('Thread #%s stopped' % self.ident)

class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass

def service_shutdown(signum, frame):
    '''Raise exception to stop the program when a terminate signal received'''
    raise ServiceExit
        
def interval_runner(worker, interval):
    '''Only start at minute 0 or 30'''
    cur_min, cur_sec = datetime.now().strftime(r'%M-%S').split('-')
    if (cur_min == '00' or cur_min == '30') and int(cur_sec) <= 10:
        worker()

def realtime_runner(worker, interval):
    '''Collect data, keep the interval accuracy'''
    cur_sec = datetime.now().strftime(r'%S')
    start = time.time()
    worker()
    end = time.time()
    run_time = round(end - start, 0)
    time.sleep(interval - run_time)

            
if __name__ == '__main__':

    connection_str = 'mongodb+srv://root:12345ADMIN@cluster0.5qjhz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    # connection_str = 'mongodb://demeterdb:27017'
    # connection_str = 'mongodb://localhost:27017'

    realtime_object = RealtimeWeather()
    realtime_object.connect(connection_str, 'demeter')


    # This part is used to stop threads when a terminate signal send to the program

    # Register signals
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)

    try:
        realtime = Job(realtime_object.update_current_weather, realtime_runner, 60)
        interval_30 = Job(realtime_object.insert_weather_30_min, interval_runner)

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