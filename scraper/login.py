from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from config import EMAIL, PASSWORD
import json
import os

COOKIE_PATH = "cookies.json"

def save_cookies(driver):
    with open(COOKIE_PATH, "w") as file:
        json.dump(driver.get_cookies(), file)
    print("💾 บันทึก cookies สำเร็จ")

def load_cookies(driver):
    if not os.path.exists(COOKIE_PATH):
        raise Exception("ไม่พบไฟล์ cookies")
    with open(COOKIE_PATH, "r") as file:
        cookies = json.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)
        
def is_logged_in(driver):
    
    wait = WebDriverWait(driver, 3)
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[normalize-space()="Login"]')))
        return False
    except Exception:
        return True

def click_enter_game_if_exists(driver):
    try:
        wait = WebDriverWait(driver, 2)
        enter_game_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[contains(text(), "ENTER GAME")]')))
        enter_game_btn.click()
    except Exception:
        pass

def do_login(driver):
    try:
        login_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[normalize-space()="Login"]')))
        login_btn.click()
        time.sleep(1)

        email_input = driver.find_element(By.ID, ':r4:')
        password_input = driver.find_element(By.ID, ':r5:')

        email_input.send_keys(EMAIL)
        password_input.send_keys(PASSWORD)

        submit_btn = driver.find_element(By.CSS_SELECTOR, "button.LoginForm_button__QjRcG")
        submit_btn.click()

    except Exception as e:
        print("❌ เกิดข้อผิดพลาดระหว่าง login:", e)

def select_character(driver):
    wait = WebDriverWait(driver, 300)
    character_selector = (By.CSS_SELECTOR, 'a[href^="/game?characterId="]')
    wait.until(EC.element_to_be_clickable(character_selector))
    driver.find_element(*character_selector).click()
