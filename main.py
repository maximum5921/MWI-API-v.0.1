from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
# Assuming these modules exist and are correctly configured in your project
from config import CHROME_USER_DATA_DIR
from scraper.login import is_logged_in, do_login, select_character, click_enter_game_if_exists
from scraper.market import go_to_market
from scraper.utils import reset_index
from db.handler import create_table, clear_data
from export_data.export import export_to_json


def main():
    """
    Main function to orchestrate the web scraping process.
    It initializes the WebDriver, performs login, character selection,
    data management (resetting index, clearing/creating database table),
    navigates to the marketplace to scrape data, and finally exports data to JSON.
    """
    total_start = time.time()

    print("🚀 Starting the system")
    options = Options()
    options.add_argument("--window-size=1920,1080")
    # Uncomment the line below to run in headless mode (without opening a browser window)
    options.add_argument('--headless')
    # Set user data directory for Chrome to persist login sessions and settings
    options.add_argument(f"--user-data-dir={os.path.abspath('chrome_user_data')}")
    driver = webdriver.Chrome(options=options)
    # This line seems redundant if the above line is already setting user-data-dir
    # options.add_argument(f"--user-data-dir={CHROME_USER_DATA_DIR}")

    driver.get("https://www.milkywayidle.com/")

    # Reset index for scraping
    t = time.time()
    reset_index()
    print(f"🧹 Reset index took {time.time() - t:.2f} seconds")

    # Login process
    t = time.time()
    if is_logged_in(driver):
        print("✅ Already logged in")
        click_enter_game_if_exists(driver)
    else:
        print("🔐 Performing automatic login")
        do_login(driver)
    print(f"🔑 Login process took {time.time() - t:.2f} seconds")

    # Character selection
    t = time.time()
    select_character(driver)
    print(f"🧑‍🚀 Character selection took {time.time() - t:.2f} seconds")

    # Database management
    t = time.time()
    clear_data() # Clear existing data
    create_table() # Ensure table exists
    print(f"🗄️ Database management took {time.time() - t:.2f} seconds")

    # Navigate to Marketplace and fetch data
    t = time.time()
    go_to_market(driver)
    print(f"🛒 Entering Marketplace and fetching data took {time.time() - t:.2f} seconds")

    # Close the browser
    t = time.time()
    driver.quit()
    print(f"👋 Closing browser took {time.time() - t:.2f} seconds")

    # Export data from database to JSON
    t = time.time()
    export_to_json()
    print(f"📤 Exporting data from database took {time.time() - t:.2f} seconds")

    total_end = time.time()
    print(f"\n⏱️ Total time elapsed: {total_end - total_start:.2f} seconds")

if __name__ == "__main__":
    main()
