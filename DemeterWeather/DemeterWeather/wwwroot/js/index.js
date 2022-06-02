var regionName;
var temp;
var wind;
var humidity;
var pressure;
var time;
var background;
var anyChartRegionId;

$(document).ready(function() {
    regionName = document.getElementById("regionName");
    temp = document.getElementById("temperature");
    wind = document.getElementById("wind");
    humidity = document.getElementById("humidity");
    pressure = document.getElementById("pressure");
    time = document.getElementById("time");
    background = document.getElementById("background");

    getLocation();
});


// Function to get the gps location at homepage and send coordinate to server
function getLocation() {
    if (window.location.pathname == "/") {
        realtimeClock();
        updateMapChart();
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(sendPosition, showError);
            navigator.geolocation.getCurrentPosition(getPredict);
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    }
}

// Change the Map frame with the filter taken by radio buttons
// use ajax to send filter to server and receive the data mapping for the map chart
function updateMapChart() {
    var filter = document.querySelector('input[name="filters"]:checked').value;
    if (anyChartRegionId != null) {
        updateLineChart();
    }
    document.getElementById("mapChart").innerHTML = "";
    $.ajax({
        type: "POST",
        url: "/api/Chart/GetMapChartData/",
        data: { "filter": filter },
        success: function(result) {
            var data = [];
            for (let i = 0; i < result.length; i++) {
                data.push({
                    "id": result[i]["AnyChartRegionId"],
                    "value": parseFloat(result[i]["Data"])
                });
            }

            // draw chart
            anychart.onDocumentReady(function() {
                const map = anychart.map();
                const dataSet = anychart.data.set(data);
                series = map.choropleth(dataSet);

                series.geoIdField("id");

                if (filter == "Temperature")
                    series.colorScale(anychart.scales.linearColor("#FFC3C3", "#990000"));
                else if (filter == "Humidity")
                    series.colorScale(anychart.scales.linearColor("#deebf7", "#3182bd"));
                else if (filter == "Wind")
                    series.colorScale(anychart.scales.linearColor("#C4DDFF", "#112B3C"));
                else
                    series.colorScale(anychart.scales.linearColor("#DAE5D0", "#B4E197"));
                series.hovered().fill("#addd8e");

                series.tooltip().format(function(e) {
                    return filter.toString() +
                        ": " +
                        e.getData("value");
                });

                map.title(`Realtime Map for ${filter}`);

                map.geoData(anychart.maps["vietnam"]);

                map.container("mapChart");

                map.draw();

                map.listen("pointDblClick",
                    function(e) {
                        anyChartRegionId = e.point.get("id");
                        updateLineChart();
                    });
            });
        }
    });
}

// send coordinate latitude and longitude to server and receive weather forecatse at that location in realtime
// Input: coordinate of position
// Output: display the weather information in homepage
function sendPosition(position) {
    if (position != null) {
        var lat = position.coords.latitude;
        var lon = position.coords.longitude;
    } else {
        var lat = "10.75";
        var lon = "106.666672";
    }
    $.ajax({
        type: "POST",
        url: "api/Region/GetRealtimeWeatherData/",
        data: { "lat": lat, "lon": lon },
        success: function(result) {
            const superscript = "o";
            regionName.innerHTML = result["RegionName"];
            temp.innerHTML = result["Temperature"] + superscript.sup() + "C";
            wind.innerHTML = `Wind: ${result["Wind"]} km/h`;
            humidity.innerHTML = `Humidity: ${result["Humidity"]}%`;
            pressure.innerHTML = `Pressure: ${result["Pressure"]} hPa`;
            time.innerHTML = `Time: ${result["Time"].split("T")[0]} ${result["Time"].split("T")[1]}`;

            getAnyChartRegionId();

            // background will change following by the temperature with the threshold as 30 degree
            if (parseInt(result["Temperature"]) < 30) {
                background.style.backgroundImage =
                    "url(https://live.staticflickr.com/2869/9432775833_d5f673978d_b.jpg)";
                temp.style.color = "white";
                wind.style.color = "white";
                humidity.style.color = "white";
                pressure.style.color = "white";
                time.style.color = "white";
            } else {
                background.style.backgroundImage =
                    "url(https://www.meteorologiaenred.com/wp-content/uploads/2021/01/nubosidad.jpg)";
            }
            setImageVisible();
        },
        error: function() {
            alert("Failed to receive the Location");
            console.log("Failed ");
        }
    });
}

function showError(error) {
    switch (error.code) {
    case error.PERMISSION_DENIED:
        console.log("User denied the request for Geolocation.");
        break;
    case error.POSITION_UNAVAILABLE:
        console.log("Location information is unavailable.");
        break;
    case error.TIMEOUT:
        console.log("The request to get user location timed out.");
        break;
    case error.UNKNOWN_ERROR:
        console.log("An unknown error occurred.");
        break;
    }
    setImageVisible();
    sendPosition();
    getPredict();
}

