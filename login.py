# login.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import os
import config

def login_and_save_cookies():
    driver = webdriver.Chrome()  # Or any other browser you prefer
    driver.get("https://www.linkedin.com/login")

    # Enter username
    username = driver.find_element(By.ID, "username")
    username.send_keys(config.LINKEDIN_USERNAME)

    # Enter password
    password = driver.find_element(By.ID, "password")
    password.send_keys(config.LINKEDIN_PASSWORD)

    # Click the login button
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

    try:
        # Wait until the user is logged in
        WebDriverWait(driver, 120).until(
            EC.url_contains("linkedin.com/feed")
        )
        print("Login successful.")

        # Save the cookies for future use
        cookies = driver.get_cookies()
        with open(config.COOKIES_FILE, "wb") as cookies_file:
            pickle.dump(cookies, cookies_file)
        print("Cookies saved successfully.")

    except Exception as e:
        print(f"Login failed or timed out: {e}")
    finally:
        driver.quit()

def load_cookies(driver):
    if os.path.exists(config.COOKIES_FILE):
        driver.get("https://www.linkedin.com")
        with open(config.COOKIES_FILE, "rb") as cookies_file:
            cookies = pickle.load(cookies_file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.refresh()
    else:
        print("Cookies file not found. Please login first.")
