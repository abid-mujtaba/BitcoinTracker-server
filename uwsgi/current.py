# This script handles the /bitcoin/recent/ end-point, fetching data from the sqlite3 database.

import jinja2
import json
import os
import time
import urllib2

import common


TICKER_URL = "https://www.bitstamp.net/api/ticker/"


def handle(start_response, route):
    """
    We pass in the function "start_response" which when called triggers the start of the response.
    """

    data = json.load(urllib2.urlopen(TICKER_URL))

    buy = float(data["ask"])
    sell = float(data["bid"])

    now = int(time.time())        # Get current unix time

    ts = common.format_time(now)

    # Load the jinja2 template in preparation for rendering:
    templateLoader = jinja2.FileSystemLoader( searchpath="/" )      # We specify that we will be using absolute paths to specify the location of the template file
    templateEnv = jinja2.Environment( loader=templateLoader )

    parent = common.get_parent_dir(__file__)      # Get absolute path of parent directory of current directory

    TEMPLATE_FILE = os.path.join(parent, 'templates/current.html')

    template = templateEnv.get_template( TEMPLATE_FILE )         # Load template from filesystem

    vars = {"time": ts, "buy": buy, "sell": sell}       # Create dictionary of variables to be substituted
    response = template.render( vars ).encode("utf-8")          # jinja2 template renderer returns unicode so we explicitly encode it as utf-8 before returning it so that the browser can read it.

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [response]