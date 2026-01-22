import sqlite3

def get_db_connection():
    conn = sqlite3.connect('db/coffee_shop.db')
    conn.row_factory = sqlite3.Row  # To access rows like dictionaries
    return conn
