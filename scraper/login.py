from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from config import EMAIL, PASSWORD


def is_logged_in(driver):
    """
    Checks if the user is currently logged into the web application.

    Args:
        driver: The Selenium WebDriver instance.

    Returns:
        bool: True if logged in (Login button not visible), False otherwise.
    """
    wait = WebDriverWait(driver, 1)
    try:
        # If the "Login" button is visible, the user is not logged in.
        wait.until(EC.visibility_of_element_located((By.XPATH, '//button[normalize-space()="Login"]')))
        return False
    except Exception:
        # If the "Login" button is not found within the timeout, assume logged in.
        return True

def click_enter_game_if_exists(driver):
    """
    Attempts to click an "ENTER GAME" button if it exists and is clickable.
    This function is designed to be non-blocking and will not raise an error
    if the button is not found.

    Args:
        driver: The Selenium WebDriver instance.
    """
    try:
        wait = WebDriverWait(driver, 2)
        # Wait for the "ENTER GAME" button to be clickable and click it.
        enter_game_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[contains(text(), "ENTER GAME")]')))
        enter_game_btn.click()
    except Exception:
        # If the button is not found or not clickable, do nothing.
        pass

def do_login(driver):
    """
    Performs a login operation on the web application.
    It waits for the login button, clicks it, fills in email and password,
    and then submits the form.

    Args:
        driver: The Selenium WebDriver instance.
    """
    try:
        # Wait for the main "Login" button to be visible and click it.
        login_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//button[normalize-space()="Login"]')))
        login_btn.click()
        time.sleep(1) # Small delay to allow login form to appear

        # Locate email and password input fields by their IDs (assuming dynamic IDs like :r4:, :r5:)
        # Note: Dynamic IDs can change, consider more robust locators if this becomes an issue.
        email_input = driver.find_element(By.ID, ':r4:')
        password_input = driver.find_element(By.ID, ':r5:')

        # Enter credentials from config
        email_input.send_keys(EMAIL)
        password_input.send_keys(PASSWORD)

        # Locate and click the submit button for the login form
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button.LoginForm_button__QjRcG")
        submit_btn.click()

    except Exception as e:
        print("❌ An error occurred during login:", e)

def select_character(driver):
    """
    Selects a character by clicking on the first available character link.
    It waits for a character selection link to be clickable before clicking it.

    Args:
        driver: The Selenium WebDriver instance.
    """
    wait = WebDriverWait(driver, 300) # Long wait time assuming character loading might take a while
    character_selector = (By.CSS_SELECTOR, 'a[href^="/game?characterId="]')
    # Wait until at least one character link is clickable
    wait.until(EC.element_to_be_clickable(character_selector))
    # Click the first character link found
    driver.find_element(*character_selector).click()
