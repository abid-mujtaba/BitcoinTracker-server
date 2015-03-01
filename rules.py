"""
We define rules here which depend upon the bitcoin prices and carry out certain actions if conditions are met.
"""

import gcm
import secrets


class Rule:
    """
    A class for analyzing the bitcoin prices and carrying out specified actions when conditions are met.
    """

    def execute(self, buy, sell):

        if self.trigger(buy, sell):

            self.action(buy, sell)

    @staticmethod
    def send(msg):
        """
        Static method for sending a payload via GCM.

        :param msg: The string that is sent inside the GCM payload.
        """
        gcm.send({"msg": msg})

    def trigger(self, buy, sell):

        raise NotImplemented

    def action(self, buy, sell):

        raise NotImplemented


class HighRule(Rule):
    """
    Send a GCM message when the SELL price exceeds the specified threshold
    """

    def __init__(self, threshold):

        self.threshold = threshold

    def trigger(self, buy, sell):

        return sell > self.threshold

    def action(self, buy, sell):

        self.send("Sell Price > ${0:.2f}".format(self.threshold))


class LowRule(Rule):
    """
    Send a GCM message when the BUY price drops below the specified threshold
    """

    def __init__(self, threshold):

        self.threshold = threshold

    def trigger(self, buy, sell):

        return buy < self.threshold

    def action(self, buy, sell):

        self.send("Buy Price < ${0:.2f}".format(self.threshold))



RULES = [

    LowRule(secrets.LOW_PRICE),           # Send a notification when the buy price falls below the specified price
    HighRule(secrets.HIGH_PRICE),          # Send a notification when the sell price falls below the specified price
]