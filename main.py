from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from config import CHROME_USER_DATA_DIR
from scraper.login import is_logged_in, do_login, select_character, click_enter_game_if_exists
from scraper.market import go_to_market
from scraper.utils import reset_index
from db.handler import create_table, clear_data
from export_data.export import export_to_json
import os

def main():
    total_start = time.time()

    print("\U0001F680 เริ่มต้นระบบ")
    options = Options()
    options.add_argument("--window-size=1920,1080") 
    # options.add_argument('--headless')
    options.add_argument(f"--user-data-dir={os.path.abspath('chrome_user_data')}")
    driver = webdriver.Chrome(options=options)
    options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")
   
    driver.get("https://www.milkywayidle.com/")
    
    if is_logged_in(driver):
        print("🔐 กำลัง login อัตโนมัติ")
        do_login(driver)
    else:
        print("✅ Login อยู่แล้ว")
        click_enter_game_if_exists(driver)

    # Reset index
    t = time.time()
    reset_index()
    print(f"\U0001F9F9 Reset index ใช้เวลา {time.time() - t:.2f} วินาที")

    # Login
    t = time.time()
    logged_in = is_logged_in(driver)  # เรียกครั้งเดียวเท่านั้น

    if logged_in:
        print("✅ Login อยู่แล้ว")
        click_enter_game_if_exists(driver)
    else:
        print("🔐 กำลัง login อัตโนมัติ")
        do_login(driver)
    print(f"🔑 การเข้าสู่ระบบใช้เวลา {time.time() - t:.2f} วินาที")

    # เลือกตัวละคร
    t = time.time()
    select_character(driver)
    print(f"\U0001F9D9 เลือกตัวละครใช้เวลา {time.time() - t:.2f} วินาที")

    # จัดการฐานข้อมูล
    t = time.time()
    clear_data()
    create_table()
    print(f"\U0001F5C3️ จัดการฐานข้อมูลใช้เวลา {time.time() - t:.2f} วินาที")

    # ไปหน้า Marketplace และดึงข้อมูล
    t = time.time()
    go_to_market(driver)
    print(f"\U0001F6D2 เข้า Marketplace และดึงข้อมูลใช้เวลา {time.time() - t:.2f} วินาที")

    # ปิดเบราว์เซอร์
    t = time.time()
    driver.quit()
    print(f"\U0001F6D1 ปิดเบราว์เซอร์ใช้เวลา {time.time() - t:.2f} วินาที")

    #ส่งออกข้อมูลจาก database เป็น json
    t = time.time()
    export_to_json()
    print(f"\U0001F6D1 ส่งออกข้อมูลจาก database ใช้เวลา {time.time() - t:.2f} วินาที")

    total_end = time.time()
    print(f"\n⏱️ เวลารวมทั้งหมด: {total_end - total_start:.2f} วินาที")

if __name__ == "__main__":
    main()
