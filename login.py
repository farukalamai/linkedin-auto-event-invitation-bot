from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import os
import time
from config import LINKEDIN_EMAIL, LINKEDIN_PASSWORD, COOKIES_FILE, LOG_FILE_PATH
from utils import wait_for_internet_connection  # Import the new function
import logging

# Set up logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.DEBUG,  # You can change this to INFO or ERROR as needed
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def login_and_save_cookies(driver):
    wait_for_internet_connection()  # Ensure internet is connected

    logging.info("Attempting to log in to LinkedIn.")
    
    # Open LinkedIn login page
    driver.get("https://www.linkedin.com/login")

    # Enter username
    username = driver.find_element(By.ID, "username")
    username.send_keys(LINKEDIN_EMAIL)
    time.sleep(5)
    
    # Enter password
    password = driver.find_element(By.ID, "password")
    password.send_keys(LINKEDIN_PASSWORD)
    time.sleep(5)

    # Click the login button
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    try:
        # Wait until the user is logged in
        WebDriverWait(driver, 120).until(
            EC.url_contains("linkedin.com/feed")
        )
        logging.info("Login successful.")
        time.sleep(5)

        # Save the cookies
        cookies = driver.get_cookies()
        if cookies:
            with open(COOKIES_FILE, "wb") as cookies_file:
                pickle.dump(cookies, cookies_file)
            logging.info("Cookies saved successfully.")
    except Exception as e:
        logging.error(f"Login failed or timed out: {e}")
        driver.quit()

def load_cookies(driver):
    wait_for_internet_connection()  # Ensure internet is connected

    if os.path.exists(COOKIES_FILE):
        driver.get("https://www.linkedin.com")

        with open(COOKIES_FILE, "rb") as cookies_file:
            cookies = pickle.load(cookies_file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.refresh()  # Refresh to apply cookies
        logging.info("Cookies loaded successfully.")
        
    else:
        logging.warning("No cookies found, logging in manually.")
        login_and_save_cookies(driver)
