# Author: Abid H. Mujtaba
# Date: 2014-03-29
#
# This script handles the /bitcoin/api/current/ API end-point, fetching the latest data from the sqlite3 database.

import json
import sqlite3


def handle(start_response, route):
    """
    We pass in the function "start_response" which when called triggers the start of the response.
    """

    conn = sqlite3.connect('/home/ubuntu/public_html/uwsgi/bitcoin/data.db')
    cursor = conn.cursor()

    #data = []

    # We query the database for all data-points recorded after the specified timestamp.
    values = cursor.execute('''SELECT "time", "buy", "sell", "wa_buy", "wa_sell" FROM "prices" ORDER BY "time" DESC LIMIT 1''').fetchone()

    conn.close()

    ts = values[0]                  # ts: timestamp
    buy = values[1]
    sell = values[2]
    wbuy = values[3]
    wsell = values[4]

    data = {'t': ts, 'b': buy, 's': sell, 'wb': wbuy, 'ws': wsell}

    response = json.dumps(data)

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [response]