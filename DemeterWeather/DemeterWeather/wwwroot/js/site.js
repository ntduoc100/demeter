$(document).ready(function() {
    $("#searchBar").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/api/Region/Search/",
                data: { "text": request.term },
                type: "POST",
                success: function(data) {
                    response($.map(data,
                        function(item) {
                            return item["RegionName"];
                        }));
                },
                error: function(resp) {
                    alert(resp.responseText);
                },
                failure: function(resp) {
                    alert(resp.responseText);
                }
            });
        },
    });
});

// Function to create a realtime clock at the navigation bar
// Input: none
// Output: draw a clock on nav bar by id
function realtimeClock() {
    var rtClock = new Date();
    var hours = rtClock.getHours();
    var minutes = rtClock.getMinutes();
    var seconds = rtClock.getSeconds();

    var amPm = (hours < 12) ? "AM" : "PM";

    hours = (hours > 12) ? hours - 12 : hours;

    // Add zero digit to front of variable and take the last 2 digits to create the hour/minute/second
    hours = (`0${hours}`).slice(-2);
    minutes = (`0${minutes}`).slice(-2);
    seconds = (`0${seconds}`).slice(-2);

    document.getElementById("clock").innerHTML = hours + " : " + minutes + " : " + seconds + " " + amPm;
    var t = setTimeout(realtimeClock, 500);
}


// function to set the loading image to invisible
function setImageVisible() {
    document.getElementById("loading-image").remove();
    document.getElementById("loading").remove();
}