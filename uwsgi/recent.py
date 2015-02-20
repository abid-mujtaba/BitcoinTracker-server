import sqlite3

import common
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
        num = 12            # The default value of num when none is specified


    conn = sqlite3.connect('/home/abid/www/bitcoin/bitcoin.db')
    cursor = conn.cursor()

    records = []        # Construct a list of tuples with each tuple of the format (time, buy, sell)

    for values in cursor.execute('''SELECT "time", "buy", "sell" FROM "prices" ORDER BY "time" DESC LIMIT ?''', (num,)):

        t = values[0]
        buy = values[1]
        sell = values[2]

        ts = common.format_time(t)

        records.append((ts, buy, sell))

    template = common.get_template(__file__, 'recent.html')

    response = template.render({'rows': records}).encode("utf-8")

    conn.close()

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [response]