from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
from scraper.utils import get_last_index, save_last_index
from db.handler import save_data


def parse_price(txt):
    """
    Parses a price string (e.g., "100K", "1.2M", "500") into an integer.
    Handles 'K' for thousands and 'M' for millions, and removes commas.

    Args:
        txt (str): The price string to parse.

    Returns:
        int: The parsed price as an integer.
    """
    txt = txt.upper().replace(",", "").strip()
    if "K" in txt:
        return int(float(txt.replace("K", "")) * 1000)
    elif "M" in txt:
        return int(float(txt.replace("M", "")) * 1000000)
    else:
        return int(txt)

def resource(driver):
    """
    Extracts market data (item name, ask price, bid price) from the current page
    and saves it to the database. It uses a saved index to track which item
    is being processed and updates the index after processing.

    Args:
        driver: The Selenium WebDriver instance.
    """
    index = get_last_index()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    price_divs = soup.find_all('div', class_='MarketplacePanel_orderBookTableContainer__hUu-X')
    icon_divs = soup.find_all('div', class_='Item_iconContainer__5z7j4')

    label = "Unknown Item" # Default label in case it's not found
    if len(icon_divs) > index:
        svg = icon_divs[index].find('svg')
        if svg and svg.has_attr('aria-label'):
            label = svg['aria-label']
            # print(f"🎯 Position {index}: {label}") # Original comment translated
            save_last_index(index + 1)

    ask_price = None
    bid_price = None
    if len(price_divs) >= 2:
        try:
            # Assuming the first div in price_divs is for ask and second for bid
            ask_text = price_divs[0].find('span').get_text(strip=True)
            bid_text = price_divs[1].find('span').get_text(strip=True)

            bid_price = parse_price(bid_text)
            if bid_price is None:
                bid_price = -1 # Assign -1 if parsing fails
            ask_price = parse_price(ask_text)
            if ask_price is None:
                ask_price = -1 # Assign -1 if parsing fails
        except Exception as e:
            print(f"❌ Failed to parse price: {e}") # Original comment translated

        # print(f"✅ Ask: {ask_price:,} | Bid: {bid_price:,}") # Original comment translated

        # Save the extracted data
        save_data(label, ask_price, bid_price)
    else:
        print(f"name:{label} ❌ Could not capture price due to fast operation or missing elements.") # Original comment translated
        return None, None

def go_to_market(driver):
    """
    Navigates the WebDriver to the Marketplace section of the web application.
    After navigating, it calls `click_items_in_market` to start processing items.

    Args:
        driver: The Selenium WebDriver instance.
    """
    try:
        # Wait for the "Marketplace" navigation link to be clickable and click it.
        marketplace = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "NavigationBar_navigationLink")]//span[normalize-space(text())="Marketplace"]'))
        )
        marketplace.click()
        print("✅ Entered Marketplace page.") # Original comment translated
        click_items_in_market(driver)
    except Exception as e:
        print(f"❌ Could not enter Marketplace: {e}") # Original comment translated

def click_items_in_market(driver):
    """
    Iterates through items in the marketplace, clicks them to view details,
    extracts data using `resource`, and handles scrolling to load more items.

    Args:
        driver: The Selenium WebDriver instance.
    """
    wait = WebDriverWait(driver, 10)
    # Wait for all item containers to be present
    items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.Item_itemContainer__x7kH1')))
    # Find scrollable elements (assuming there's a specific one for the item list)
    scrollables = driver.find_elements(By.CSS_SELECTOR, ".TabPanel_tabPanel__tXMJF")
    time.sleep(1) # Short delay for page to settle

    c = 0 # Counter for items processed
    # Iterate through a slice of items (from index 1 to 2, effectively items[1] and items[2])
    # Note: The original code iterates items[1:3], which means it processes two items.
    for item in items[1:182]:
        item.click()
        time.sleep(0.5) # Short delay after clicking item
        c += 1
        resource(driver) # Call the resource function to scrape data
        # Click a general button (assuming it closes the item detail or navigates back)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".Button_button__1Fe9z"))).click()
        time.sleep(0.5) # Short delay after clicking button

        # Scroll logic: if 80 items have been processed, scroll the first scrollable element
        # Note: Given the loop processes only 2 items (items[1:3]), this 'if c == 80' condition
        # will likely never be met unless this function is called repeatedly or 'items' list
        # is much larger and the loop logic changes.
        if c == 80:
            first_scrollable = scrollables[1]  # Assuming the second scrollable element is the target
            driver.execute_script("arguments[0].scrollTop += 462;", first_scrollable)
            c = 0 # Reset counter after scrolling
            time.sleep(0.5) # Short delay after scrolling
