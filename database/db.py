import sqlite3
import os

DATABASE_PATH = os.path.join(
    os.path.dirname(__file__),
    "records.db"
)


def get_db():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection