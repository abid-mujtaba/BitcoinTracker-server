"""
Contains the settings for the project.
"""

import os


DB_NAME = "bitcoin.db"
DB_PATH = "/home/abid/www/bitcoin/"     # This is the path as it exists on the remote server.


def db():
    """
    :return: A File object that refers to the SQLITE3 database.
    """

    return os.path.join(DB_PATH, DB_NAME)