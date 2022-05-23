using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace DemeterWeather.Models
{
    public class WeatherForecast
    {
        [BsonId]
        public ObjectId Id { get; set; }
        [BsonElement("Time")]
        public string Time { get; set; }
        [BsonElement("Temperature")]
        public double Temperature { get; set; }
        [BsonElement("Wind")]
        public double Wind { get; set; }
        [BsonElement("Humidity")]
        public double Humidity { get; set; }
        [BsonElement("Pressure")]
        public double Pressure { get; set; }
        [BsonElement("Place")]
        public string Place { get; set; }
    }
}
