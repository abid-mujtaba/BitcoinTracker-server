"""
Implements a method for sending a GCM push to the specified Android device.
"""

import json
from urllib2 import Request, urlopen, URLError

import secrets


GCM_URL = "https://android.googleapis.com/gcm/send"


def send(data):
    """
    Method for sending a Push Notification via GCM.

    :param data: A python dictionary containing the payload to be sent via the Push Notification
    """

    headers = {'Content-Type': 'application/json', 'Authorization': 'key=' + secrets.API_KEY}

    payload = {
        "registration_ids": [secrets.DEV_REG_ID,],
        "data": data,
        "delay_while_idle": False,
        "time_to_live": 0,
    }

    jpayload = json.dumps(payload)

    try:
        request = Request(GCM_URL, jpayload, headers)
        response = urlopen(request)

        print("Response Code: {}".format(response.code))

        output = response.read()

        print("\nResponse: " + output)

    except URLError, e:

        print(e)
        print("Error while executing request to: " + GCM_URL)


if __name__ == '__main__':

    data = {"msg": "Hello, World"}

    send(data)