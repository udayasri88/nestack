import sqlite3
from db import DATABASE_PATH

def initialize_database():

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("PRAGMA foreign_keys = ON")

    with open("database/schema.sql", "r") as file:

        schema = file.read()

    connection.executescript(schema)

    connection.close()

    print("Database initialized successfully!")


if __name__ == "__main__":

    initialize_database()