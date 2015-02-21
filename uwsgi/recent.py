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


    db = common.get_db()
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    records = []        # Construct a list of tuples with each tuple of the format (time, buy, sell)

    for values in cursor.execute('''SELECT "time", "buy", "sell" FROM "prices" ORDER BY "time" DESC LIMIT ?''', (num,)):

        t = values[0]
        buy = values[1]
        sell = values[2]

        ts = common.format_time(t)

        records.append({'time': ts, 'buy': buy, 'sell': sell})

    bi, si = maxima(records)          # get the indices of the maxima

    records[bi]['min_buy'] = True           # Append boolean values to the records corresponding to the maxima
    records[si]['max_sell'] = True

    template = common.get_template('recent.html')

    response = template.render({'rows': records}).encode("utf-8")

    conn.close()

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [response]


def maxima(records):
    """
    Calculate the indices of the records in the provided list with the min buy and max sell prices.

    :param records: List of dictionaries containing price information.
    :return: A tuple containing the indices for the records with min buy and max sell price in the input list.
    """

    bi = 0
    si = 0

    bmin = records[0]['buy']
    smax = records[0]['sell']

    for ii in range(1, len(records)):

        record = records[ii]

        if record['buy'] < bmin:

            bi = ii
            bmin = record['buy']

        if record['sell'] > smax:

            si = ii
            smax = record['sell']

    return bi, si