using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace DemeterWeather.Models
{
    public class Region
    {
        [BsonId]
        public ObjectId Id { get; set; }
        [BsonElement("Place")]
        public string Place { get; set; }
        [BsonElement("id")]
        public int PlaceId { get;set; }
        [BsonElement("place_id")]
        public string ChartPlaceId { get; set; }
        [BsonElement("coordinate")]
        public double[] Coordinate { get; set; }
    }
}
