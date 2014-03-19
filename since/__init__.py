# Author: Abid H. Mujtaba
# Date: 2014-03-14
#
# This script handles the /bitcoin/api/since/{num}/ API end-point, fetching data from the sqlite3 database.

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

    if 'timestamp' in route:

        timestamp = int(route['timestamp'])

        if timestamp <= 0:        # Invalid number requested by user

            return error.handle(start_response, '400 Bad Request', "<i>timestamp</i> should be greater than 0.")

    else:

        return error.handle(start_response, '400 Bad Request', "<i>timestamp</i> not passed in URL.")


    conn = sqlite3.connect('/home/ubuntu/public_html/uwsgi/bitcoin/data.db')
    cursor = conn.cursor()

    data = []

    # We query the database for all data-points recorded after the specified timestamp.
    for values in cursor.execute('''SELECT "time", "buy", "sell" FROM "prices" WHERE "time" > ?''', (timestamp,)):

        ts = values[0]                  # ts: timestamp
        buy = values[1]
        sell = values[2]

        data.append({'t': ts, 'b': buy, 's': sell})

    conn.close()

    response = json.dumps({'data': data})

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [response] 
