$(function() {

    // We force Highcharts to use local time for the time-axis:
    Highcharts.setOptions({
        global: {
            useUTC: false
        }
    });


    // We get the current time in milliseconds and convert it to seconds
    var now = Math.floor( (new Date).getTime() / 1000 );

    // We calculate the timestamp for 2 days ago which is how long we want the graph to cover:
    var threshold = now - (86400 * 2);

    // Construct the URL that will fetch the price data.
    var data_url = 'http://www.abid-mujtaba.name:8080/bitcoin/api/since/'.concat(threshold, '/');


    $.getJSON(data_url, function(data) {

    // We create lists to contain the graph data points. We will populate them below:
    var buy = [];
    var sell = [];
    var wbuy = [];
    var wsell = [];

    // Access list of price points:
    var dArray = data['data'];

    // Iterate over list of price points and use extracted information to construct graph lists:
    for (var i in dArray) {             // The 'var i in dArray' structure causes 'i' to iterate over the indices of the list

        var datum = dArray[i];
        var time = datum['t'] * 1000;

        buy.push( [ time, datum['b'] ] );
        sell.push( [ time, datum['s'] ] );
        wbuy.push( [ time, datum['wb'] ] );
        wsell.push( [ time, datum['ws'] ] );
    }

    // Fetch the current (latest) buy and sell prices and displays them in the header (top-right of the page) using CSS ids to access the relevant HTML elements

    update_prices(buy[buy.length-1][1], sell[sell.length - 1][1]);


        // Create the chart
        $('#graph').highcharts('StockChart', {

            rangeSelector : {

                buttons: [{
                    type: 'minute',
                    count: 60,
                    text: '1h'
                }, {
                    type: 'minute',
                    count: 120,
                    text: '2h'
                }, {
                    type: 'minute',
                    count: 360,
                    text: '6h'
                }, {
                    type: 'minute',
                    count: 720,
                    text: '12h'
                }, {
                    type: 'day',
                    count: 1,
                    text: '1d'
                }, {
                    type: 'all',
                    text: 'All'
                }],

                selected : 2,       // Index of 'buttons' array to specify which range to use initially
                inputEnabled: true,

            },

            title : {
                text : 'BTC Prices'
            },
            
            // Specify the colors used by the data series.
            colors: [
                '#ff0000',
                '#009922',
                '#ff0000',
                '#009922'
            ],
            
            series : [{
                name : 'Buy',
                data : buy,
                lineWidth: 1,
                marker: {
                    enabled: true,
                    radius: 2
                },
            },
            {
                name : 'Sell',
                data: sell,
                lineWidth: 1,
                marker: {
                    enabled: true,
                    radius: 2
                },
            },
            {
                name: 'W. Buy',
                data: wbuy,
                enableMouseTracking: false,         // Stops including in tooltip
            },
            {
                name: 'W. Sell',
                data: wsell,
                enableMouseTracking: false,
            }],

            tooltip: { valueDecimals: 2 },
        });
    });


    // We setup a repeated function call every 1 minute to update the prices

    setInterval(function() {

        // We make an AJAX POST call to fetch the current price. We use POST here because POSTs are never cached.

        $.post("http://www.abid-mujtaba.name:8080/bitcoin/api/current/", {}, function(data_string, status) {

            var data = JSON.parse(data_string);     // The GET call returns a string which we parse as a JSON object to get a dictionary.

            update_prices(data['b'], data['s']);        // Update Current Price header

            var chart = $('#graph').highcharts();           // Gain access to the chart object for modification

            var t = data['t'] * 1000;           // Convert time to milliseconds as required by HighCharts

            chart.series[0].addPoint([t, data['b']], false);
            chart.series[1].addPoint([t, data['s']], false);
            chart.series[2].addPoint([t, data['wb']], false);
            chart.series[3].addPoint([t, data['ws']], false);

            chart.redraw();         // Tell the chart to update itself
        });
    }, 1 * 60 * 1000);      // Set interval in milliseconds

});


function update_prices(buy, sell)       // Function that updates the header price information with the (float) values supplied
{
    $('#buy').text(" $" + buy.toFixed(2));
    $('#sell').text(" $" + sell.toFixed(2));
}