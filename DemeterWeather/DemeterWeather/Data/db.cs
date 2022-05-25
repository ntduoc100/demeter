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
        MongoDbContext database = new MongoDbContext();

        public List<LocationList> GetListLocation(string prefix)
        {
            List<LocationList> list = new List<LocationList>();
            var collection = database.Region;
            foreach (var item in collection.Find(s => s.Place.Contains(prefix)).ToList())
            {
                list.Add(new LocationList
                {
                    Label = item.Place.ToString(),
                    Val = item.PlaceId.ToString(),
                });
            }
            return list;
        }

        public string CalculateLocation(string lat, string lon)
        {
            var collection = database.Region;
            var distance = 100000.0;
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

        public ForecastList getForecastByLocation(string city)
        {
            ForecastList forecast = new ForecastList();
            var collection = database.Realtime;
            foreach (var item in collection.Find(s => s.Place == city).ToList())
            {
                forecast.Id = item.Id.ToString();
                forecast.Temperature = item.Temperature.ToString();
                forecast.Time = item.Time.ToString();
                forecast.Wind = item.Wind.ToString();
                forecast.Humidity = item.Humidity.ToString();
                forecast.Pressure = item.Pressure.ToString();
                forecast.Place = item.Place.ToString();
            }
            return forecast;
        }

        public ForecastList GetWeatherForecast(string lat, string lon)
        {
            var city = CalculateLocation(lat, lon);
            ForecastList forecast = getForecastByLocation(city);
            return forecast;
        }

        public List<PredictList> GetPredictForecast(string lat, string lon)
        {
            List<PredictList> predict = new List<PredictList>();
            var city = CalculateLocation(lat, lon);
            var collection = database.Predict;
            var today = DateTime.Now;
            for (var i = 1; i <= 5; i++)
            {
                var predictDate = today.AddDays(i);
                var sumTemp = 0.0;
                var countTime = 0.0;
                var minTemp = 100.0;
                var maxTemp = 0.0;
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
