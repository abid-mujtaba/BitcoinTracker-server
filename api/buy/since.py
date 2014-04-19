# Author: Abid H. Mujtaba
# Date: 2014-04-18
#
# This script handles the /bitcoin/api/buy/since/{num}/ API end-point, fetching buy data from the sqlite3 database.

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
    for values in cursor.execute('''SELECT P."time", "buy", "b_sma", "b_lma", "b_delta" FROM "prices" AS P JOIN "averages" AS A ON P."time" = A."time" WHERE P."time" > ?''', (timestamp,)):

        ts = values[0]                  # ts: timestamp
        buy = values[1]
        b_sma = values[2]
        b_lma = values[3]
        b_delta = values[4]

        data.append({'t': ts, 'buy': buy, 'b_sma': b_sma, 'b_lma': b_lma, 'b_delta': b_delta})

    conn.close()

    response = json.dumps({'data': data})

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [response]