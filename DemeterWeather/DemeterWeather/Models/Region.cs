using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace DemeterWeather.Models
{
    public class Region
    {
        [BsonId]
        [BsonRepresentation(BsonType.ObjectId)]
        public string Id { get; set; }
        [BsonElement("Place")]
        public string RegionName { get; set; }
        [BsonElement("id")]
        public int RegionId { get; set; }
        [BsonElement("place_id")]
        public string AnyChartRegionId { get; set; }
        [BsonElement("coordinate")]
        public double[] Coordinate { get; set; }
    }
}
