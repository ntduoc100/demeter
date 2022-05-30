using System.Data;
using System.Data.SqlClient;
using DemeterWeather.Models;
using System.Configuration;
using System.Collections.Generic;
using DemeterWeather.Data;
using MongoDB.Driver;
using System;

namespace DemeterProject.Data

{
    public class Db
    {
        // create a mongodb context object
        MongoDbContext database = new MongoDbContext();

        // function to query the list of location which has the prefix string
        // Input: string predixt - user input in the searching form
        // Output: the list of location that has prefix
        public List<ResultList> GetListLocation(string prefix)
        {
            List<ResultList> list = new List<ResultList>();
            var collection = database.Region;
            foreach (var item in collection.Find(s => s.Place.Contains(prefix)).ToList())
            {
                list.Add(new ResultList
                {
                    Label = item.Place.ToString(),
                    Val = item.PlaceId.ToString(),
                });
            }
            return list;
        }

        // function to check whether the location exist or not
        // Input:  string locationName - name of city
        // Output:  true - if the location exists
        //          false - if the location does not exist
        public bool CheckExistLocation(string locationName)
        {
            List<ResultList> list = new List<ResultList>();
            var collection = database.Region;
            var item = collection.Find(s => s.Place == locationName).FirstOrDefault();
            if (item != null)
                return true;
            return false;
        }

        // function to get the place ip for mapping with map chart
        // Input: string city - location name
        // Output: ChartPlaceId
        public string GetLocationMapID(string city)
        {
            var regionCollection = database.Region;
            var item = regionCollection.Find(s => s.Place == city).FirstOrDefault();
            return item.ChartPlaceId;
        }

        // function to get the data of the temperature map
        // Input: none
        // Output: List LocationList of chart information
        public List<ResultList> TemperatureMap()
        {
            var regionCollection = database.Region;
            var realtimeCollection = database.Realtime;
            List<ResultList> chartInformation = new List<ResultList>();
            // use linq aggregate and look up function to join region collection with realtime colelction
            // Corresponding SQL:region join realtime where region.place = realtime.place
            foreach (var item in regionCollection.Aggregate().Lookup("realtime_data", "Place", "Place", "result").ToList())
            {
                chartInformation.Add(new ResultList
                {
                    Label = item["place_id"].ToString(),
                    Val = item["result"][0]["Temperature"].ToString(),
                });
            }
            return chartInformation;
        }

        // function to get the data of the wind map
        // Input: none
        // Output: List LocationList of chart information
        public List<ResultList> WindMap()
        {
            var regionCollection = database.Region;
            var realtimeCollection = database.Realtime;
            List<ResultList> chartInformation = new List<ResultList>();
            // use linq aggregate and look up function to join region collection with realtime colelction
            // Corresponding SQL:region join realtime where region.place = realtime.place
            foreach (var item in regionCollection.Aggregate().Lookup("realtime_data", "Place", "Place", "result").ToList())
            {
                chartInformation.Add(new ResultList
                {
                    Label = item["place_id"].ToString(),
                    Val = item["result"][0]["Wind"].ToString(),
                });
            }
            return chartInformation;
        }

        // function to get the data of the humidity map
        // Input: none
        // Output: List LocationList of chart information
        public List<ResultList> HumidityMap()
        {
            var regionCollection = database.Region;
            var realtimeCollection = database.Realtime;
            List<ResultList> chartInformation = new List<ResultList>();
            // use linq aggregate and look up function to join region collection with realtime colelction
            // Corresponding SQL:region join realtime where region.place = realtime.place
            foreach (var item in regionCollection.Aggregate().Lookup("realtime_data", "Place", "Place", "result").ToList())
            {
                chartInformation.Add(new ResultList
                {
                    Label = item["place_id"].ToString(),
                    Val = item["result"][0]["Humidity"].ToString(),
                });
            }
            return chartInformation;
        }

        // function to get the data of the pressure map
        // Input: none
        // Output: List LocationList of chart information
        public List<ResultList> PressureMap()
        {
            var regionCollection = database.Region;
            var realtimeCollection = database.Realtime;
            List<ResultList> chartInformation = new List<ResultList>();
            // use linq aggregate and look up function to join region collection with realtime colelction
            // Corresponding SQL:region join realtime where region.place = realtime.place
            foreach (var item in regionCollection.Aggregate().Lookup("realtime_data", "Place", "Place", "result").ToList())
            {
                chartInformation.Add(new ResultList
                {
                    Label = item["place_id"].ToString(),
                    Val = item["result"][0]["Pressure"].ToString(),
                });
            }
            return chartInformation;
        }
        
        // function to set the switch case for the input filter for the map chart at homepage
        // Input: string filter
        // Output: redirect to the corresponding filter function
        public List<ResultList> GetMapChartInformation(string filter)
        {
            switch (filter)
            {
                case "Temperature":
                    return TemperatureMap();
                case "Wind":
                    return WindMap();
                case "Humidity":
                    return HumidityMap();
                case "Pressure":
                    return PressureMap();
            }
            return null;
        }

