import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime, timedelta, date
import os
from argparse import ArgumentParser

class WeatherDataCollecting:
    '''
    Description:
    This class is used to collect data from mv.freemeteo.com
    and store them in a folder called "data"
    '''
    def __init__(self):
        self._cities = None
        self._gids = None
        self._stations = None
        self._period = []
    
    def generateTimePeriod(self, sdate: str, edate: str):
        '''
        Parameters:
        - sdate: start date, format "YYYY-MM-DD"
        - edate: end date, format "YYYY-MM-DD"

        Description:
        Generate a time series between sdate and edate
        '''
        sdate = datetime.strptime(sdate, "%Y-%m-%d")
        edate = datetime.strptime(edate, "%Y-%m-%d")
        delta = edate - sdate       # as timedelta
        
        for i in range(delta.days + 1):
            day = sdate + timedelta(days=i)
            self._period.append(day.strftime("%Y-%m-%d"))


    def collectData(self, cities: list, gids: list, stations: list, folder: str):
        '''
        Parameters:
        - cities: list of cities
        - gids: list of id of cities on the maps, in cities's order
        - stations: list of station that get information of cities on the maps, in cities's order

        Description:
        Collect the weather data from mv.freemeteo.com and save as json format
        '''
        self._cities = cities.copy()
        self._gids = gids.copy()
        self._stations = stations.copy()

        os.makedirs(f"./{folder}/")
        for i, city in enumerate(self._cities):
            print(f"Get {city} data ...")
            if city not in os.listdir(f"./{folder}/"):
                os.makedirs(f"./{folder}/{city}")
            for date in self._period:
                if f"{city}-{date}.json" in os.listdir(f"./{folder}/{city}/"):
                    df = pd.read_json(f"./{folder}/{city}/{city}-{date}.json")
                    # If 49 lines from 0:00 to 23:30 already existed, pass the for loops
                    if (len(df)>=48): 
                        continue
                
                URL = f"https://mv.freemeteo.com/weather/{city}/history/daily-history/?gid={self._gids[i]}&station={self._stations[i]}&date={date}&language=english&country=vietnam"

                rq = requests.get(URL)
                while (rq.ok == False):
                    time.sleep(1)
                    rq = requests.get(URL)

                soup = BeautifulSoup(rq.text, 'lxml')
                table = soup.find('table', attrs={'class':'daily-history'})

                table_header = table.find('thead')
                table_body = table.find('tbody')

                attr_list = [str(attr.text.replace('\n','').replace('\xa0','')) for attr in table_header.findAll('th')]

                new_table = pd.DataFrame(columns=attr_list)

                for row in table_body.find_all('tr'):
                    row_vals = [row_val.text.strip() for row_val in row.find_all('td')]
                    
                    new_row = pd.Series(row_vals, index = new_table.columns)
                    new_table = new_table.append(new_row, ignore_index=True)
                
                new_table = new_table.drop(columns=['Wind Gust', 'Icon', 'DescriptionDetails'])
                
                new_table.to_json(f"./{folder}/{city}/{city}-{date}.json")



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


    gids = [
            1566083, 1581130, 1581298, 1580240, 1572151, 1586203, 1568510, 1568574, 1562414,\
            1573517, 1591527, 1591474, 1586896, 1586443, 1586357, 1586185,\
            1584071, 1583477, 1582926, 1582886, 1582436, 1581349, 1580410, 1581326,\
            1580830, 1580541, 1578500, 1576303, 1575627, 1574023, 1571067, 1571058, 1570549,\
            1569684, 1568770, 1567788, 1567681, 1566319, 1566166, 1563926, 1563281,\
            1563287, 1562820, 1562693, 1560011, 1560349, 1560037
        ]

    stations = [ 
            11437, 11376, 11376, 11394, 11437, 11437, 11437, 11397, 11437, 11376, 11376, 11437, \
            11437, 11437, 11376, 11376, 11437, 11376, 11394, 11394, 11437, \
            11376, 11376, 11376, 11376, 11397, 11397, 11376, 11437, 11437, 11437, 11437, 11437, \
            11397, 11397, 11437, 11376, 11376, 11376, 11437, 11397, 11376, 11376, \
            11437, 11376, 11376, 11376
        ]
    
    parser = ArgumentParser(description= "Collect Viet Nam data from freemeteo, take 2 arguments, save to a folder")
    parser.add_argument('fdpath', type = str, help = "Folder name to store data")
    parser.add_argument('-s', '--sdate', type = str , help = "The start date, with format YYYY-MM-DD")
    parser.add_argument('-e', '--edate', type = str, help = "The end date, with format YYYY-MM-DD")
    args = parser.parse_args()
    folder = args.fdpath
    sdate = args.sdate
    edate = args.edate

    dataCollectObject = WeatherDataCollecting()
    dataCollectObject.generateTimePeriod(sdate, edate)
    dataCollectObject.collectData(cities, gids, stations, folder)
