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
var chartPlaceId;

// Function to create a realtime clock at the navigation bar
// Input: none
// Output: draw a clock on nav bar by id
function realtimeClock() {
    var rtClock = new Date();
    var hours = rtClock.getHours();
    var minutes = rtClock.getMinutes();
    var seconds = rtClock.getSeconds();

    var amPm = (hours < 12) ? "AM" : "PM" 

    hours = (hours > 12) ? hours - 12 : hours;

    // Add zero digit to front of variable and take the last 2 digits to create the hour/minute/second
    hours = ("0" + hours).slice(-2);    
    minutes = ("0" + minutes).slice(-2);
    seconds = ("0" + seconds).slice(-2);

    document.getElementById('clock').innerHTML = hours + " : " + minutes + " : " + seconds + " " + amPm;
    var t = setTimeout(realtimeClock, 500);
}

// function to set the loading image to invisible
function setImageVisible() {
    document.getElementById("loading-image").remove();
    document.getElementById("loading").remove();
}

// function to get the location id for drawing chart by mapping the city string with database in server
function getLocationMapID() {
    $.ajax({
        type: "POST",
        url: '/Home/GetLocationMapID/',
        data: { city: place.innerHTML },
        success: function (result) {
            chartPlaceId = result;
            updateLineChart();
        }
    });
}
// Function to get the gps lcoation at homepage and send coordinate to server
function getLocation() {
    if (window.location.pathname == '/') {
        if (navigator.geolocation) {
            realtimeClock();
            updateMapChart();
            navigator.geolocation.getCurrentPosition(sendPosition);
            navigator.geolocation.getCurrentPosition(getPredict);
        } else {
            place.innerHTML = "Geolocation is not supported by this browser.";
        }
    }
}

// send coordinate latitude and longitude to server and receive weather forecatse at that location in realtime
// Input: coordinate of position
// Output: display the weather information in homepage
function sendPosition(position) {
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;
    $.ajax({
        type: "POST",
        url: '/Home/GetRealtime/',
        data: { lat: lat, lon: lon },
        success: function (result) {
            let myString = JSON.stringify(result); // stringify the Object array return by server
            var stringify = JSON.parse(myString); // parse the stringify string to JSON format
            let superscipt = "o";
            place.innerHTML = stringify['place']
            temp.innerHTML = stringify['temperature'] + superscipt.sup() + 'C';
            wind.innerHTML = 'Wind: ' + stringify['wind'] + ' km/h';
            humidity.innerHTML = 'Humidity: ' + stringify['humidity'] + '%';
            pressure.innerHTML = 'Pressure: ' + stringify['pressure'] + ' hPa';
            time.innerHTML = 'Time: ' + stringify['time'].split('T')[0] + ' ' + stringify['time'].split('T')[1];
            getLocationMapID();
            // background will change following by the temperature with the threshold as 30 degree
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
            setImageVisible();
        },
        error: function () {
            alert('Failed to receive the Location');
            console.log('Failed ');
        }
    });
}

// function get predict weathr forecast for the next 5 days
// Input: coordinate position of gps function
// Output: the array of 5 Objects
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

// function when clicking to the city string of gps location frame
// Input: none
// Output: redirect to the location detail view page with the parameter as the location name.
function clickLocation() {
    var str = place.innerHTML.split(' ');
    var strNew = "";
    // preprocess the city name to create the parameter for HET method in Locations controller
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
            window.open('/Locations?locationName=' + strNew); // open the Locations Index View with parameter
        },
        error: function () {
            alert('Failed to receive the Location');
            console.log('Failed ');
        }
    })
}

// Change the Map frame with the filter taken by radio buttons
// use ajax to send filter to server and receive the data mapping for the map chart
function updateMapChart() {
    var filter = document.querySelector('input[name="filters"]:checked').value;
    if (chartPlaceId != null) {
        updateLineChart();
    }
    document.getElementById("container").innerHTML = "";
    $.ajax({
        type: "POST",
        url: '/Home/MapChartInformationList/',
        data: { filter: filter },
        success: function (result) {
            let myString = JSON.stringify(result);
            var stringify = JSON.parse(myString);
            for (var i = 0; i < stringify.length; i++) {
                result.push({ "id": stringify[i]['label'], "value": parseInt(stringify[i]['val']) });
            }

            // draw chart
            anychart.onDocumentReady(function () {
                var map = anychart.map();
                var dataSet = anychart.data.set(result);
                series = map.choropleth(dataSet);

                series.geoIdField('id');

                series.colorScale(anychart.scales.linearColor('#deebf7', '#3182bd'));
                series.hovered().fill('#addd8e');

                map.title("Realtime Map for " + filter);


                map.geoData(anychart.maps['vietnam']);

                map.container('container');

                map.draw();

                map.listen("pointDblClick", function (e) {
                    chartPlaceId = e.point.get("id");
                    updateLineChart();
                });
            });
        }
    });
}

// Change the Line Chart with the filter taken by radio buttons and the ChartPlaceId taken from the map or gps for realtime location
// Use ajax to send chart place id to server and receive the value of prediction
function updateLineChart() {
    var filter = document.querySelector('input[name="filters"]:checked').value;
    document.getElementById("lineChart").innerHTML = "";
    $.ajax({
        type: "POST",
        url: '/Home/LineChartInformationList/',
        data: { chartPlaceId: chartPlaceId },
        success: function (result) {
            let myString = JSON.stringify(result);
            var stringify = JSON.parse(myString);

            anychart.onDocumentReady(function () {
                stringify = stringify.sort(function (data1, data2) {
                    return ('' + data1["time"]).localeCompare(data2["time"]);
                })

                // Convert data to 2d array
                var newData = []
                for (let i = 0; i < 8; i++) {
                    newData[i] = [
                        stringify[i].time.slice(11, 16),
                        stringify[i].temperature,
                        stringify[i].humidity,
                        stringify[i].pressure,
                        stringify[i].wind,
                    ]
                }
                var chart = anychart.area();

                // create tooltip for line chart
                var tooltip = chart.tooltip()
                tooltip.format(function (e) {
                    return "Temperature: " + newData[this.index][1]
                        + "\nHumidity: " + newData[this.index][2]
                        + "\nPressure: " + newData[this.index][3]
                        + "\nWind: " + newData[this.index][4]
                })

                chart.background()

                chart.padding([20, 20, 20, 20]);
                chart.animation(true);
                chart.crosshair(false);
                var title = chart.title();
                title.text("Predicted " + filter + " for " + stringify[0].place);
                title.fontSize(20);
                title.fontFamily("Roboto-Light");
                chart.title().enabled(true)
                chart.yAxis().enabled(true);
                chart.xAxis().labels()
                var dataSet = anychart.data.set(newData);
                // set the index for corresponding filter to use for create dataset mapping
                var mapValue = {
                    "Temperature": 1,
                    "Humidity": 2,
                    "Pressure": 3,
                    "Wind": 4,
                }
                var firstSeriesData = dataSet.mapAs({ x: 0, value: mapValue[filter] });
                var series;
                series = chart.splineArea(firstSeriesData).fill(['#deebf7', '#3182bd'], 90);
                series.name('Time');
                series.labels().enabled(true).anchor('top').padding(10);
                series.labels().fontFamily("Roboto-Light");
                chart.container('lineChart');
                chart.draw();
            });
        }
    });
}
