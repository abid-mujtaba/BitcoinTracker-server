# This script is used to generate an error page to indicate to the user that an error has occurred.


def handle(start_response, status_code, error_message):

    start_response(status_code, [('Content-Type', 'text/html')])

    return ["<h1>ERROR: {}</h1><p><i>Reason:</i> {}</p>".format(status_code, error_message)]
