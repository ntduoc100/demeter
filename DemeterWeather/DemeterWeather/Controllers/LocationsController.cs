using DemeterProject.Data;
using DemeterWeather.Data;
using DemeterWeather.Models;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;

namespace DemeterWeather.Controllers
{
    public class LocationsController : Controller
    {
        Db dbop = new Db();

        // Show the weather forecast information for a specify location
        // Input: string locationName -> from searching or from clicking the gps location at homepage
        // Output: mapping the data result by query from database to correspinding view data
        public void SetHeaderWeather(string locationName)
        {
            ForecastList forecast = dbop.getForecastByLocation(locationName);
            ViewData["Temperature"] = forecast.Temperature;
            ViewData["Wind"] = "Wind: " + forecast.Wind + " km/h";
            ViewData["Humidity"] = "Humidity: " + forecast.Humidity + "%";
            ViewData["Pressure"] = "Pressure: " + forecast.Pressure + " hPa";
            ViewData["Time"] = "Time: " + forecast.Time.Split('T')[0] + ' ' + forecast.Time.Split('T')[1];
            if (int.Parse(forecast.Temperature) < 30)
            {
                @ViewData["Background"] = "url(https://www.wallpaperup.com/uploads/wallpapers/2015/11/19/838974/1a6094aabc9ec2b40bbbb694a8a55c38-700.jpg)";
            }
            else
            {
                @ViewData["Background"] = "url(https://arizonaoddities.com/wp-content/uploads/2012/06/Clouds.jpg)";
            }
        }

        // Controller for Error view page
        [HttpGet]
        public IActionResult Error()
        {
            return View();
        }

        // Controller for Index View page
        [HttpGet]
        public IActionResult Index(string locationName)
        {
            // check whether the location exist or not
            if (dbop.CheckExistLocation(locationName) == false)
            {
                // if not exist that lcoation, redirect to the error page
                return RedirectToAction("Error", "Locations");
            }
            else
            {
                // if exist that location, query data and mapping to show the information
                @ViewData["Location"] = locationName;
                SetHeaderWeather(locationName);
                // get array of predict forecast for the location
                List<ForecastList> predict = dbop.GetTimelyPredictForecast(locationName);
                for (var i = 0; i < 8; i++)
                {
                    // mapping information for the view data
                    @ViewData["Time" + i] = predict[i].Time.Split('T')[0] + ' ' + predict[i].Time.Split('T')[1];
                    @ViewData["Temp" + i] = predict[i].Temperature;
                    @ViewData["Wind" + i] = "Wind: " + predict[i].Wind + " km/h";
                    @ViewData["Humidity" + i] = "Humidity: " + predict[i].Humidity + "%";
                    @ViewData["Pressure" + i] = "Pressure: " + predict[i].Pressure + " hPa";
                    // change weather forecast icon based on temperature
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
}
