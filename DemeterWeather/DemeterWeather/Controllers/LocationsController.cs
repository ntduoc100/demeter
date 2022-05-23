using Microsoft.AspNetCore.Mvc;

namespace DemeterWeather.Controllers
{
    public class LocationsController : Controller
    {
        public IActionResult Index(string locationName)
        {
            @ViewData["Location"] = locationName;
            return View();
        }
    }
}
