"""
Handles requests made to the /bitcoin/api/*/ end-point.
"""

import json
import sqlite3

import common
import current
import error


def handle_current(start_response, route):
    """
    Handler for the /bitcoin/api/current/ endpoint.

    Returns the current bitcoin price as JSON.
    """

    ts, buy, sell = current.fetch_current()

    response = json.dumps({'t': ts, 'b': buy, 's': sell})

    start_response('200 OK', [('Content-Type', 'application/json')])

    return [response]


def handle_since(start_response, route):
    """
    Handler for the /bitcoin/api/since/<timestamp>/ end-point.

    It returns JSON containing bitcoin price data since the timestamp specified.
    """

    if 'timestamp' in route:

        timestamp = int(route['timestamp'])

        if timestamp <= 0:        # Invalid number requested by user

            return error.handle(start_response, '400 Bad Request', "<i>timestamp</i> should be greater than 0.")

    else:

        return error.handle(start_response, '400 Bad Request', "<i>timestamp</i> not passed in URL.")

    db = common.get_db()
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    data = []

    for values in cursor.execute('''SELECT "time", "buy", "sell" FROM "prices" WHERE "time" > ?''', (timestamp,)):

        ts = values[0]
        buy = values[1]
        sell = values[2]

        data.append({'t': ts, 'b': buy, 's': sell})

    conn.close()

    response = json.dumps({'data': data})

    start_response('200 OK', [('Content-Type', 'application/json')])

    return [response]