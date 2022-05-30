using DemeterWeather.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using DemeterProject.Data;
using System.Text.Encodings.Web;

namespace DemeterProject.Controllers
{
    public class HomeController : Controller
    {
        // create a database object
        Db dbop = new Db();

        private readonly ILogger<HomeController> _logger;

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        // controller function for the autocomplete search in the client
        // Input: string prefix
        // Output: Json format of list of LocationList
        [HttpPost]
        public JsonResult LocationList(string prefix)
        {
            List<ResultList> list = dbop.GetListLocation(prefix);
            return Json(list);
        }

        // controller function for returning the chart place id for the location name
        // Input: string city
        // Output: chartPlaceId
        [HttpPost]
        public string GetLocationMapID(string city)
        {
            return dbop.GetLocationMapID(city);
        }

        // controller function to get the information for the Map Chart
        // Input: string filter
        // Output: Json format of the List of ResultList 
        [HttpPost]
        public JsonResult MapChartInformationList(string filter)
        {
            List<ResultList> chartInformation = dbop.GetMapChartInformation(filter);
            return Json(chartInformation);
        }

        // controller function to get the information for the Line Chart
        // Input: string chartplaceId
        // Output: Json format of the List of ForecaseList
        [HttpPost]
        public JsonResult LineChartInformationList(string chartPlaceId)
        {
            List<ForecastList> lines = dbop.GetLineChartInformation(chartPlaceId);
            return Json(lines);
        }

        // controller function to get the realtime weather forecast
        // Input: coordinate - lat, lon
        // Output: Json format of the List of the ForecaseList
        [HttpPost]
        public JsonResult GetRealtime(string lat, string lon)
        {
            ForecastList res = dbop.GetWeatherForecast(lat, lon);
            return Json(res);
        }

        // controller functon to get the predict forecast
        // Input: coordinate - lat, lon
        // Output: Json format of the List of PredictList
        [HttpPost]
        public JsonResult GetPredict(string lat, string lon)
        {
            List<PredictList> res = dbop.GetPredictForecast(lat, lon);
            return Json(res);
        }

        // controller function for Index View page
        [HttpGet]
        public async Task<IActionResult> Index()
        {
            return View();
        }

        // controller function for About View page
        public async Task<IActionResult> About()
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
