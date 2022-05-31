using System.Collections.Generic;
using DemeterWeather.Models;
using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using System.Linq;
using DemeterWeather.Services;

namespace DemeterWeather.Controllers
{
    public class HomeController : Controller
    {
        private readonly PredictService _predictService;
        private readonly RealtimeService _realtimeService;
        private readonly RegionService _regionService;

        public HomeController(
            RegionService regionService,
            RealtimeService realtimeService,
            PredictService predictService)
        {
            _regionService = regionService;
            _predictService = predictService;
            _realtimeService = realtimeService;
        }

        public IActionResult Index()
        {
            return View();
        }

        public IActionResult Detail(string regionName)
        {
            if (string.IsNullOrEmpty(regionName))
                return RedirectToAction("Index");

            var region = _regionService.FindByName(regionName);
            if (region == null)
            {
                var text = RegionService.PreprocessRegionName(regionName);
                if (!string.IsNullOrEmpty(text))
                {
                    region = _regionService.DoFuzzySearch(regionName)
                        .FirstOrDefault();
                }
            }

            if (region == null)
                return RedirectToAction("NotExisted");

            ViewData["RegionName"] = region.RegionName;

            var realtimeData = _realtimeService.FindByRegionName(region.RegionName);
            if (realtimeData == null)
                return RedirectToAction("Error");

            ViewData["Temperature"] = realtimeData.Temperature;
            ViewData["Wind"] = "Wind: " + realtimeData.Wind + " km/h";
            ViewData["Humidity"] = "Humidity: " + realtimeData.Humidity + "%";
            ViewData["Pressure"] = "Pressure: " + realtimeData.Pressure + " hPa";
            ViewData["Time"] = "Time: " + realtimeData.Time.Split('T')[0] + ' ' + realtimeData.Time.Split('T')[1];
            ViewData["Background"] = realtimeData.Temperature < 30
                ? "url(https://www.wallpaperup.com/uploads/wallpapers/2015/11/19/838974/1a6094aabc9ec2b40bbbb694a8a55c38-700.jpg)"
                : "url(https://arizonaoddities.com/wp-content/uploads/2012/06/Clouds.jpg)";

            var limit = 8;
            var predictData = _predictService.FindByRegion(region.RegionName, limit);
            if (predictData.Count != limit)
                return RedirectToAction("Error");

            for (var i = 0; i < limit; i++)
            {
                ViewData["Time" + i] = predictData[i].Time.Split('T')[0] + ' ' + predictData[i].Time.Split('T')[1];
                ViewData["Temp" + i] = predictData[i].Temperature;
                ViewData["Wind" + i] = "Wind: " + predictData[i].Wind + " km/h";
                ViewData["Humidity" + i] = "Humidity: " + predictData[i].Humidity + "%";
                ViewData["Pressure" + i] = "Pressure: " + predictData[i].Pressure + " hPa";
                // change weather forecast icon based on temperature
                ViewData["Image" + i] = predictData[i].Temperature < 30
                    ? "well.png"
                    : "hot.png";
            }

            return View();
        }

        public IActionResult NotExisted()
        {
            return View();
        }

        public IActionResult About()
        {
            return View();
        }


        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}