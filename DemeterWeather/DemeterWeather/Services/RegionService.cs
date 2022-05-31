using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using DemeterWeather.Models;
using FuzzySharp;
using MongoDB.Driver;

namespace DemeterWeather.Services
{
    public class RegionService
    {
        private const int CachedIntervalMinutes = 30;
        private readonly IMongoCollection<Region> _regionCol;
        private DateTime _cachedAt = DateTime.MinValue;
        private List<Region> _cachedRegions;

        public RegionService(IDemeterDatabaseSettings demeterDatabaseSettings)
        {
            var client = new MongoClient(
                demeterDatabaseSettings.ConnectionString);

            var database = client.GetDatabase(
                demeterDatabaseSettings.DatabaseName);

            _regionCol = database.GetCollection<Region>(
                demeterDatabaseSettings.RegionCollectionName);
            GetCachedRegions();
        }

        private List<Region> GetCachedRegions()
        {
            var period = DateTime.UtcNow - _cachedAt;
            if (period.TotalMinutes < CachedIntervalMinutes)
                return _cachedRegions;

            _cachedRegions = _regionCol
                .Find(_ => true)
                .ToList();
            _cachedAt = DateTime.UtcNow;
            return _cachedRegions;
        }

        public List<Region> GetAll()
        {
            return GetCachedRegions();
        }

        public List<Region> DoSimpleSearch(string text)
        {
            if (string.IsNullOrEmpty(text))
                return new List<Region>();

            return _regionCol
                .Find(region => region.RegionName.ToLower().Contains(text))
                .ToList();
        }

        public List<Region> DoFullTextSearch(string text)
        {
            if (string.IsNullOrEmpty(text))
                return new List<Region>();

            return _regionCol
                .Find(Builders<Region>.Filter.Text(text))
                .ToList();
        }

        public static string PreprocessRegionName(string input)
        {
            input = Regex.Replace(input, "[^ a-zA-Z0-9]", " ");
            input = Regex.Replace(input, @"\s+", " ");
            input = input.ToLower();
            return input.Trim();
        }

        public List<Region> DoFuzzySearch(string text)
        {
            if (string.IsNullOrEmpty(text))
                return new List<Region>();

            var results = Process.ExtractTop(
                new Region { RegionName = text },
                _cachedRegions,
                processor: region => PreprocessRegionName(region.RegionName),
                limit: 10);
            return results
                .Where(r => r.Score > 60)
                .Select(r => r.Value)
                .ToList();
        }

        public Region FindByName(string name)
        {
            if (string.IsNullOrEmpty(name))
                return null;

            var region = GetCachedRegions().
                Find(s => s.RegionName == name);
            return region;
        }


        public Region FindByAnyChartRegionId(string anyChartId)
        {
            if (string.IsNullOrEmpty(anyChartId))
                return null;

            var region = GetCachedRegions()
                .Find(region => region.AnyChartRegionId == anyChartId);
            return region;
        }
    }
}