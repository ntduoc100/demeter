using DemeterProject.Models;
using System;
using System.Linq;

namespace DemeterProject.Data
{
    public static class DbInitializer
    {
        public static void Initialize(WeatherContext context)
        {
            context.Database.EnsureCreated();

            if (context.Locations.Any())
            {
                return;
            }

            var locations = new Location[]
            {
                new Location{LocationName = "Ho Chi Minh City"},
                new Location{LocationName = "Da Nang City"},
                new Location{LocationName = "Tay Ninh"}
            };
            foreach (Location l in locations)
            {
                context.Locations.Add(l);
            }
            context.SaveChanges();

            var weather = new Weather[]
            {
                new Weather{ LocationID = 1, Humidity = "50%", Precipitation = "48%", Wind = "15km/h", Date = DateTime.Parse("2003-09-01")},
                new Weather{ LocationID = 2, Humidity = "50%", Precipitation = "48%", Wind = "15km/h", Date = DateTime.Parse("2003-09-01")},
                new Weather{ LocationID = 3, Humidity = "50%", Precipitation = "48%", Wind = "15km/h", Date = DateTime.Parse("2003-09-01")},
                new Weather{ LocationID = 4, Humidity = "50%", Precipitation = "48%", Wind = "15km/h", Date = DateTime.Parse("2003-09-01")}
            };
            foreach(Weather w in weather)
            {
                context.Weathers.Add(w);
            }
            context.SaveChanges();
        }
    }
}
