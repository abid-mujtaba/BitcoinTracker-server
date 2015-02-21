"""
Contains the settings for the project.
"""

import os


DB_NAME = "bitcoin.db"


def db():
    """
    :return: A File object that refers to the SQLITE3 database.
    """
    cwd = os.path.abspath(os.path.dirname(__file__))            # Get the current directory which contains this file

    return os.path.join(cwd, DB_NAME)