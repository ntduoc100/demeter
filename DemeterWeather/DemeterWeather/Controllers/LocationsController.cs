using DemeterProject.Data;
using DemeterWeather.Data;
using DemeterWeather.Models;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;

namespace DemeterWeather.Controllers
{
    public class LocationsController : Controller
    {
        MongoDbContext database = new MongoDbContext();
        Db dbop = new Db();

        public void SetHeaderWeather(string locationName)
        {
            ForecastList forecast = dbop.getForecastByLocation(locationName);
            ViewData["Temperature"] = forecast.Temperature;
            ViewData["Wind"] = "Wind: " + forecast.Wind + " m/s";
            ViewData["Humidity"] = "Humidity: " + forecast.Humidity + "%";
            ViewData["Pressure"] = "Pressure: " + forecast.Pressure + " hPa";
            ViewData["Time"] = "Time: " + forecast.Time.Split('T')[0] + ' ' + forecast.Time.Split('T')[1];
        }

        [HttpGet]
        public IActionResult Index(string locationName)
        {
            @ViewData["Location"] = locationName;
            SetHeaderWeather(locationName);
            List<ForecastList> predict = dbop.GetTimelyPredictForecast(locationName);
            for (var i = 0; i < 8; i++)
            {
                ViewData["Time" + i] = predict[i].Time.Split('T')[0] + ' ' + predict[i].Time.Split('T')[1];
                @ViewData["Temp" + i] = predict[i].Temperature;
                @ViewData["Wind" + i] = "Wind: " + predict[i].Wind + " m/s";
                @ViewData["Humidity" + i] = "Humidity: " + predict[i].Humidity + "%";
                @ViewData["Pressure" + i] = "Pressure: " + predict[i].Pressure + " hPa";
            }
            return View();
        }
    }
}
