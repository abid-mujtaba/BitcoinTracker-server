var flag_title_buy = false;
var gbuy, gsell;


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

    // Fetch the current price and show it in the header
    fetch_current_price();

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


/*
    $.getJSON(data_url, function(data) {

    // We create lists to contain the graph data points. We will populate them below:
    var buy = [];
    var sell = [];

    // Access list of price points:
    var dArray = data['data'];

    // Iterate over list of price points and use extracted information to construct graph lists:
    for (var i in dArray) {             // The 'var i in dArray' structure causes 'i' to iterate over the indices of the list

        var datum = dArray[i];
        var time = datum['t'] * 1000;

        buy.push( [ time, datum['b'] ] );
        sell.push( [ time, datum['s'] ] );
    }

    // Fetch the current (latest) buy and sell prices and displays them in the header (top-right of the page) using CSS ids to access the relevant HTML elements

    var cbuy = buy[buy.length-1][1];        // Get last buy and sell prices
    var csell = sell[sell.length-1][1]

    update_prices(cbuy, csell);
    update_title(cbuy, csell);              // We update the document title to display the latest sell price

    gbuy = cbuy;         // Store the latest prices globally (used for changing document title)
    gsell = csell;



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

        // Move y-axis to the opposite (right) side and shifts if slightly more right to keep it off the chart
        yAxis: {
            opposite: true,
            offset: 30,
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
        }],

        tooltip: { valueDecimals: 2 },

        });
    });
*/


    // We setup a repeated function call every 1 minute to update the prices

    setInterval(function() {

        // We make an AJAX POST call to fetch the current price. We use POST here because POSTs are never cached.
        fetch_current_price();

    }, 1 * 60 * 1000);      // Set interval in milliseconds


    // We set up callbacks for clicking the current buy and sell price, using these to change the price displayed in the document title
    $('#buy').click(function() {

        flag_title_buy = true;          // Set the flag to indicate that the buy price is to be displayed
        update_title(gbuy, gsell);      // Update the title using the global buy and sell prices to make the change
    });

    $('#sell').click(function() {

        flag_title_buy = false;
        update_title(gbuy, gsell);
    });

});


function fetch_current_price()
{
    $.post("https://marzipan.whatbox.ca:3983/bitcoin/api/current/", {}, function(data, status) {

    update_prices(data['b'], data['s']);        // Update Current Price header
    update_title(data['b'], data['s']);
    });
}


function update_prices(buy, sell)       // Function that updates the header price information with the (float) values supplied
{
    $('#buy').text(" $" + buy.toFixed(2));
    $('#sell').text(" $" + sell.toFixed(2));

    gbuy = buy;         // Store the latest buy and sell prices globally
    gsell = sell;
}


function update_title(buy, sell)
{
    if (flag_title_buy)
    {
        document.title = "Bitcoin: {0}".format(buy);
    }
    else
    {
        document.title = "Bitcoin: {0}".format(sell);
    }
}