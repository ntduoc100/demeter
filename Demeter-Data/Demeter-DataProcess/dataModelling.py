import pymongo
import pandas as pd
from datetime import datetime
import pmdarima as pm
import numpy as np
from argparse import ArgumentParser


class WeatherDataModelling:
    '''
    Description:
    - For the SAMRIMAX model, try to find $(p,q,r)$
    and seasonal_order for this model. Then, store
    them to mongoDb for the next phase
    '''
    def __init__(self):
        self._db = None
        self._modelCoefficient = []

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
  
    def getData(self, historicalCollectionName: str):
        '''
        Parameters:
        - historicalCollectionName: Name of the collection that 
        store historical data
        Description:
        - Get data from the chosen collection, change some properties 
        to match the model and return the list of place in this collection
        '''
        historicalData = self._db.get_collection(f'{historicalCollectionName}')
        self._df = pd.DataFrame(list(historicalData.find()))
        self._df = self._df.drop(columns = '_id')
        self._df['Time'] = pd.to_datetime(self._df['Time'], format = '%Y-%m-%dT%H:%M:%S')
        places = self._df['Place'].unique()
        
        return places

    def trainAcrossRegion(self, place: str):
        '''
        Parameters:
        - place: Name of place was chosen to train
        - coefficientCollection: The collection in MongoDB to store coefficient
        Description:
        - Apply "Auto_arima" to find coefficient that some models (ARIMA, SARIMA, SARIMAX) use
        '''
        # Get `place` data and set index for it
        city_df = self._df[self._df['Place'] == place]
        city_df = city_df.set_index('Time')
        city_df = city_df.sort_index()

        # Training data for each 3-hour-period
        trainingData = city_df[:].resample('3h').mean()
        # Fill missing data with the nearest datetime
        trainingData = trainingData.fillna(method = 'ffill')
        
        # Traverse through 4 attributes: Temperature, Humidity, Wind, Pressure
        for column in trainingData.columns:
            print(column)
            result= dict()
            model = pm.auto_arima(trainingData[column], #data
                                d=1, # non-seasonal difference order
                                start_p=0, # initial guess for p
                                start_q=0, # initial guess for q
                                max_p=2, # max value of p to test
                                max_q=2, # max value of q to test
                                seasonal=True, # is the time series seasonal? YES
                                m = 8, # the seasonal period
                                #D=1, # seasonal difference order
                                start_P=1, # initial guess for P
                                start_Q=1, # initial guess for Q
                                max_P=1, # max value of P to test
                                max_Q=1, # max value of Q to test
                                information_criterion='aic', # used to select best model
                                trace=True, # print results whilst training
                                error_action='ignore', # ignore orders that don't work
                                stepwise=True, # apply intelligent order search
                                )
            result['Place'] = place
            result['Attribute'] = column
            result['order'] = model.order
            result['seasonal_order'] = model.seasonal_order
            self._modelCoefficient.append(result)
  

    def updateToDatabase(self, coefficientCollection: str):
        '''
        Parameters:
        - coefficientCollection: The collection in MongoDB to store coefficient
        Description:
        - Save data to coefficientCollection on Database
        '''
        self._db.drop_collection(f'{coefficientCollection}')
        coefficientModelCollection = self._db.get_collection(f'{coefficientCollection}')
        coefficientModelCollection.insert_many(self._modelCoefficient)

if __name__ == '__main__':
    parser = ArgumentParser(description= "Uploading parameter for prediction model")
    parser.add_argument('dbname', type = str, help = "Database name that store data")
    parser.add_argument('historicalCollectionName', type = str, help = "Collection name that store historical data")
    parser.add_argument('coefficollection', type = str, help = "Collection name to store coefficient data")

    args = parser.parse_args()
    dbname  = args.dbname
    historicalCollectionName = args.historicalCollectionName
    coefficientCollection = args.coefficollection

    connection_string = f'mongodb+srv://root:12345ADMIN@cluster0.5qjhz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    predictObject = WeatherDataModelling()
    predictObject.connect(connection_string, dbname)
    places = predictObject.getData(historicalCollectionName)
    for place in places:
        predictObject.trainAcrossRegion(place)
    predictObject.updateToDatabase(coefficientCollection)