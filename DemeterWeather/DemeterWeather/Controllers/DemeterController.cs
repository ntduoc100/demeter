using Microsoft.AspNetCore.Mvc;
using MongoDB.Driver;
using MongoDB.Bson;
using DemeterWeather.Models;
using System.Text.Encodings.Web;
using System.Collections.Generic;

namespace DemeterWeather.Controllers
{
    public class DemeterController: Controller
    {

        // TODO: create a function to calculate min distance and return the name city
        // Input: lat and lon of current location
        // Output: the name of city to view on html
        [HttpGet]
        public IEnumerable<WeatherForecast> Index()
        {
            var client = new MongoClient("mongodb+srv://root:12345ADMIN@cluster0.5qjhz.mongodb.net/?retryWrites=true&w=majority");
            var database = client.GetDatabase("demeter");

            var collection = database.GetCollection<WeatherForecast>("predict_data");

            // return HtmlEncoder.Default.Encode($"Hello, NumTimes is: ");
            // var region = collection.Find(s => s.Place == "Ha Nam").ToList();
            var region = collection.AsQueryable();
            return region;
        }
    }
}
