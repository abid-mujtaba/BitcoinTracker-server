$(function() {

    // Extend String class to have a format function to simplify string construction from variables  (Source: http://journalofasoftwaredev.wordpress.com/2011/10/30/replicating-string-format-in-javascript/)
    String.prototype.format = function()
    {
        var content = this;
    
        for (var i=0; i < arguments.length; i++)
        {
            var replacement = '{' + i + '}';
            content = content.replace(replacement, arguments[i]);  
        }    

        return content;
    };

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
    var data_url = 'http://www.abid-mujtaba.name:8080/bitcoin/api/sell/since/'.concat(threshold, '/');


    $.getJSON(data_url, function(data) {

    // We create lists to contain the graph data points. We will populate them below:
    var sell = [];
    var s_sma = [];
    var s_lma = [];
    var s_delta = [];

    // Access list of price points:
    var dArray = data['data'];

    // Iterate over list of price points and use extracted information to construct graph lists:
    for (var i in dArray) {             // The 'var i in dArray' structure causes 'i' to iterate over the indices of the list

        var datum = dArray[i];
        var time = datum['t'] * 1000;

        sell.push( [ time, datum['sell'] ] );
        s_sma.push( [ time, datum['s_sma'] ] );
        s_lma.push( [ time, datum['s_lma'] ] );
        s_delta.push( [ time, datum['s_delta'] ] );
    }

    // Fetch the current (latest) buy and sell prices and displays them in the header (top-right of the page) using CSS ids to access the relevant HTML elements

    var ii = sell.length - 1;        // Index of last element of array

    update_prices(sell[ii][1], s_sma[ii][1], s_lma[ii][1], s_delta[ii][1]);      // Update displayed data and document title with latest value
    update_title(sell[ii][1]);



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
            text : 'BTC Buy Prices'
        },

        // Specify the colors used by the data series.
        colors: [
            '#009922',
            '#ff0000',
            '#002299'
        ],

        series : [{
            name : 'Sell',
            data : sell,
            lineWidth: 1,
            marker: {
                enabled: true,
                radius: 2
            },
        },
        {
            name: 'SMA',
            data: s_sma,
            lineWidth: 1,
            enableMouseTracking: false,         // Stops including in tooltip
        },
        {
            name: 'LMA',
            data: s_lma,
            lineWidth: 1,
            enableMouseTracking: false,
        }],

        tooltip: { valueDecimals: 2 },

        });
    });


    // We setup a repeated function call every 1 minute to update the prices

    setInterval(function() {

        // We make an AJAX POST call to fetch the current price. We use POST here because POSTs are never cached.

        $.post("http://www.abid-mujtaba.name:8080/bitcoin/api/sell/current/", {}, function(data_string, status) {

            var data = JSON.parse(data_string);     // The GET call returns a string which we parse as a JSON object to get a dictionary.

            update_prices(data['sell'], data['s_sma'], data['s_lma'], data['s_delta']);        // Update Current Price header
            update_title(data['sell']);

            var chart = $('#graph').highcharts();           // Gain access to the chart object for modification

            var t = data['t'] * 1000;           // Convert time to milliseconds as required by HighCharts

            chart.series[0].addPoint([t, data['sell']], false);
            chart.series[1].addPoint([t, data['s_sma']], false);
            chart.series[2].addPoint([t, data['s_lma']], false);

            chart.redraw();         // Tell the chart to update itself
        });
    }, 1 * 60 * 1000);      // Set interval in milliseconds
});


function update_prices(buy, s_sma, s_lma, s_delta)       // Function that updates the header price information with the (float) values supplied
{
    $('#sell').text(" $" + buy.toFixed(2));
    $('#sma').text(" $" + s_sma.toFixed(2));
    $('#lma').text(" $" + s_lma.toFixed(2));
    $('#delta').text(" $" + s_delta.toFixed(2));
}


function update_title(sell)
{
    document.title = "Bitcoin: {0}".format(sell);
}