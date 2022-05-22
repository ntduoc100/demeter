// Please see documentation at https://docs.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.

var x = document.getElementById("location");

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    x.innerHTML = "Latitude: " + position.coords.latitude +
        " Longitude: " + position.coords.longitude;
}


function sendPosition(position) {
    var lat = position.coords.latitude;
    var lon = position.coords.longtitude;
    $.ajax({
        type: "GET",
        url: "/Home/Index?lat=" + lat,
        success: function (object) {
            console.log(object);
        }
    })
}
window.onload = getLocation();

