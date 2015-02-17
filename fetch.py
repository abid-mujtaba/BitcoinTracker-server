"""
Fetches the current price from the bitstamp ticker and stores it in the sqlite3 database.
"""

import client
import settings

from datetime import datetime
import sqlite3
import sys
import time


def main():

    data = client.fetch_price()
    buy = data['buy']
    sell = data['sell']

    now = int(time.time())          # The current time as of this fetch

    if len(sys.argv) > 1 and sys.argv[1] == '--insert':     # Insertion only occurs if the --insert switch is specified

        conn = sqlite3.connect(settings.db())
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO "prices" ("time", "buy", "sell") VALUES (?, ?, ?)''', (now, buy, sell))

        conn.commit()
        conn.close()

    else:       # If --insert is not specified we simply print the current price info to the terminal

        ts = datetime.fromtimestamp(now).strftime("%H:%M:%S")

        print("{} :-  Buy: {} - Sell: {}".format(ts, buy, sell))




if __name__ == '__main__':

    main()