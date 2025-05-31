from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
from scraper.utils import get_last_index, save_last_index
from db.handler import save_data

def parse_price(txt):
    txt = txt.upper().replace(",", "").strip()
    if "K" in txt:
        return int(float(txt.replace("K", "")) * 1000)
    elif "M" in txt:
        return int(float(txt.replace("M", "")) * 1000000)
    else:
        return int(txt)

def resouce(driver):
    index = get_last_index()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    price_divs = soup.find_all('div', class_='MarketplacePanel_orderBookTableContainer__hUu-X')
    icon_divs = soup.find_all('div', class_='Item_iconContainer__5z7j4')

    if len(icon_divs) > index:
        svg = icon_divs[index].find('svg')
        if svg and svg.has_attr('aria-label'):
            label = svg['aria-label']
            # print(f"🎯 ตำแหน่ง {index}: {label}")
            save_last_index(index + 1)

    ask_price = None
    bid_price = None
    if len(price_divs) >= 2:
        try:
            ask_text = price_divs[0].find('span').get_text(strip=True)
            bid_text = price_divs[1].find('span').get_text(strip=True)
            bid_price = parse_price(bid_text)
            if bid_price is None:
                bid_price = -1
            ask_price = parse_price(ask_text)
            if ask_price is None:
                ask_price = -1
        except Exception as e:
            print("❌ แปลงราคาไม่สำเร็จ:", e)

        # print(f"✅ Ask: {ask_price:,} | Bid: {bid_price:,}")
        
        save_data(label, ask_price, bid_price) 
    else:
        print("name:{label} ❌ เก็บราคาไม่ได้เนื่องจากทำงานเร็วเกินไป")
        return None, None

def go_to_market(driver):
    try:
        marketplace = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "NavigationBar_navigationLink")]//span[normalize-space(text())="Marketplace"]'))
        )
        marketplace.click()
        print("✅ เข้าสู่หน้า Marketplace แล้ว")
        click_items_in_market(driver)
    except Exception as e:
        print("❌ ไม่สามารถเข้า Marketplace ได้:", e)

def click_items_in_market(driver):
    wait = WebDriverWait(driver, 10)
    items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.Item_itemContainer__x7kH1')))
    scrollables = driver.find_elements(By.CSS_SELECTOR, ".TabPanel_tabPanel__tXMJF")
    time.sleep(1)
    c =0
    for item in items[1:3]:
        item.click()
        time.sleep(0.5)
        c +=1
        resouce(driver)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Button_button__1Fe9z"))).click()
        time.sleep(0.5)
        if c == 80:
            first_scrollable = scrollables[1]  # ตัวแรก
            driver.execute_script("arguments[0].scrollTop += 462;", first_scrollable)
            c = 0
            time.sleep(0.5)
