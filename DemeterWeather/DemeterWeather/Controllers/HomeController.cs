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
using DemeterWeather.Models.JsonObjectFormat;

namespace DemeterProject.Controllers
{
    public class HomeController : Controller
    {
        Db dbop = new Db();

        private readonly ILogger<HomeController> _logger;

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        [HttpPost]
        public JsonResult LocationList(string prefix)
        {
            List<LocationList> list = dbop.GetListLocation(prefix);
            return Json(list);
        }

        [HttpPost]
        public JsonResult ChartInformationList(string filter)
        {
            List<ChartInformationList> chartInformation = dbop.GetChartInformation(filter);
            return Json(chartInformation);
        }

        [HttpPost]
        public JsonResult GetRealtime(string lat, string lon)
        {
            ForecastList res = dbop.GetWeatherForecast(lat, lon);
            return Json(res);
        }

        [HttpPost]
        public JsonResult GetPredict(string lat, string lon)
        {
            List<PredictList> res = dbop.GetPredictForecast(lat, lon);
            return Json(res);
        }

        [HttpGet]
        public async Task<IActionResult> Index()
        {
            return View();
        }

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
