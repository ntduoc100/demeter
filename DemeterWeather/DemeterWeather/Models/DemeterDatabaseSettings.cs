namespace DemeterWeather.Models
{
    public interface IDemeterDatabaseSettings
    {
        string RegionCollectionName { get; set; }
        string RealtimeCollectionName { get; set; }
        string PredictCollectionName { get; set; }
        string ConnectionString { get; set; }
        string DatabaseName { get; set; }
    }

    public class DemeterDatabaseSettings : IDemeterDatabaseSettings
    {
        public string ConnectionString { get; set; } = null!;
        public string DatabaseName { get; set; } = null!;
        public string RegionCollectionName { get; set; } = null!;
        public string RealtimeCollectionName { get; set; } = null!;
        public string PredictCollectionName { get; set; } = null!;
    }
}