using System.Data;
using System.Data.SqlClient;
using DemeterWeather.Models;
using System.Configuration;
using System.Collections.Generic;
using DemeterWeather.Data;
using MongoDB.Driver;

namespace DemeterProject.Data

{
    public class Db
    {
        MongoDbContext database = new MongoDbContext();

        public List<LocationList> LocationGet(string prefix)
        {
            List<LocationList> list = new List<LocationList>();
            var collection = database.Region;
            foreach (var item in collection.Find(s => s.Place.Contains(prefix)).ToList())
            {
                list.Add(new LocationList
                {
                    label = item.Place.ToString(),
                    val = item.PlaceId.ToString(),
                });;
            }
            return list;
        }
    }
}
