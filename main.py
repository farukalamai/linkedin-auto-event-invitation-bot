from selenium import webdriver
import os
import csv
import time
from login import load_cookies, login_and_save_cookies
from inviter import LinkedInInviter
from config import INVITED_ATTENDEES_CSV
from utils import wait_for_internet_connection  # Import the new function

# Initialize the webdriver
driver = webdriver.Chrome()  # or webdriver.Firefox(), depending on your browser

# Ensure internet is connected before proceeding
wait_for_internet_connection()

# Load cookies if available, else login and save cookies
load_cookies(driver)
time.sleep(5)

# Check if CSV file exists, if not, create it
if not os.path.exists(INVITED_ATTENDEES_CSV):
    with open(INVITED_ATTENDEES_CSV, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Headline", "Timestamp"])  # Add headers to the CSV file
    time.sleep(5)

# Create the LinkedInInviter instance and invite attendees
inviter = LinkedInInviter(driver)
inviter.invite_attendees(max_invites=10)

# Close the browser
driver.quit()
