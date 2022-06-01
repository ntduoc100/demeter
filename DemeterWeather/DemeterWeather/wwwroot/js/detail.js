var regionName;
var anyChartRegionId;

$(document).ready(function() {
    regionName = document.getElementById("regionNameDetail").innerHTML;
    regionName = regionName.trim();
    $.ajax({
        type: "POST",
        url: "/api/Region/GetAnyChartRegionId/",
        data: { "regionName": regionName },
        success: function(result) {
            anyChartRegionId = result;
            updateLineChartDetail();
        }
    });
});

function updateLineChartDetail() {
    var filter = document.querySelector('input[name="filtersDetail"]:checked').value;
    document.getElementById("detailLineChart").innerHTML = "";

    $.ajax({
        type: "POST",
        url: "/api/Chart/GetLineChartData/",
        data: { "anyChartRegionId": anyChartRegionId },
        success: function(result) {
            anychart.onDocumentReady(function() {
                result = result.sort(function(data1, data2) {
                    return (`${data1["time"]}`).localeCompare(data2["time"]);
                });

                // Convert data to 2d array
                var newData = [];
                for (let i = 0; i < 20; i++) {
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
                var title = chart.title();
                title.text(`Predicted ${filter} for ${result[0]["RegionName"]}`);
                title.fontSize(20);
                title.fontFamily("Roboto-Light");
                chart.title().enabled(true);
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
                chart.container("detailLineChart");
                chart.draw();
            });
        }
    });
}