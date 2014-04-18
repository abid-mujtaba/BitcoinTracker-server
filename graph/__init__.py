# Author: Abid H. Mujtaba
# Date: 2014-03-14
#
# This script handles the /bitcoin/recent/ end-point, fetching data from the sqlite3 database.

from datetime import datetime
import jinja2
import json
import os
import sqlite3
import time
import urllib2


def handle(start_response, route):
    """
    We pass in the function "start_response" which when called triggers the start of the response.
    """
    return base_handle(start_response, route, 'graph.html')


def handle_buy(start_response, route):
    """
    Handles the /graph/buy/ end-point.
    """
    return base_handle(start_response, route, 'graph_buy.html')


def handle_sell(start_response, route):
    """
    Handles the /graph/sell/ end-point.
    """
    return base_handle(start_response, route, 'graph_sell.html')


def base_handle(start_response, route, template_filename):
    """
    Generic handler for all graph requests. It is passed the template_filename it is supposed to use for rendering.
    """
    
    # Load the jinja2 template in preparation for rendering:
    templateLoader = jinja2.FileSystemLoader( searchpath="/" )      # We specify that we will be using absolute paths to specify the location of the template file
    templateEnv = jinja2.Environment( loader=templateLoader )

    TEMPLATE_FILE = os.path.join( os.path.dirname(__file__), template_filename)

    template = templateEnv.get_template( TEMPLATE_FILE )         # Load template from filesystem

    response = template.render().encode("utf-8")          # jinja2 template renderer returns unicode so we explicitly encode it as utf-8 before returning it so that the browser can read it.

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [response] 

