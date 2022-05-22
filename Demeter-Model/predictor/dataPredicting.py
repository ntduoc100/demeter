import pymongo
import pandas as pd
from datetime import datetime, timedelta
from argparse import ArgumentParser
from statsmodels.tsa.statespace.sarimax import SARIMAX
import numpy as np
import time


class WeatherPrediction:
    '''
    Description:
    - This class get data from mongoDB server, train them and then give
    prediction for the future.
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
    
    def getData(self, dataCollection: str, coefCollection: str):
        '''
        Parameters:
        - dataCollection: Name of historical collection
        - coefficientCollection: name of coefficient for the model collection
        Description:
        - Get data and coefficient for training model
        '''
        historicalDataCollection = self._db.get_collection(dataCollection)
        coefficientCollection= self._db.get_collection(coefCollection)
        # Get the historical data and transform them
        self._df = pd.DataFrame(list(historicalDataCollection.find({}, {'_id': False})))
        self._df['Time'] = pd.to_datetime(self._df['Time'], format = '%Y-%m-%dT%H:%M:%S')
        self._df = self._df.set_index('Time')
        # Get the coefficient for model
        self._coef_df =  pd.DataFrame(list(coefficientCollection.find({}, {'_id': False})))

    def predictAndSave(self, places: list, predictCollection: str):
        '''
        Parameters:
        - places: List of place be predicted
        - predictCollection: Collection on Database used to predict
        Description:
        - Use SARIMAX to predict and save them to mongoDB
        '''
        predictlDataCollection = self._db.get_collection(f'{predictCollection}')
        for place in places:
            print(place)
            # Get place's data and transform them
            place_df = self._df[self._df['Place'] == place]
            place_df = place_df.sort_index()
            trainingData = place_df['2020':].resample('3h').mean()
            # Fill missing data with the nearest datetime
            trainingData = trainingData.fillna(method = 'ffill')
            # Get the place's coefficient
            place_coef = self._coef_df[self._coef_df['Place'] == place]
            result_predict = []
            # Predicting for each attributes
            for attribute in ['Temperature', 'Wind', 'Humidity', 'Pressure']:
                model = SARIMAX(trainingData[attribute], \
                            order = tuple(place_coef[place_coef['Attribute'] == attribute]['order'].values[0]), \
                            seasonal_order = tuple(place_coef[place_coef['Attribute'] == attribute]['seasonal_order'].values[0]))
                results = model.fit()
                # Forecast for the next 7 days
                forecast = results.forecast(56)
                result_predict.append(forecast)

            predictList = []
            for i in range(len(result_predict[0])):
                jsonformat = dict()
                jsonformat['Time'] = result_predict[0].index[i].strftime('%Y-%m-%dT%H:%M:%S')
                jsonformat['Temperature'] = round(result_predict[0][i],1)
                jsonformat['Wind'] = round(result_predict[1][i],1)
                jsonformat['Humidity'] = round(result_predict[2][i],1)
                jsonformat['Pressure'] = round(result_predict[3][i],1)
                jsonformat['Place'] = place
                predictList.append(jsonformat)
            predictlDataCollection.insert_many(predictList)

    def RemoveOldRecords(self, dataCollection: str):
        '''
        Description:
        - Remove old predicted records 
        '''
        collection = self._db.get_collection(dataCollection)
        now = (datetime.utcnow() + timedelta(hours=7)).strftime("%Y-%m-%dT%H:%M:%S")
        collection.delete_many({'Time':{'$lt': now}})


if __name__ == '__main__':
    parser = ArgumentParser(description= "Uploading parameter for prediction model")
    parser.add_argument('dbname', type = str, help = "Database name that store data")
    parser.add_argument('collectionName', type = str, help = "Collection name that store data")
    parser.add_argument('coeffiCollection', type = str, help = "Collection name that store coefficient data")
    parser.add_argument('predictCollection', type = str, help = "Collection name to store predicted data")

    args = parser.parse_args()
    dbname  = args.dbname
    collectionName = args.collectionName
    coefficientName = args.coeffiCollection
    predictName = args.predictCollection

    places = [
            "Ho Chi Minh city", 
            "Hanoi", "Hai Phong", "Thua Thien Hue", "Khanh Hoa", "Can Tho", "Kien Giang", \
            "Binh Dinh", "Ba Ria - Vung Tau", "Nam Dinh", "Bac Giang", "Bac Lieu",  "Dak Lak", \
            "Ca Mau", "Quang Ninh",  "Cao Bang",  "Lam Dong", "Dien Bien", \
            "Quang Tri", "Quang Binh", "Binh Phuoc", "Ha Giang", "Quang Ninh", "Hai Duong", "Hoa Binh", \
            "Quang Nam", "Kon Tum", "Lao Cai", "An Giang", "Tien Giang", "Ninh Thuan", "Binh Thuan",\
            "Ben Tre", "Gia Lai", "Quang Ngai", "Soc Trang", "Son La",  "Thai Nguyen", \
            "Thanh Hoa", "Tra Vinh", "Phu Yen", "Tuyen Quang",  "Phu Tho", "Vinh Long",  \
            "Lai Chau", "Yen Bai",  "Vinh Phuc"
        ]

    weatherObject = WeatherPrediction()
    connection_string = f'mongodb+srv://root:12345ADMIN@cluster0.5qjhz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

    weatherObject.connect(connection_string, dbname)

    while True:
        now = datetime.now()
        if now.hour in np.arange(0, 22, 3) and now.minute == 0:
            break

    while True:
        weatherObject.getData(collectionName,coefficientName)
        weatherObject.predictAndSave(places, predictName)
        weatherObject.RemoveOldRecords(collectionName)
        time.sleep(3600)

    # weatherObject.getData(collectionName,coefficientName)
    # weatherObject.predictAndSave(places, predictName)