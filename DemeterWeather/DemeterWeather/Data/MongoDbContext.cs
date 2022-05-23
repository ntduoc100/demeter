using MongoDB.Driver;
using DemeterWeather.Models;

namespace DemeterWeather.Data
{
    public class MongoDbContext
    {
        private readonly IMongoDatabase _mongoDb;
        public MongoDbContext()
        {
            var client = new MongoClient("mongodb+srv://root:12345ADMIN@cluster0.5qjhz.mongodb.net/?retryWrites=true&w=majority");
            _mongoDb = client.GetDatabase("demeter");
        }

        public IMongoCollection<Region> Region
        {
            get
            {
                return _mongoDb.GetCollection<Region>("region_data");
            }
        }

        public IMongoCollection<WeatherForecast> Realtime
        {
            get
            {
                return _mongoDb.GetCollection<WeatherForecast>("realtime_data");
            }
        }

        public IMongoCollection<WeatherForecast> Predict
        {
            get
            {
                return _mongoDb.GetCollection<WeatherForecast>("predict_data");
            }
        }
    }
}
