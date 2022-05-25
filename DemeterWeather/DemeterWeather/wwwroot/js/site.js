// Please see documentation at https://docs.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.
var x = document.getElementById("location");

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
        url: '/Home/GetLocation/',
        data: { lat: lat, lon: lon},
        success: function (result) {
            x.innerHTML = result;
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