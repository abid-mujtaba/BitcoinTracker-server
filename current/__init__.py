# Author: Abid H. Mujtaba
# Date: 2014-03-14
#
# This script handles the /bitcoin/recent/ end-point, fetching data from the sqlite3 database.

from datetime import datetime
import json
import sqlite3
import time
import urllib2


TICKER_URL = "https://www.bitstamp.net/api/ticker/"


def handle(start_response, route):
    """
    We pass in the function "start_response" which when called triggers the start of the response.
    """

    data = json.load(urllib2.urlopen(TICKER_URL))

    buy = float(data["ask"])
    sell = float(data["bid"])

    now = int(time.time())        # Get current unix time
    timestring = datetime.fromtimestamp(now).strftime('%H:%M')


    response = """<!DOCTYPE HTML>
                  <head>
                    <link rel="stylesheet" type="text/css" href="../static/css/styles.css"/>
                  </head>
                  <body>
                    </br>
                    <p><b>Current Price:</b> {} - ${:.2f} - ${:.2f}</p>
                    </br>
                  </body>""".format(timestring, buy, sell)

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [response] 
