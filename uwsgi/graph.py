"""
Handler for the /bitcoin/graph/ end-point.
"""

import common


def handle(start_response, route):

    template = common.get_template('graph.html')

    response = template.render().encode("utf-8")

    start_response('200 OK', [('Content-Type', 'text/html')])

    return [response]