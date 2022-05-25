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
            if (int.Parse(forecast.Temperature) < 30)
            {
                @ViewData["Background"] = "url(https://img5.thuthuatphanmem.vn/uploads/2021/12/28/anh-bau-troi-may-den-u-am-tuyet-vong_022428259.jpg)";
            }
            else
            {
                @ViewData["Background"] = "url(https://arizonaoddities.com/wp-content/uploads/2012/06/Clouds.jpg)";
            }
        }

        [HttpGet]
        public IActionResult Index(string locationName)
        {
            @ViewData["Location"] = locationName;
            SetHeaderWeather(locationName);
            List<ForecastList> predict = dbop.GetTimelyPredictForecast(locationName);
            for (var i = 0; i < 8; i++)
            {
                @ViewData["Time" + i] = predict[i].Time.Split('T')[0] + ' ' + predict[i].Time.Split('T')[1];
                @ViewData["Temp" + i] = predict[i].Temperature;
                @ViewData["Wind" + i] = "Wind: " + predict[i].Wind + " m/s";
                @ViewData["Humidity" + i] = "Humidity: " + predict[i].Humidity + "%";
                @ViewData["Pressure" + i] = "Pressure: " + predict[i].Pressure + " hPa";
                if (double.Parse(predict[i].Temperature) < 30.0)
                {
                    @ViewData["Image" + i] = "well.png";
                }
                else
                {
                    @ViewData["Image" + i] = "hot.png";
                }
            }
            return View();
        }
    }
}
