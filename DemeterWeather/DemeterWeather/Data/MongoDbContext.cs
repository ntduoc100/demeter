using MongoDB.Driver;
using DemeterWeather.Models;

namespace DemeterWeather.Data
{
    public class MongoDbContext
    {
        private readonly IMongoDatabase _mongoDb;

        // create a connection with mongodb to get the database
        public MongoDbContext()
        {
            var client = new MongoClient("mongodb+srv://root:12345ADMIN@cluster0.5qjhz.mongodb.net/?retryWrites=true&w=majority");
            _mongoDb = client.GetDatabase("demeter");
        }

        // return the Region collection corresponding to region_data in database
        public IMongoCollection<Region> Region
        {
            get
            {
                return _mongoDb.GetCollection<Region>("region_data");
            }
        }
        
        // return the Realtime collection corresponding to realtime_data in database
        public IMongoCollection<WeatherForecast> Realtime
        {
            get
            {
                return _mongoDb.GetCollection<WeatherForecast>("realtime_data");
            }
        }

        // return the Predict collection corresponding to predict_data in database
        public IMongoCollection<WeatherForecast> Predict
        {
            get
            {
                return _mongoDb.GetCollection<WeatherForecast>("predict_data");
            }
        }
    }
}
