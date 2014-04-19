# Author: Abid H. Mujtaba
# Date: 2014-04-18
#
# This script handles the /bitcoin/api/buy/current/ API end-point, fetching the latest buy data from the sqlite3 database.

import json
import sqlite3

from bitcoin import DB_PATH


def handle(start_response, route):
    """
    We pass in the function "start_response" which when called triggers the start of the response.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #data = []

    # We query the database for all data-points recorded after the specified timestamp.
    values = cursor.execute('''SELECT P."time", "buy", "b_sma", "b_lma", "b_delta" FROM "prices" AS P JOIN "averages" AS A ON P."time" = A."time" ORDER BY P."time" DESC LIMIT 1''').fetchone()

    conn.close()

    ts = values[0]                  # ts: timestamp
    buy = values[1]
    b_sma = values[2]
    b_lma = values[3]
    b_delta = values[4]

    data = {'t': ts, 'buy': buy, 'b_sma': b_sma, 'b_lma': b_lma, 'b_delta': b_delta }

    response = json.dumps(data)

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [response]