import pymongo 
import requests
import sys
import time

MAX_ATTEMPTS = 10
SLEEP_TIME_FOR_REQUEST = 0.05

class RealtimeWeather:
    '''
    Description:
    This class is used to retrieve data from openweathermap 
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
        Establish connection to MongoDB server
        '''
        client = pymongo.MongoClient(connection_string)
        self._db = client.get_database(dbname)
        self._api_key = '4ce6dbd5661bd1a387f31884de79b6c2'
        
    def update_current_weather(self):
        '''
        Description:
        Based on data from region_data collection
        collect data from openweather api and update the data
        in realtime_weather collection
        '''
        if self._db == None:
            raise Exception('No connection to database')
        
        region_data_collection = self._db.get_collection('region_data')
        regions_data = region_data_collection.find({}, {'_id': False, 'id': True, 'region': True})

        realtime_data_collection = self._db.get_collection('realtime_weather')

        for region in regions_data:

            api_url = f'https://api.openweathermap.org/data/2.5/weather?id={region["id"]}&appid={self._api_key}'

            for _ in range(MAX_ATTEMPTS):
                response = requests.get(api_url)
                time.sleep(SLEEP_TIME_FOR_REQUEST)
                if response.ok == True:
                    break
            
            # Fix name
            jsondata = response.json()
            jsondata['name'] = region['region']

            # Update
            realtime_data_collection.find_one_and_update({'id': region['id']}, {'$set': jsondata}, upsert=True)

if __name__=='__main__':
    args = sys.argv[1:]
    if len(args) != 1:
        sys.exit()
    
    connection_str = f'mongodb+srv://root:{args[0]}@cluster0.5qjhz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    # connection_str = 'mongodb://demeterdb:27017'
    connection_str = 'mongodb://localhost:27017'
    realtime_object = RealtimeWeather()
    realtime_object.connect(connection_str, 'demeter')
    realtime_object.update_current_weather()