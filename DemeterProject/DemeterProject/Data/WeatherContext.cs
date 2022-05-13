using DemeterProject.Models;
using Microsoft.EntityFrameworkCore;

namespace DemeterProject.Data
{
    public class WeatherContext : DbContext
    {
        public WeatherContext(DbContextOptions<WeatherContext> options) : base(options)
        {
        }

        public DbSet<Location> Locations { get; set; }
        public DbSet<Weather> Weathers { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Location>().ToTable("Location");
            modelBuilder.Entity<Weather>().ToTable("Weather");
        }
    }
}
