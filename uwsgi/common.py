"""
Contains functions and utilities which are used by multiple modules.
"""

from datetime import datetime as dt
import jinja2
import os
import pytz


def get_parent_dir():
    """
    :return: Absolute path of the parent of the directory of this file.
    """

    cwd = os.path.dirname(__file__)     # Here __file__ refers to this file 'common.py'. The parent directory is calculated with reference to this file
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


def get_template(name):
    """
    :param name: Name of the template file e.g. 'current.html'
    :return: A template object which can be passed arguments and rendered.
    """

    # Load the jinja2 template in preparation for rendering:
    templateLoader = jinja2.FileSystemLoader( searchpath="/" )      # We specify that we will be using absolute paths to specify the location of the template file

    # We specify that '#' is the line statement prefix so that one can use '# for row in rows:' instead of '{* for row in rows %}
    # We specify that '##' is the line comment prefix so we can start comments with '##'
    # These specifications make writing jinja2 templates easier and clearer.

    templateEnv = jinja2.Environment( loader=templateLoader, line_statement_prefix='#', line_comment_prefix='##' )

    parent = get_parent_dir()      # Get absolute path of parent directory of current directory which contains this file

    template_file = os.path.join(parent, 'templates', name)

    return templateEnv.get_template(template_file)         # Load template from filesystem


def get_db():
    """
    :return: A file object referring to the database file: bitcoin.db
    """

    parent = get_parent_dir()

    return os.path.join(parent, 'bitcoin.db')
