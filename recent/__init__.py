# Author: Abid H. Mujtaba
# Date: 2014-03-14
#
# This script handles the /bitcoin/recent/ end-point, fetching data from the sqlite3 database.

from datetime import datetime
import json
import sqlite3
import time
import urllib2

import error


def handle(start_response, route):
    """
    We pass in the function "start_response" which when called triggers the start of the response.
    """

    if 'num' in route:

        num = int(route['num'])
        
        if num <= 0:        # Invalid number requested by user

            return error.handle(start_response, '400 Bad Request', "<i>num</i> should be greater than 0.")

    else:

        num = 10            # The default value of num when none is specified


    conn = sqlite3.connect('/home/ubuntu/public_html/uwsgi/bitcoin/data.db')
    cursor = conn.cursor()

    response = "</br>"

    for values in cursor.execute('''SELECT "time", "buy", "sell" FROM "prices" ORDER BY "time" DESC LIMIT ?''', (num,)):

        timestamp = values[0]
        buy = values[1]
        sell = values[2]

        timestring = datetime.fromtimestamp(timestamp).strftime('%H:%M')

        response += "<p>{} - ${:.2f} - ${:.2f}</p>\n".format(timestring, buy, sell)

    conn.close()

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [response] 
