using DemeterWeather.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using DemeterProject.Data;

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
        public IActionResult Index(string CountryName, string CountryID)
        {
            ViewBag.Message = "Country Name: " + CountryName + "Country ID: " + CountryID;
            return View();
        }

        [HttpPost]
        public JsonResult CountryList(string prefix)
        {
            List<LocationList> list = dbop.LocationGet(prefix);
            return Json(list);
        }

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
