"""
Contains functions and utilities which are used by multiple modules.
"""

from datetime import datetime as dt
import os
import pytz


def get_parent_dir(f):

    cwd = os.path.dirname(f)
    return os.path.abspath(os.path.join(cwd, os.pardir))


def format_time(t):

    ut = pytz.utc.localize(dt.utcfromtimestamp(t))          # Localize time as UTC
    tz = pytz.timezone('Asia/Karachi')                      # Get timezone for PST
    tc = tz.normalize(ut.astimezone(tz))                     # Convert time to PST

    return tc.strftime('%I:%M %p')                           # Get formatted string for the time