using System;
using System.Collections.Generic;

namespace DemeterProject.Models
{
    public class Weather
    {
        public int WeatherId { get; set; }
        public int LocationID { get; set; }
        public DateTime Date { get; set; }
        public string Humidity { get; set; }
        public string Precipitation { get; set; }
        public string Wind { get; set; }
    }
}
