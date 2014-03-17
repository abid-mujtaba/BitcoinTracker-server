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


def handle(env, start_response):
    """
    We pass in the environment that comes in with the HTTP Request and a function "start_response" which when called triggers the start of the response.
    """

    data = json.load(urllib2.urlopen(TICKER_URL))

    buy = float(data["ask"])
    sell = float(data["bid"])

    now = int(time.time())        # Get current unix time
    timestring = datetime.fromtimestamp(now).strftime('%H:%M')


    response = "</br>\n<p><b>Current Price:</b> {} - ${:.2f} - ${:.2f}</p>\n</br>\n".format(timestring, buy, sell)

    conn = sqlite3.connect('/home/ubuntu/public_html/uwsgi/bitcoin/data.db')
    cursor = conn.cursor()

    for values in cursor.execute('''SELECT "time", "buy", "sell" FROM "prices" ORDER BY "time" DESC LIMIT 10'''):

        timestamp = values[0]
        buy = values[1]
        sell = values[2]

        timestring = datetime.fromtimestamp(timestamp).strftime('%H:%M')

        response += "<p>{} - ${:.2f} - ${:.2f}</p>\n".format(timestring, buy, sell)

    conn.close()

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [response] 
