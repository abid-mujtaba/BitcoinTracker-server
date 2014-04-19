# Author: Abid H. Mujtaba
# Date: 2014-04-18
#
# This script handles the /bitcoin/api/sell/since/{num}/ API end-point, fetching sell data from the sqlite3 database.

import json
import sqlite3

from bitcoin import DB_PATH, error


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


    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    data = []

    # We query the database for all data-points recorded after the specified timestamp.
    for values in cursor.execute('''SELECT P."time", "sell", "s_sma", "s_lma", "s_delta" FROM "prices" AS P JOIN "averages" AS A ON P."time" = A."time" WHERE P."time" > ?''', (timestamp,)):

        ts = values[0]                  # ts: timestamp
        sell = values[1]
        s_sma = values[2]
        s_lma = values[3]
        s_delta = values[4]

        data.append({'t': ts, 'sell': sell, 's_sma': s_sma, 's_lma': s_lma, 's_delta': s_delta})

    conn.close()

    response = json.dumps({'data': data})

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [response]