        // function to get all predict information at the location for the line chart
        // Input: string chartPlaceId - place id for mapping with map chart
        // Output: List of ForecastList for that location
        public List<ForecastList> GetLineChartInformation(string chartplaceId)
        {
            List<ForecastList> lines = new List<ForecastList>();
            var regionCollection = database.Region;
            var predictCollection = database.Predict;
            // get the location name of the chartPlacId by finding in the region collection
            var city = regionCollection.Find(s => s.ChartPlaceId == chartplaceId).FirstOrDefault();
            // get all predict forecast at predict collection
            foreach (var item in predictCollection.Find(s => s.Place == city.Place).ToList())
            {
                lines.Add(new ForecastList
                {
                    Temperature = item.Temperature.ToString(),
                    Wind = item.Wind.ToString(),
                    Humidity = item.Humidity.ToString(),
                    Pressure = item.Pressure.ToString(),
                    Time = item.Time.ToString(),
                    Place = city.Place
                });
            }
            return lines;
        }

        // function to calculate the distance between gps coordinate and all locations in database
        // Input: coordinate - lat, lon
        // Output: the name of location which is nearest the gps coordinate
        public string CalculateLocation(string lat, string lon)
        {
            var collection = database.Region;
            var distance = double.MaxValue;
            var name = string.Empty;
            foreach (var item in collection.Find(s => s.Place != " ").ToList())
            {
                var x = Math.Abs(item.Coordinate[1] - double.Parse(lat));
                var y = Math.Abs(item.Coordinate[0] - double.Parse(lon));
                var res = Math.Sqrt(Math.Pow(x, 2) + Math.Pow(y, 2));
                if (distance > res)
                {
                    distance = res;
                    name = item.Place.ToString();
                }
            }
            return name;
        }

        // function to the the weather forecast based on location string
        // Input: string city - location name
        // Output: ForecaseList item for that location
        public ForecastList getForecastByLocation(string city)
        {
            ForecastList forecast = new ForecastList();
            var collection = database.Realtime;
            var item = collection.Find(s => s.Place == city).FirstOrDefault();
            forecast.Id = item.Id.ToString();
            forecast.Temperature = item.Temperature.ToString();
            forecast.Time = item.Time.ToString();
            forecast.Wind = item.Wind.ToString();
            forecast.Humidity = item.Humidity.ToString();
            forecast.Pressure = item.Pressure.ToString();
            forecast.Place = item.Place.ToString();
            return forecast;
        }

        // function to get the weather forecast based on coordinate 
        // Input: coordinate - lat, lon
        // Output: Forecast item for that coordinate
        public ForecastList GetWeatherForecast(string lat, string lon)
        {
            var city = CalculateLocation(lat, lon);
            ForecastList forecast = getForecastByLocation(city);
            return forecast;
        }
        
        // function to get the predict forecast of the next 5 days
        // Input: coordinate - lat, lon
        // Output: Array of 5 Predict List Objects
        public List<PredictList> GetPredictForecast(string lat, string lon)
        {
            List<PredictList> predict = new List<PredictList>();
            var city = CalculateLocation(lat, lon); // get the location name
            var collection = database.Predict;
            var today = DateTime.Now; // get date in realtime
            for (var i = 1; i <= 5; i++)
            {
                var predictDate = today.AddDays(i);
                var sumTemp = 0.0;
                var countTime = 0.0;
                var minTemp = 100.0;
                var maxTemp = 0.0;
                // calculate the min temperature, max temperature and range of temperature at this location
                foreach (var item in collection.Find(s => s.Place == city & s.Time.Contains(predictDate.ToString("yyyy-MM-dd"))).ToList())
                {
                    sumTemp += item.Temperature;
                    countTime += 1;
                    if (minTemp > item.Temperature)
                    {
                        minTemp = item.Temperature;
                    }
                    else if (maxTemp < item.Temperature)
                    {
                        maxTemp = item.Temperature;
                    }
                }
                // add new object
                predict.Add(new PredictList
                {
                    Date = predictDate.ToString("yyyy-MM-dd"),
                    MeanTemperature = (sumTemp / countTime).ToString(),
                    LowerBoundTemperature = minTemp.ToString(),
                    UpperBoundTemperature = maxTemp.ToString()
                });
            }
            return predict;
        }

        // function to get the timely predict forecast - 3 hours for 1 predict
        // Input: string city - location name
        // Output: List ForecaseList of that location
        public List<ForecastList> GetTimelyPredictForecast(string city)
        {
            List<ForecastList> predict = new List<ForecastList>();
            var collection = database.Predict;
            foreach(var item in collection.Find(s => s.Place == city).ToList())
            {
                predict.Add(new ForecastList
                {
                    Id = item.Id.ToString(),
                    Temperature = item.Temperature.ToString(),
                    Time = item.Time.ToString(),
                    Wind = item.Wind.ToString(),
                    Humidity = item.Humidity.ToString(),
                    Pressure = item.Pressure.ToString(),
                    Place = item.Place.ToString(),
                });
            }
            return predict;
        }
     }
}
