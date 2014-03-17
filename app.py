from cgi import parse_qs
import os
import sys
import wsgiref.util
#from urlparse import urlparse

# We start by appending the current folder to the system path to allow importing custom modules:
path = os.path.abspath(os.path.dirname(__file__))           # Append the absolute path of the current folder to the python path

if not path in sys.path:
    sys.path.insert(1, path)

del path


import recent


def application(env, start_response):

    return recent.handle(env, start_response)
    #d = parse_qs(env['QUERY_STRING'])    

    #response = "<p>Request URI: %s - %s</p>" % (wsgiref.util.request_uri(env, include_query=False), wsgiref.util.application_uri(env))

    #if any( [k in d for k in ['s', 'l']] ):

        #response += str(d)
            
        #start_response('200 OK', [('Content-Type', 'text/html')])
        #return [response]

    #else:

        #start_response('400 Bad Request', [('Content-Type', 'text/html')])
        #return [response + "<h1>ERROR: 400 Bad Request</h1><p><i>Reason:</i> Only 's' (prices since timestamp) and 'l' (last interval of prices) are allowed as GET parameters.</p>"]
