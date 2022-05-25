anychart.onDocumentReady(function () {

    // var predictData = getData()
    // var predictData = $.ajax(
    //     {
    //         url: "",
    //         type: "GET",
    //         data: {},
    //     }
    // ).done(function (json) {
    //     var max = json.data.length;
    //     var data = [];
    //     for (let i = 0; i < max; i++) {
    //         var t = json.data[i];
    //         data[i] = {
    //             "Time": t["Time"],
    //             "Temperature": t["Temperature"],
    //             "Wind": t["Wind"],
    //             "Humidity": t["Humidity"],
    //             "Pressure": t["Pressure"],
    //         };

    //     }
    // })

    var predictData = [
        {
            "Time": "2022-05-25T00:00:00",
            "Temperature": 28.4,
            "Wind": 0.8,
            "Humidity": 64.5,
            "Pressure": 1008.7,
            "Place": "Ho Chi Minh city"
        },
        {
            "Time": "2022-05-25T06:00:00",
            "Temperature": 27.3,
            "Wind": 0.7,
            "Humidity": 64.5,
            "Pressure": 1008.7,
            "Place": "Ho Chi Minh city"
        },
        {
            "Time": "2022-05-25T03:00:00",
            "Temperature": 30.5,
            "Wind": 0.5,
            "Humidity": 64.5,
            "Pressure": 1008.7,
            "Place": "Ho Chi Minh city"
        },
        {
            "Time": "2022-05-25T12:00:00",
            "Temperature": 29.5,
            "Wind": 0.8,
            "Humidity": 64.5,
            "Pressure": 1008.7,
            "Place": "Ho Chi Minh city"
        },
        {
            "Time": "2022-05-25T09:00:00",
            "Temperature": 31.2,
            "Wind": 0.9,
            "Humidity": 64.5,
            "Pressure": 1008.7,
            "Place": "Ho Chi Minh city"
        },
        {
            "Time": "2022-05-25T18:00:00",
            "Temperature": 31.2,
            "Wind": 0.9,
            "Humidity": 64.5,
            "Pressure": 1008.7,
            "Place": "Ho Chi Minh city"
        },
        {
            "Time": "2022-05-25T15:00:00",
            "Temperature": 33.0,
            "Wind": 0.9,
            "Humidity": 64.5,
            "Pressure": 1008.7,
            "Place": "Ho Chi Minh city"
        },
        {
            "Time": "2022-05-25T21:00:00",
            "Temperature": 26.0,
            "Wind": 0.2,
            "Humidity": 64.5,
            "Pressure": 1008.7,
            "Place": "Ho Chi Minh city"
        },
    ]
    // Sort data
    var sortedWeatherData = predictData.sort(function (data1, data2) {
        return ('' + data1["Time"]).localeCompare(data2["Time"]);
    })
    // Convert data
    var newData = []
    for (let i = 0; i < predictData.length; i++) {
        newData[i] = [
            sortedWeatherData[i].Time.slice(11, 16),
            sortedWeatherData[i].Temperature,
            sortedWeatherData[i].Humidity,
            sortedWeatherData[i].Pressure,
            sortedWeatherData[i].Wind
        ]
    }
    // create area chart
    var chart = anychart.area();

    // tooltip
    var tooltip = chart.tooltip()
    tooltip.format(function (e) {
        // return newData[1].indexOf(this.value)
        return "Temperature: " + newData[this.index][1]
            + "\nHumidity: " + newData[this.index][2]
            + "\nPressure: " + newData[this.index][3]
            + "\nWind: " + newData[this.index][4]
    })


    // set background
    chart.background().fill("#284c5c")
    // set chart padding
    chart.padding([20, 20, 20, 20]);

    // turn on chart animation
    chart.animation(true);

    // turn off the crosshair
    chart.crosshair(false);

    // set chart title text settings
    // var title = chart.title('Ngày ' + predictData[0].Time.slice(8, 10)
    //     + ' Tháng ' + predictData[0].Time.slice(5, 7)
    //     + ' Năm ' + predictData[0].Time.slice(0, 4)
    // );
    chart.title().enabled(false)
    
    
    // remove y axis
    chart.yAxis().enabled(false);
    chart.xAxis().labels().fontColor('White')

    // create data set on our data,also we can pud data directly to series
    var dataSet = anychart.data.set(newData);

    // map data for the first series,take value from first column of data set
    var firstSeriesData = dataSet.mapAs({ x: 0, value: 1 });

    // temp variable to store series instance
    var series;

    // setup first series
    series = chart.splineArea(firstSeriesData).fill(['#206F91','#86C7E2'], 90);
    series.name('Time');
    // enable series data labels
    series.labels().enabled(true).anchor('top').padding(10).fontColor('White');
    // enable series markers
    series.markers(true);

    // turn the legend on
    // chart.legend().enabled(true).fontSize(13).padding([0, 0, 20, 0]);

    // set container for the chart and define padding
    chart.container('container');
    // initiate chart drawing
    chart.draw();
});   