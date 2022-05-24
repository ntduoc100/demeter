// Please see documentation at https://docs.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.
var x = document.getElementById("location");
var temp = document.getElementById("temperature");
var wind = document.getElementById("wind"); 
var humidity = document.getElementById("humidity");
var pressure = document.getElementById("pressure");
var time = document.getElementById("time");

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(sendPosition);
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
    var lon = position.coords.longitude;
    $.ajax({
        type: "POST",
        url: '/Home/GetRealtime/',
        data: { lat: lat, lon: lon},
        success: function (result) {
            let myString = JSON.stringify(result);
            var stringify = JSON.parse(myString);
            let superscipt = "o";
            x.innerHTML = stringify['place']
            temp.innerHTML = stringify['temperature'] + superscipt.sup();
            wind.innerHTML = 'Wind: ' + stringify['wind'];
            humidity.innerHTML = 'Humidity: ' + stringify['humidity'];
            pressure.innerHTML = 'Pressure: ' + stringify['pressure'];
            time.innerHTML = 'Time: ' + stringify['time'];
        },
        error: function () {
            alert('Failed to receive the Location');
            console.log('Failed ');
        }
    })
}



function clickLocation() {
    var str = x.innerHTML.split(' ');
    var strNew = "";
    str.forEach((value, index, array) => {
        if (index == 0) {
            strNew = value;
        }
        else {
            strNew = strNew + '+' + value;
        }
    });

    $.ajax({
        type: "GET",
        url: '/Locations/Index/',
        data: { locationName: x.innerHTML },
        success: function (result) {
            window.open('https://localhost:44381/Locations?locationName=' + strNew);
        },
        error: function () {
            alert('Failed to receive the Location');
            console.log('Failed ');
        }
    })
}