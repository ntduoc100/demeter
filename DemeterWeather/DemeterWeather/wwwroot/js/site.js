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
            humidity.innerHTML = 'Humidity: ' + stringify['humidity'] + '%';
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
            window.open('/Locations?locationName=' + strNew);
        },
        error: function () {
            alert('Failed to receive the Location');
            console.log('Failed ');
        }
    })
}

function update() {
    var select = document.getElementById('filters');
    var value = select.options[select.selectedIndex].value;
    document.getElementById("container").innerHTML = "";
    $.ajax({
        type: "POST",
        url: '/Home/ChartInformationList/',
        data: { filter: value },
        success: function (result) {
            let myString = JSON.stringify(result);
            var stringify = JSON.parse(myString);
            for (var i = 0; i < stringify.length; i++) {
                result.push({ "id": stringify[i]['id'], "value": parseInt(stringify[i]['value']) });
            }

            anychart.onDocumentReady(function () {
                var map = anychart.map();
                var dataSet = anychart.data.set(result);
                series = map.choropleth(dataSet);

                series.geoIdField('id');

                series.colorScale(anychart.scales.linearColor('#deebf7', '#3182bd'));
                series.hovered().fill('#addd8e');

                // https://cdn.anychart.com/#maps-collection
                map.title("Realtime Map with " + value);
                map.geoData(anychart.maps['vietnam']);

                map.container('container');

                map.draw();

                map.listen("pointDblClick", function (e) {
                    chartPlaceId = e.point.get("id");
                });
            });
        }
    });
}

function lineChart() {
    document.getElementById("lineChart").innerHTML = "";
    $.ajax({
        type: "POST",
        url: '/Home/LineChartInformationList/',
        data: { chartPlaceId: chartPlaceId },
        success: function (result) {
            let myString = JSON.stringify(result);
            var stringify = JSON.parse(myString);
            anychart.onDocumentReady(function () {
                var newData = []
                for (let i = 0; i < stringify.length; i++) {
                    newData[i] = [
                        stringify[i].time.slice(11, 16),
                        Number(stringify[i].temperature),
                        Number(stringify[i].humidity),
                        Number(stringify[i].pressure),
                        Number(stringify[i].wind),
                    ]
                }

                var mostRecentPredictedTime = Number(stringify[0]['time'].slice(11, 13))
                for (let i = 0; i < mostRecentPredictedTime; i += 3) {
                    var tmp_hour;
                    if (i < 10) {
                        tmp_hour = '0' + i + ':00'
                    } else {
                        tmp_hour = i + ':00'
                    }
                    newData.unshift([tmp_hour, 'N/A', 'N/A', 'N/A', 'N/A'])
                }

                var chart = anychart.area();

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
                chart.title(stringify[0].place
                    + ', Day ' + stringify[0].time.slice(8, 10)
                    + ' Month ' + stringify[0].time.slice(5, 7)
                    + ' Year ' + stringify[0].time.slice(0, 4));
                chart.yAxis().enabled(true);
                //var dataSet = anychart.data.set(newData);
                var dataSet = anychart.data.set(newData.map(function (x) { return [x[0], x[1]] }));
                //var firstSeriesData = dataSet.mapAs({ x: 0, value: 1 });
                var firstSeriesData = dataSet;
                var series;
                series = chart.splineArea(firstSeriesData).fill("#5DF8FD");
                series.name('Time');
                series.labels().enabled(true).anchor('top').padding(10).fontSize('15');
                series.markers(false);
                chart.container('lineChart');

                chart.draw();
            });
        }
    });
}
