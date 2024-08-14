from selenium import webdriver
import time
import logging
from utils import setup_logging, setup_csv
from login import load_cookies, login_and_save_cookies
from inviter import LinkedInInviter
from config import LINKEDIN_EVENT_URLS, MAX_INVITES


# Initialize the webdriver
try:
    driver = webdriver.Chrome()  # or webdriver.Firefox(), depending on your browser
    logging.info("WebDriver initialized successfully.")
except Exception as e:
    logging.critical(f"Failed to initialize WebDriver: {e}")
    raise

try:
    # Load cookies if available, else login and save cookies
    load_cookies(driver)
    time.sleep(5)

    for event_url in LINKEDIN_EVENT_URLS:
        event_name = event_url.split('/')[-3]  # Extract a unique event name from the URL
        setup_logging(event_name)  # Setup logging for this event
        csv_file_path = setup_csv(event_name)  # Setup CSV file for this event

        # Create the LinkedInInviter instance and invite attendees
        inviter = LinkedInInviter(driver, event_url, csv_file_path)
        inviter.invite_attendees(max_invites=MAX_INVITES)
        time.sleep(5)

except Exception as e:
    logging.error(f"An error occurred during the invitation process: {e}")

finally:
    # Close the browser
    driver.quit()
    logging.info("WebDriver closed and script finished.")

