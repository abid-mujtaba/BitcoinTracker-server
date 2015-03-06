# This script handles the /bitcoin/recent/ end-point, fetching data from the sqlite3 database.

import json
import time
import urllib2

import common


TICKER_URL = "https://www.bitstamp.net/api/ticker/"


def handle(start_response, route):
    """
    We pass in the function "start_response" which when called triggers the start of the response.
    """

    t, buy, sell = fetch_current()

    ts = common.format_time(t)          # Convert time integer to string

    template = common.get_template('current.html')

    data = {"time": ts, "buy": buy, "sell": sell}       # Create dictionary of variables to be substituted

    response = template.render(data).encode("utf-8")          # jinja2 template renderer returns unicode so we explicitly encode it as utf-8 before returning it so that the browser can read it.

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [response]


def fetch_current():
    """
    Fetch the current bitcoin price.

    :return: A tuple consisting of the (timestamp, buy, sell)
    """

    data = json.load(urllib2.urlopen(TICKER_URL))

    buy = float(data["ask"])
    sell = float(data["bid"])

    now = int(time.time())        # Get current unix time

    return now, buy, sell