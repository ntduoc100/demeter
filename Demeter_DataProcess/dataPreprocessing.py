import pandas as pd
import os
import re
import numpy as np
from datetime import datetime, timedelta
from argparse import ArgumentParser

class WeatherDataPreprocessing:
    '''
    Description:
    This class is used to preprocess data that we collect from mv.freemeteo.com
    and store them in a folder, in different format.
    '''
    def __init__(self):
        self._cities = None
        self._syncing = None
        self._df = None

    def generateStackedDF(self, cities: list, syncing: list):
        '''
        Parameters:
        - cities: list of cities
        - gids: list of id of cities on the maps, in cities's order
        - syncing: list of place in openweathermap that the same with cities in freemeteo

        Description:
        From the data we have already collected, stack them into a dataframe `self._df`.
        '''
        self._cities = cities.copy()
        self._syncing = syncing.copy()
        self._df = pd.DataFrame()

        for i, city in enumerate(cities):
            folderScanning = os.listdir(f"./data/{city}")
            for file in folderScanning:
                df = pd.read_json(f"./data/{city}/{file}")
                # getDate: for example, "ho-chi-minh-city-2022-12-03.json"
                # will return 2022-12-03
                getDate = re.search(r"(\d{4}.*?)(?=[.])",file)
                df['Date'] = [getDate.group()] * len(df)
                df['Place']= [self._syncing[i]]*len(df)
                self._df = self._df.append(df)
    
    def cleanData(self):
        '''
        Description:
        Clean the data using pandas function and Regular Expression
        '''
        self._df['Time'] = [datetime.strptime(s, '%Y-%m-%d %H:%M') for s in self._df['Date'] + " " + self._df['Time']]
        self._df['Time'] = [s.strftime('%Y-%m-%dT%H:%M:%S') for s in self._df['Time']]

        self._df['Wind'] = self._df['Wind'].replace("Calm", "0 Km/h").str.extract(r'(\d+?)(?= \D)')
        self._df['Temperature'] = self._df['Temperature'].str.extract(r'(\d+)')
        self._df['Rel. humidity'] = self._df['Rel. humidity'].str.extract(r'(\d+)')
        self._df['Pressure'] = self._df['Pressure'].str.extract(r'([^a-zA-Z]+)')
        self._df.index= np.arange(len(self._df))
        self._df = self._df.drop(columns = ['Date', 'Relative Temperature', 'Dew Point'])
        self._df = self._df.rename(columns= {"Rel. humidity": "Humidity"})
    
    def generateCleannedData(self, folder: str):
        '''
        Parameters:
        - folder: the name of output folder

        Description:
        From the data we have already preprocessed, store them into `folder`, in date order.
        '''
        if folder not in os.listdir("./"):
            os.makedirs(f"./{folder}")

        self._df.to_json(f'./{folder}/preprocessed-data.json')
        
if __name__ == "__main__":
    cities = [
            "ho-chi-minh-city", "hanoi", "haiphong", "hue", "nha-trang", "can-tho", "rach-gia", \
            "quy-nhon", "vung-tau", "nam-dinh", "bac-giang", "bac-lieu",  "buon-ma-thuot", \
            "ca-mau", "cam-pha-mines",  "cao-bang",  "da-lat", "dien-bien-phu", \
            "dong-ha", "dong-hoi", "dong-xoai", "ha-giang", "ha-long", "hai-duong", "hoa-binh", \
            "hoi-an", "kon-tum", "lao-cai", "long-xuyen", "my-tho", "phan-rang-thap-cham", \
            "phan-thiet", "phu-khuong", "pleiku", "quang-ngai", "soc-trang", "son-la", \
            "thai-nguyen", "thanh-hoa", "tra-vinh", "tuy-hoa", "tuyen-quang",  "viet-tri", \
            "vinh-long",  "ye-yen-sun-ho-tao", "yen-bai",  "yen-vinh"
        ]

    syncing = [
            "Ho Chi Minh city", "Hanoi", "Hai Phong", "Thua Thien Hue", "Khanh Hoa", "Can Tho", "Kien Giang", \
            "Binh Dinh", "Ba Ria - Vung Tau", "Nam Dinh", "Bac Giang", "Bac Lieu",  "Dak Lak", \
            "Ca Mau", "Quang Ninh",  "Cao Bang",  "Lam Dong", "Dien Bien", \
            "Quang Tri", "Quang Binh", "Binh Phuoc", "Ha Giang", "Quang Ninh", "Hai Duong", "Hoa Binh", \
            "Quang Nam", "Kon Tum", "Lao Cai", "An Giang", "Tien Giang", "Ninh Thuan", "Binh Thuan",\
            "Ben Tre", "Gia Lai", "Quang Ngai", "Soc Trang", "Son La",  "Thai Nguyen", \
            "Thanh Hoa", "Tra Vinh", "Phu Yen", "Tuyen Quang",  "Phu Tho", "Vinh Long",  \
            "Lai Chau", "Yen Bai",  "Vinh Phuc"
        ]
    parser = ArgumentParser(description= \
        "Preprocessing Viet Nam data already collected, take 1 argument, save to a folder")
    parser.add_argument('fdpath', type = str,\
         help = "Folder name to store preprocessed data")

    args = parser.parse_args()
    folder = args.fdpath

    dataPreprocessObject = WeatherDataPreprocessing()
    dataPreprocessObject.generateStackedDF(cities = cities, syncing = syncing)
    dataPreprocessObject.cleanData()
    dataPreprocessObject.generateCleannedData(folder)
