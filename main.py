# main.py

from selenium import webdriver
import csv
import os
import login
import inviter
import config

# Initialize the webdriver
driver = webdriver.Chrome()  # Or webdriver.Firefox(), depending on your browser

# Load cookies or log in if cookies are not available
login.load_cookies(driver)

# Check if cookies were successfully loaded, otherwise prompt to login
if not driver.get_cookies():
    login.login_and_save_cookies()

# Ensure the invited attendees CSV file exists
if not os.path.exists(config.INVITED_ATTENDEES_CSV):
    with open(config.INVITED_ATTENDEES_CSV, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Attendee Name", "Attendee Headline"])

# Create the LinkedInInviter object and start the invitation process
inviter_instance = inviter.LinkedInInviter(driver)
new_invites = inviter_instance.invite_attendees()


# Save the new invites to the CSV file
if new_invites:
    with open(config.INVITED_ATTENDEES_CSV, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(new_invites)

# Close the browser when done
driver.quit()