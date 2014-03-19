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

    // Access list of price points:
    var dArray = data['data'];

    // Iterate over list of price points and use extracted information to construct graph lists:
    for (var i in dArray) {             // The 'var i in dArray' structure causes 'i' to iterate over the indices of the list

        var datum = dArray[i];

        buy.push( [ datum['t'] * 1000, datum['b'] ] );
        sell.push( [ datum['t'] * 1000, datum['s'] ] );
    }


        // Create the chart
        $('#graph').highcharts('StockChart', {
            

            rangeSelector : {
                selected : 1,
                inputEnabled: $('#graph').width() > 480
            },

            title : {
                text : 'BTC Prices'
            },
            
            series : [{
                name : 'Buy',
                data : buy,
                tooltip: {
                    valueDecimals: 2
                }
            },
            {
                name : 'Sell',
                data: sell,
                tooltip: {
                    valueDecimals: 2
                }
            }]
        });
    });
});
