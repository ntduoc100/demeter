using Microsoft.AspNetCore.Mvc;

namespace DemeterWeather.Controllers
{
    public class LocationsController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
