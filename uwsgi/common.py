"""
Contains functions and utilities which are used by multiple modules.
"""

from datetime import datetime as dt
import jinja2
import os
import pytz


def get_parent_dir(f):
    """
    :param f: os.path file object (usually __file__)
    :return: Absolute path of the parent of the directory containing the specified file.
    """

    cwd = os.path.dirname(f)
    return os.path.abspath(os.path.join(cwd, os.pardir))


def format_time(t):
    """
    :param t: Integral timestamp.
    :return: Specified timestamp localized to PST and returned as a formatted string.
    """

    ut = pytz.utc.localize(dt.utcfromtimestamp(t))          # Localize time as UTC
    tz = pytz.timezone('Asia/Karachi')                      # Get timezone for PST
    tc = tz.normalize(ut.astimezone(tz))                     # Convert time to PST

    return tc.strftime('%I:%M %p')                           # Get formatted string for the time


def get_template(f, name):
    """
    :param f: File object (usually __file__)
    :param name: Name of the template file e.g. 'current.html'
    :return: A template object which can be passed arguments and rendered.
    """

    # Load the jinja2 template in preparation for rendering:
    templateLoader = jinja2.FileSystemLoader( searchpath="/" )      # We specify that we will be using absolute paths to specify the location of the template file
    templateEnv = jinja2.Environment( loader=templateLoader )

    parent = get_parent_dir(f)      # Get absolute path of parent directory of current directory

    template_file = os.path.join(parent, 'templates', name)

    return templateEnv.get_template(template_file)         # Load template from filesystem
