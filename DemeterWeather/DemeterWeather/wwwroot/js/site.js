// Please see documentation at https://docs.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.
var place = document.getElementById("location");
var temp = document.getElementById("temperature");
var wind = document.getElementById("wind"); 
var humidity = document.getElementById("humidity");
var pressure = document.getElementById("pressure");
var time = document.getElementById("time");
var background = document.getElementById("background");

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
            wind.innerHTML = 'Wind: ' + stringify['wind'] + ' m/s';
            humidity.innerHTML = 'Humidity: ' + stringify['humidity'] +'%';
            pressure.innerHTML = 'Pressure: ' + stringify['pressure'] + ' hPa';
            time.innerHTML = 'Time: ' + stringify['time'].split('T')[0] + ' ' + stringify['time'].split('T')[1];
            if (parseInt(stringify['temperature']) < 30) {
                background.style.backgroundImage = "url(https://live.staticflickr.com/2869/9432775833_d5f673978d_b.jpg)";
                temp.style.color = "white";
                wind.style.color = "white";
                humidity.style.color = "white";
                pressure.style.color = "white";
                time.style.color = "white";
            }
            else {
                background.style.backgroundImage = "url(https://www.meteorologiaenred.com/wp-content/uploads/2021/01/nubosidad.jpg)";
            }
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
                mean.innerHTML = parseInt(stringify[i]['meanTemperature']) + superscipt.sup() + 'C';
                range.innerHTML = parseInt(stringify[i]['lowerBoundTemperature']) + superscipt.sup() + ' - ' + parseInt(stringify[i]['upperBoundTemperature']) + superscipt.sup();
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