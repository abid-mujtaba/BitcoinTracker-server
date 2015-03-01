"""
Fetches the current price from the bitstamp ticker and stores it in the sqlite3 database.
"""

import client
import rules
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

    if '--insert' in sys.argv[1:]:     # Insertion only occurs if the --insert switch is specified

        conn = sqlite3.connect(settings.db())
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO "prices" ("time", "buy", "sell") VALUES (?, ?, ?)''', (now, buy, sell))

        conn.commit()
        conn.close()

    else:       # If --insert is not specified we simply print the current price info to the terminal

        ts = datetime.fromtimestamp(now).strftime("%H:%M:%S")

        print("{} :-  Buy: {} - Sell: {}".format(ts, buy, sell))

    # If the --rules switch is specified we execute all the rules specified
    if '--rules' in sys.argv[1:]:

        for rule in rules.RULES:

            rule.execute(float(buy), float(sell))



if __name__ == '__main__':

    main()