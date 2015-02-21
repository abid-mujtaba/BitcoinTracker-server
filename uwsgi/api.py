"""
Handles requests made to the /bitcoin/api/*/ end-point.
"""

import json

import current


def handle_current(start_response, route):

    ts, buy, sell = current.fetch_current()

    response = json.dumps({'b': buy, 's': sell})

    start_response('200 OK', [('Content-Type', 'application/json')])

    return [response]