import sqlite3
import json
import os
from datetime import datetime
from config import DATABASE_PATH, EXPORT_PATH



def export_to_json():
    # เชื่อมต่อฐานข้อมูล
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # ดึงข้อมูลทั้งหมด
    cursor.execute("SELECT name, ask_price, bid_price FROM market_data")
    rows = cursor.fetchall()
    conn.close()

    # สร้างโครงสร้างข้อมูล
    data = {
        "exported_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": []
    }

    for row in rows:
        data["items"].append({
            "name": row[0],
            "ask_price": row[1],
            "bid_price": row[2]
        })

    # ลบไฟล์เก่าถ้ามี
    if os.path.exists(EXPORT_PATH):
        os.remove(EXPORT_PATH)

    # บันทึกเป็น JSON
    with open(EXPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"📦 ส่งออกข้อมูลเป็นไฟล์ {EXPORT_PATH} แล้ว")
