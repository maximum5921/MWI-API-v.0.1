import sqlite3
import os
from config import DATABASE_PATH

def create_table():
    """
    Creates the 'market_data' table in the SQLite database if it doesn't already exist.
    If the database file does not exist, it will be created.
    """
    # Check if the database file exists; if not, it's a new database
    is_new_db = not os.path.exists(DATABASE_PATH)
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    if is_new_db:
        print("Creating new database and table...")
    c.execute('''
        CREATE TABLE IF NOT EXISTS market_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            name TEXT,
            ask_price INTEGER,
            bid_price INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_data(name, ask_price, bid_price):
    """
    Saves market data (name, ask_price, bid_price) into the 'market_data' table.

    Args:
        name (str): The name of the market item.
        ask_price (int): The ask price of the item.
        bid_price (int): The bid price of the item.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO market_data (name, ask_price, bid_price) VALUES (?, ?, ?)
    ''', (name, ask_price, bid_price))
    conn.commit()
    conn.close()

def clear_data():
    """
    Clears all data from the 'market_data' table.
    It also resets the AUTOINCREMENT sequence for the 'id' column.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    # Delete all rows from the table but keep the table structure
    c.execute("DELETE FROM market_data")
    # Reset the AUTOINCREMENT sequence for the id column
    c.execute("DELETE FROM sqlite_sequence WHERE name='market_data'")
    conn.commit()
    conn.close()
import sqlite3
import os
from config import DATABASE_PATH

def create_table():
    """
    Creates the 'market_data' table in the SQLite database if it doesn't already exist.
    If the database file does not exist, it will be created.
    """
    # Check if the database file exists; if not, it's a new database
    is_new_db = not os.path.exists(DATABASE_PATH)
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    if is_new_db:
        print("Creating new database and table...")
    c.execute('''
        CREATE TABLE IF NOT EXISTS market_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            name TEXT,
            ask_price INTEGER,
            bid_price INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_data(name, ask_price, bid_price):
    """
    Saves market data (name, ask_price, bid_price) into the 'market_data' table.

    Args:
        name (str): The name of the market item.
        ask_price (int): The ask price of the item.
        bid_price (int): The bid price of the item.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO market_data (name, ask_price, bid_price) VALUES (?, ?, ?)
    ''', (name, ask_price, bid_price))
    conn.commit()
    conn.close()

def clear_data():
    """
    Clears all data from the 'market_data' table.
    It also resets the AUTOINCREMENT sequence for the 'id' column.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    # Delete all rows from the table but keep the table structure
    c.execute("DELETE FROM market_data")
    # Reset the AUTOINCREMENT sequence for the id column
    c.execute("DELETE FROM sqlite_sequence WHERE name='market_data'")
    conn.commit()
    conn.close()
