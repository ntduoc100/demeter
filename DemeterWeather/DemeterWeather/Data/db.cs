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

        public List<LocationList> LocationGet(string prefix)
        {
            List<LocationList> list = new List<LocationList>();
            var collection = database.Region;
            foreach (var item in collection.Find(s => s.Place.Contains(prefix)).ToList())
            {
                list.Add(new LocationList
                {
                    label = item.Place.ToString(),
                    val = item.PlaceId.ToString(),
                });;
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

        public ForecastList GetWeatherForecast(string lat, string lon)
        {
            ForecastList forecast = new ForecastList();
            var city = CalculateLocation(lat, lon);
            var collection = database.Realtime;
            foreach (var item in collection.Find(s => s.Place == city).ToList())
            {
                forecast.Id = item.Id.ToString();
                forecast.Temperature = item.Temperature.ToString();
                forecast.Time = item.Time.ToString();
                forecast.Wind = item.Wind.ToString();
                forecast.Humidity= item.Humidity.ToString();
                forecast.Pressure= item.Pressure.ToString();
                forecast.Wind = item.Wind.ToString();
                forecast.Place = item.Place.ToString();
            }
            return forecast;
        }
    }
}
