using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using DemeterWeather.Models;
using DemeterWeather.Services;
using Microsoft.AspNetCore.Mvc;

namespace DemeterWeather.Controllers
{
    public class RegionEntity
    {
        public string RegionName { get; set; }
        public int RegionId { get; set; }
    }

    public class PredictDataEntity
    {
        public string Date { get; set; }
        public string MeanTemperature { get; set; }
        public string LowerBoundTemperature { get; set; }
        public string UpperBoundTemperature { get; set; }
    }

    [ApiController]
    [Route("api/[controller]/[action]")]
    public class RegionController : ControllerBase
    {
        private readonly PredictService _predictService;
        private readonly RealtimeService _realtimeService;
        private readonly RegionService _regionService;

        public RegionController(
            RegionService regionService,
            RealtimeService realtimeService,
            PredictService predictService)
        {
            _regionService = regionService;
            _predictService = predictService;
            _realtimeService = realtimeService;
        }

        [HttpPost]
        public ActionResult<List<RegionEntity>> Search([FromForm] string text)
        {
            var result = new List<RegionEntity>();

            if (string.IsNullOrEmpty(text))
                return result;

            text = RegionService.PreprocessRegionName(text);

            if (string.IsNullOrEmpty(text))
                return result;

            var regions = _regionService.DoFuzzySearch(text);
            foreach (var region in regions)
                result.Add(new RegionEntity
                {
                    RegionName = region.RegionName,
                    RegionId = region.RegionId
                });

            return result;
        }

        [HttpPost]
        public ActionResult<string> GetAnyChartRegionId([FromForm] string regionName)
        {
            if (string.IsNullOrEmpty(regionName))
                return string.Empty;

            var region = _regionService.FindByName(regionName);
            if (region == null)
                return string.Empty;
            return region.AnyChartRegionId;
        }

        [HttpPost]
        public ActionResult<WeatherData> GetRealtimeWeatherData([FromForm] string lat, [FromForm] string lon)
        {
            if (!double.TryParse(lat, out var latValue))
                return null;
            if (!double.TryParse(lon, out var lonValue))
                return null;

            var regionName = FindNearestRegion(latValue, lonValue);
            if (string.IsNullOrEmpty(regionName))
                return null;

            return _realtimeService.FindByRegionName(regionName);
        }

        [HttpPost]
        public ActionResult<List<PredictDataEntity>> GetPredictWeatherData([FromForm] string lat, [FromForm] string lon)
        {
            var result = new List<PredictDataEntity>();

            if (!double.TryParse(lat, out var latValue))
                return null;
            if (!double.TryParse(lon, out var lonValue))
                return null;

            var regionName = FindNearestRegion(latValue, lonValue);
            if (string.IsNullOrEmpty(regionName))
                return null;

            var today = DateTime.UtcNow.Date;
            for (var i = 1; i <= 5; i++)
            {
                var date = today.AddDays(i);
                var dataList = _predictService.FindByRegionNameOnDay(regionName, date);
                if (dataList.Count == 0)
                    continue;

                var meanTemp = dataList.Average(weatherData => weatherData.Temperature);
                var maxTemp = dataList.Max(weatherData => weatherData.Temperature);
                var minTemp = dataList.Min(weatherData => weatherData.Temperature);

                result.Add(new PredictDataEntity
                {
                    Date = date.ToString("yyyy-MM-dd"),
                    MeanTemperature = meanTemp.ToString(CultureInfo.InvariantCulture),
                    UpperBoundTemperature = maxTemp.ToString(CultureInfo.InvariantCulture),
                    LowerBoundTemperature = minTemp.ToString(CultureInfo.InvariantCulture),
                });
            }

            return result;
        }

        private string FindNearestRegion(double lat, double lon)
        {
            var minDistance = double.MaxValue;
            var regionName = string.Empty;

            var regions = _regionService.GetAll();
            foreach (var item in regions)
            {
                var x = Math.Abs(item.Coordinate[1] - lat);
                var y = Math.Abs(item.Coordinate[0] - lon);
                var distance = Math.Sqrt(Math.Pow(x, 2) + Math.Pow(y, 2));

                if (minDistance > distance)
                {
                    minDistance = distance;
                    regionName = item.RegionName;
                }
            }

            return regionName;
        }
    }
}