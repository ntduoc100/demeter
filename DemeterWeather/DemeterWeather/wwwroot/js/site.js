// Please see documentation at https://docs.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.
var place = document.getElementById("location");
var temp = document.getElementById("temperature");
var wind = document.getElementById("wind"); 
var humidity = document.getElementById("humidity");
var pressure = document.getElementById("pressure");
var time = document.getElementById("time");

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(sendPosition);
        navigator.geolocation.getCurrentPosition(getPredict);
    } else {
        place.innerHTML = "Geolocation is not supported by this browser.";
    }
}


function sendPosition(position) {
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;
    $.ajax({
        type: "POST",
        url: '/Home/GetRealtime/',
        data: { lat: lat, lon: lon },
        success: function (result) {
            let myString = JSON.stringify(result);
            var stringify = JSON.parse(myString);
            let superscipt = "o";
            place.innerHTML = stringify['place']
            temp.innerHTML = stringify['temperature'] + superscipt.sup() + 'C';
            wind.innerHTML = 'Wind: ' + stringify['wind'];
            humidity.innerHTML = 'Humidity: ' + stringify['humidity'];
            pressure.innerHTML = 'Pressure: ' + stringify['pressure'];
            time.innerHTML = 'Time: ' + stringify['time'].split('T')[0] + ' ' + stringify['time'].split('T')[1];
        },
        error: function () {
            alert('Failed to receive the Location');
            console.log('Failed ');
        }
    });
}

function getPredict(position) {
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;
    $.ajax({
        type: "POST",
        url: '/Home/GetPredict/',
        data: { lat: lat, lon: lon },               
        success: function (result) {
            let myString = JSON.stringify(result);
            var stringify = JSON.parse(myString);
            let superscipt = "o";
            for (var i = 0; i < 5; i++) {
                var date = document.getElementById("date" + (i + 1));
                var mean = document.getElementById("mean" + (i + 1));
                var range = document.getElementById("range" + (i + 1));
                date.innerHTML = stringify[i]['date'];
                mean.innerHTML = parseInt(stringify[i]['meanTemperature']) + superscipt.sup();;
                range.innerHTML = stringify[i]['lowerBoundTemperature'] + ' - ' + stringify[i]['upperBoundTemperature'];
            }
        },
        error: function () {
            alert('Failed to receive the Predict');
            console.log('Failed ');
        }
    });
}


function clickLocation() {
    var str = place.innerHTML.split(' ');
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
        data: { locationName: place.innerHTML },
        success: function (result) {
            window.open('https://localhost:44381/Locations?locationName=' + strNew);
        },
        error: function () {
            alert('Failed to receive the Location');
            console.log('Failed ');
        }
    })
}