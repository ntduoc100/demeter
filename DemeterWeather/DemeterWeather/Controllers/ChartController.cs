using System;
using System.Collections.Generic;
using DemeterWeather.Models;
using DemeterWeather.Services;
using Microsoft.AspNetCore.Mvc;

namespace DemeterWeather.Controllers
{
    public enum MapChartFilter
    {
        Temperature,
        Wind,
        Humidity,
        Pressure
    }

    public class MapChartEntity
    {
        public string AnyChartRegionId { get; set; }
        public string Data { get; set; }
    }

    [Route("api/[controller]/[action]")]
    [ApiController]
    public class ChartController : ControllerBase
    {
        private readonly PredictService _predictService;
        private readonly RealtimeService _realtimeService;
        private readonly RegionService _regionService;

        public ChartController(
            RegionService regionService,
            RealtimeService realtimeService,
            PredictService predictService)
        {
            _regionService = regionService;
            _predictService = predictService;
            _realtimeService = realtimeService;
        }

        [HttpPost]
        public ActionResult<List<MapChartEntity>> GetMapChartData([FromForm]string filter)
        {
            var result = new List<MapChartEntity>();
            if (!Enum.TryParse<MapChartFilter>(filter, true, out var mapChartFilter))
                return result;
            result = _realtimeService.GetMapChartData(mapChartFilter);
            return result;
        }

        [HttpPost]
        public ActionResult<List<WeatherData>> GetLineChartData([FromForm] string anyChartRegionId)
        {
            var result = new List<WeatherData>();
            if (string.IsNullOrEmpty(anyChartRegionId))
                return result;

            var region = _regionService.FindByAnyChartRegionId(anyChartRegionId);

            if (region == null)
                return result;

            result = _predictService.GetLineChartData(region.RegionName);

            return result;
        }
    }
}