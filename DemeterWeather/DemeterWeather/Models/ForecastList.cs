namespace DemeterWeather.Models
{
    public class ForecastList
    {
        public string Id { get; set; }
        public string Time { get; set; }
        public string Temperature { get; set; }
        public string Wind { get; set; }
        public string Humidity { get; set; }
        public string Pressure { get; set; }
        public string Place { get; set; }
    }
}