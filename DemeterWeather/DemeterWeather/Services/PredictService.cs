using System;
using System.Collections.Generic;
using DemeterWeather.Models;
using MongoDB.Driver;

namespace DemeterWeather.Services
{
    public class PredictService
    {
        private readonly IMongoCollection<WeatherData> _predictCol;

        public PredictService(IDemeterDatabaseSettings demeterDatabaseSettings)
        {
            var client = new MongoClient(
                demeterDatabaseSettings.ConnectionString);

            var database = client.GetDatabase(
                demeterDatabaseSettings.DatabaseName);

            _predictCol = database.GetCollection<WeatherData>(
                demeterDatabaseSettings.PredictCollectionName);
        }

        public List<WeatherData> GetLineChartData(string regionName)
        {
            if (string.IsNullOrEmpty(regionName))
                return new List<WeatherData>();

            var query = _predictCol
                .Find(e => e.RegionName == regionName)
                .SortBy(e => e.Time);
            return query.ToList();
        }

        public List<WeatherData> FindByRegionNameOnDay(string regionName, DateTime date)
        {
            if (string.IsNullOrEmpty(regionName))
                return new List<WeatherData>();

            var query = _predictCol
                .Find(e => e.RegionName == regionName &&
                           e.Time.Contains(date.ToString("yyyy-MM-dd")));
            return query.ToList();
        }

        public List<WeatherData> FindByRegion(string regionName, int limit)
        {
            if (string.IsNullOrEmpty(regionName))
                return new List<WeatherData>();

            var query = _predictCol
                .Find(e => e.RegionName == regionName)
                .SortBy(e => e.Time)
                .Limit(limit);
            return query.ToList();
        }
    }
}
