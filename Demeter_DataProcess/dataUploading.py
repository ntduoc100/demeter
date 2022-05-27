import pymongo 
import requests
import sys
import time
import pandas as pd
from argparse import ArgumentParser

class WeatherDataUploading:
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
    
    def uploadHistoricalData(self, folderName: str, collectionName: str):
        '''
        Parameters:
        - foldername: name of folder that contains historical data

        Description:
        This function is used for uploading historical weather data, each data line
        contains weather data each 30 minutes interval
        '''
        historicalDataCollection = self._db.get_collection(f'{collectionName}')
        historicalData = pd.read_json(f"./{folderName}/preprocessed-data.json")
        historicalList = []
        for line in historicalData.values:
            jsonformat = dict()
            jsonformat['Time'] = line[0]
            jsonformat['Temperature'] = line[1]
            jsonformat['Wind'] = line[2]
            jsonformat['Humidity'] = line[3]
            jsonformat['Pressure'] = line[4]
            jsonformat['Place'] = line[5]
            historicalList.append(jsonformat)
        historicalDataCollection.insert_many(historicalList)

if __name__ == '__main__':
    parser = ArgumentParser(description= "Uploading Viet Nam data already preprocessed to mongoDB, take 1 argument")
    parser.add_argument('fdpath', type = str, help = "Folder name to store preprocessed data")
    parser.add_argument('colName', type = str, help = "Collection name to store data")

    args = parser.parse_args()
    folder = args.fdpath
    collectionName = args.colName

    connection_str = f'mongodb+srv://root:12345ADMIN@cluster0.5qjhz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    weatherdataobject = WeatherDataUploading()
    weatherdataobject.connect(connection_str, 'demeter')
    weatherdataobject.uploadHistoricalData(folder, collectionName)