// function to get the location id for drawing chart by mapping the city string with database in server
function getAnyChartRegionId() {
    $.ajax({
        type: "POST",
        url: "/api/Region/GetAnyChartRegionId/",
        data: { "regionName": regionName.innerHTML },
        success: function(result) {
            anyChartRegionId = result;
            updateLineChart();
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
        url: "/api/Chart/GetLineChartData/",
        data: { "anyChartRegionId": anyChartRegionId },
        success: function(result) {
            anychart.onDocumentReady(function() {

                // Convert data to 2d array
                var newData = [];
                for (let i = 0; i < 8; i++) {
                    newData[i] = [
                        result[i]["Time"].slice(5, 10) + " " + result[i]["Time"].slice(11, 16),
                        result[i]["Temperature"],
                        result[i]["Humidity"],
                        result[i]["Pressure"],
                        result[i]["Wind"],
                    ];
                }
                var chart = anychart.area();

                // create tooltip for line chart
                var tooltip = chart.tooltip();
                tooltip.format(function(e) {
                    return `Temperature: ${newData[this.index][1]}\nHumidity: ${newData[this.index][2]}\nPressure: ${
                        newData[this.index][3]}\nWind: ${newData[this.index][4]}`;
                });

                chart.background();

                chart.padding([20, 20, 20, 20]);
                chart.animation(true);
                chart.crosshair(false);

                var regionName = result[0]["RegionName"];
                var title = chart.title();

                title.useHtml(true);

                if (filter == "Temperature")
                    title.text(
                        `Predicted ${filter} for <b style="color:#990000;">${regionName}</b>` + 
                        "<br><i style=\"font-size: 0.8rem;\">click for detail</a>"
                    );
                else if (filter == "Humidity")
                    title.text(
                        `Predicted ${filter} for <b style="color:#3182bd;">${regionName}</b>` + 
                        "<br><i style=\"font-size: 0.8rem;\">click for detail</a>"
                    );
                else if (filter == "Wind")
                    title.text(
                        `Predicted ${filter} for <b style="color:#112B3C;">${regionName}</b>` + 
                        "<br><i style=\"font-size: 0.8rem;\">click for detail</a>"
                    );
                else
                    title.text(
                        `Predicted ${filter} for <b style="color:#00B14F;">${regionName}</b>` + 
                        "<br><i style=\"font-size: 0.8rem;\">click for detail</a>"
                    );

                title.enabled(true);
                title.listen("click",
                    function() {
                        window.open(`/Home/Detail?regionName=${regionName}`);
                    }
                );
                title.listen("mouseOver",
                    function() {
                        setCursorByID("lineChart", "pointer");
                    }
                );
                title.listen("mouseOut",
                    function() {
                        setCursorByID("lineChart", "auto");
                    }
                );

                title.fontSize(20);
                title.fontFamily("Roboto-Light");
                chart.yAxis().enabled(true);
                chart.xAxis().labels();
                var dataSet = anychart.data.set(newData);

                // set the index for corresponding filter to use for create dataset mapping
                var mapValue = {
                    "Temperature": 1,
                    "Humidity": 2,
                    "Pressure": 3,
                    "Wind": 4
                };
                var firstSeriesData = dataSet.mapAs({ x: 0, value: mapValue[filter] });
                var series;
                if (filter == "Temperature")
                    series = chart.splineArea(firstSeriesData).fill(["#FFC3C3", "#990000"], 90);
                else if (filter == "Humidity")
                    series = chart.splineArea(firstSeriesData).fill(["#deebf7", "#3182bd"], 90);
                else if (filter == "Wind")
                    series = chart.splineArea(firstSeriesData).fill(["#C4DDFF", "#112B3C"], 90);
                else
                    series = chart.splineArea(firstSeriesData).fill(["#DAE5D0", "#B4E197"], 90);
                series.name("Time");
                series.labels().enabled(true).anchor("top").padding(10);
                series.labels().fontFamily("Roboto-Light");
                chart.container("lineChart");
                chart.draw();
            });
        }
    });
}

function setCursorByID(id, cursorStyle) {
    var elem;
    if (document.getElementById && (elem = document.getElementById(id))) {
        if (elem.style)
            elem.style.cursor = cursorStyle;
    }
}

// function get predict weathr forecast for the next 5 days
// Input: coordinate position of gps function
// Output: the array of 5 Objects
function getPredict(position) {
    if (position != null) {
        var lat = position.coords.latitude;
        var lon = position.coords.longitude;
    } else {
        var lat = "10.75";
        var lon = "106.666672";
    }
    $.ajax({
        type: "POST",
        url: "/api/Region/GetPredictWeatherData/",
        data: { "lat": lat, "lon": lon },
        success: function(result) {
            const superscript = "o";
            for (let i = 0; i < 5; i++) {
                const date = document.getElementById(`date${i + 1}`);
                const mean = document.getElementById(`mean${i + 1}`);
                const range = document.getElementById(`range${i + 1}`);
                date.innerHTML = result[i]["Date"];
                mean.innerHTML = parseInt(result[i]["MeanTemperature"]) + superscript.sup() + "C";
                range.innerHTML = parseInt(result[i]["LowerBoundTemperature"]) +
                    superscript.sup() +
                    " - " +
                    parseInt(result[i]["UpperBoundTemperature"]) +
                    superscript.sup();
            }
        },
        error: function() {
            alert("Failed to receive the Predict");
            console.log("Failed ");
        }
    });
}

// function when clicking to the city string of gps location frame
// Input: none
// Output: redirect to the location detail view page with the parameter as the location name.
function clickLocation() {
    window.open(`/Home/Detail?regionName=${regionName.innerHTML}`);
}