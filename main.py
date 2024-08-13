from selenium import webdriver
import os
import csv
import time
import logging
from login import load_cookies, login_and_save_cookies
from inviter import LinkedInInviter
from config import INVITED_ATTENDEES_CSV, LOG_FILE_PATH, MAX_INVITES

# Set up logging using the path from the config file
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.DEBUG,  # You can change this to INFO or ERROR as needed
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Log that the script has started
logging.info("LinkedIn inviter script started.")

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

    # Check if CSV file exists, if not, create it
    if not os.path.exists(INVITED_ATTENDEES_CSV):
        with open(INVITED_ATTENDEES_CSV, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Headline", "Timestamp"])  # Add headers to the CSV file
        logging.info(f"CSV file '{INVITED_ATTENDEES_CSV}' created with headers.")
        time.sleep(5)

    # Create the LinkedInInviter instance and invite attendees
    inviter = LinkedInInviter(driver)
    inviter.invite_attendees(max_invites=MAX_INVITES)

except Exception as e:
    logging.error(f"An error occurred during the invitation process: {e}")

finally:
    # Close the browser
    driver.quit()
    logging.info("WebDriver closed and script finished.")
