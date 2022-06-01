using System.Collections.Generic;
using DemeterWeather.Controllers;
using DemeterWeather.Models;
using Microsoft.Extensions.Options;
using MongoDB.Driver;

namespace DemeterWeather.Services
{
    public class RealtimeService
    {
        private readonly IDemeterDatabaseSettings _settings;
        private readonly IMongoCollection<WeatherData> _realtimeCol;

        public RealtimeService(IDemeterDatabaseSettings demeterDatabaseSettings)
        {
            _settings = demeterDatabaseSettings;
            var client = new MongoClient(
                demeterDatabaseSettings.ConnectionString);

            var database = client.GetDatabase(
                demeterDatabaseSettings.DatabaseName);

            _realtimeCol = database.GetCollection<WeatherData>(
                demeterDatabaseSettings.RealtimeCollectionName);
        }

        public List<MapChartEntity> GetMapChartData(MapChartFilter filter)
        {
            var result = new List<MapChartEntity>();
            
            var field_Region_RegionName = "Place";
            var field_Realtime_RegionName= "Place";
            var field_LookupResult = "lookup_result";
            var field_Region_AnyChartRegionId = "place_id";
            var filterString = filter.ToString();

            var query = _realtimeCol.Aggregate().Lookup(
                _settings.RegionCollectionName,
                field_Realtime_RegionName,
                field_Region_RegionName,
                field_LookupResult);

            foreach (var entity in query.ToList())
            {
                result.Add(new MapChartEntity
                {
                    AnyChartRegionId = entity[field_LookupResult][0][field_Region_AnyChartRegionId].ToString(),
                    Data = entity[filterString].ToString(),
                });
            }

            return result;
        }

        public WeatherData FindByRegionName(string regionName)
        {
            if (string.IsNullOrEmpty(regionName))
                return null;

            var query = _realtimeCol
                .Find(e => e.RegionName == regionName);
            return query.FirstOrDefault();
        }
    }
}