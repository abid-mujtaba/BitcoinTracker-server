from cgi import parse_qs
import os
import re
import routes
import sys
import wsgiref.util
#from urlparse import urlparse

# We start by appending the current folder to the system path to allow importing custom modules:
path = os.path.abspath(os.path.dirname(__file__))           # Append the absolute path of the current folder to the python path

if not path in sys.path:
    sys.path.insert(1, path)

del path


import current
import error
import recent

# We define the valid routes of the bitcoin uwsgi application using "routes":
router = routes.Mapper()

router.connect(None, '/bitcoin/recent/', handler = recent.handle)
router.connect(None, R'/bitcoin/recent/{num:\d+}/', handler = recent.handle)
router.connect(None, '/bitcoin/current/', handler = current.handle)


def application(env, start_response):

    # We extract the URL of the request made to this server:
    base_uri = wsgiref.util.application_uri(env)[:-1]           # We strip off the trailing / since we will need it to be part of the url we extract
    full_uri = wsgiref.util.request_uri(env)

    m = re.match(base_uri + "(/.*)", full_uri)

    if m:

        url = m.group(1)            # The extracted url with the domain part removed. It is now in a form that routes can use
        route = router.match(url)       # We use the router to match the url to the connections established earlier

        if route:           # A route matching the incoming URL exists. We use its handler function

            return route['handler'](start_response, route)

        else:

            return error.handle(start_response, '400 Bad Request', "Invalid path.")

    else:

        return error.handle(start_response, '400 Bad Request', "Regex extraction from full URI failed.")
