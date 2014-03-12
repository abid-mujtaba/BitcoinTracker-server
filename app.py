from cgi import parse_qs


def application(env, start_response):

    d = parse_qs(env['QUERY_STRING'])    

    if any( [k in d for k in ['s', 'l']] ):

        response = str(d)
            
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [response]

    else:

        start_response('400 Bad Request', [('Content-Type', 'text/html')])
        return ["<h1>ERROR: 400 Bad Request</h1><p><i>Reason:</i> Only 's' (prices since timestamp) and 'l' (last interval of prices) are allowed as GET parameters.</p>"]
