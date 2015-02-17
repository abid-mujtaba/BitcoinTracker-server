import json
import urllib2


def fetch_price():
    """
    Fetch the current buy and sell price from bitstamp.

    :return: A dictionary of the current buy and sell prices.
    """

    url = "https://www.bitstamp.net/api/ticker/"

    response = json.load(urllib2.urlopen(url))

    return {"buy": response['ask'], "sell": response['bid']}