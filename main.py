from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
from config import CHROME_USER_DATA_DIR
from scraper.login import is_logged_in, do_login, select_character, click_enter_game_if_exists
from scraper.market import go_to_market
from scraper.utils import reset_index
from db.handler import create_table, clear_data
from export_data.export import export_to_json


def main():
    total_start = time.time()

    print("🚀 เริ่มต้นระบบ")
    options = Options()
    profile_path = os.path.abspath(CHROME_USER_DATA_DIR)
    options.add_argument("--headless")  # ซ่อน browser
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--window-size=1920,1080") 

    driver = webdriver.Chrome(options=options)

    # Reset index
    t = time.time()
    reset_index()
    print(f"🧹 Reset index ใช้เวลา {time.time() - t:.2f} วินาที")

    # Login
    t = time.time()
    if is_logged_in(driver):
        print("✅ Login อยู่แล้ว")
        click_enter_game_if_exists(driver)
    else:
        print("🔐 กำลัง login อัตโนมัติ")
        do_login(driver)
    print(f"🔑 การเข้าสู่ระบบใช้เวลา {time.time() - t:.2f} วินาที")

    # เลือกตัวละคร
    t = time.time()
    select_character(driver)
    print(f"🧙 เลือกตัวละครใช้เวลา {time.time() - t:.2f} วินาที")

    # จัดการฐานข้อมูล
    t = time.time()
    clear_data()
    create_table()
    print(f"🗃️ จัดการฐานข้อมูลใช้เวลา {time.time() - t:.2f} วินาที")

    # ไปหน้า Marketplace และดึงข้อมูล
    t = time.time()
    go_to_market(driver)
    print(f"🛒 เข้า Marketplace และดึงข้อมูลใช้เวลา {time.time() - t:.2f} วินาที")

    # ปิดเบราว์เซอร์
    t = time.time()
    driver.quit()
    print(f"🛑 ปิดเบราว์เซอร์ใช้เวลา {time.time() - t:.2f} วินาที")

    #ส่งออกข้อมูลจาก database เป็น json
    t = time.time()
    export_to_json()
    print(f"🛑 ส่งออกข้อมูลจาก database เป็น json ใช้เวลา {time.time() - t:.2f} วินาที")
    total_end = time.time()
    print(f"\n⏱️ เวลารวมทั้งหมด: {total_end - total_start:.2f} วินาที")

if __name__ == "__main__":
    main()
