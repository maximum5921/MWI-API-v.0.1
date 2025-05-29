import sqlite3
import os
from config import DATABASE_PATH

def create_table():
    # ถ้าไม่มีไฟล์ฐานข้อมูล ให้สร้างไฟล์และตาราง
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
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO market_data (name, ask_price, bid_price) VALUES (?, ?, ?)
    ''', (name, ask_price, bid_price))
    conn.commit()
    conn.close()

def clear_data():
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM market_data")  # ลบข้อมูลทั้งหมดในตาราง แต่ไม่ลบตาราง
    c.execute("DELETE FROM sqlite_sequence WHERE name='market_data'")
    conn.commit()
    conn.close()
