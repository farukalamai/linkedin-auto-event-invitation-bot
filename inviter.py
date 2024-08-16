from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pickle
import os
import csv
import logging
from utils import wait_for_internet_connection  # Import the new function
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

from time import sleep
def sleep_minutes(minutes):
    sleep(minutes * 60)

class LinkedInInviter:
    def __init__(self, driver, event_url, csv_file_path):
        self.driver = driver
        self.event_url = event_url
        self.csv_file_path = csv_file_path
        self.invited_attendees = set()
        self.attendees_selected = 0
        self.load_invited_attendees()

    def load_invited_attendees(self):
        invited_attendees = set()

        # Load from CSV file
        if os.path.exists(self.csv_file_path):
            with open(self.csv_file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip the header
                invited_attendees = set(row[0] for row in reader)  # Read all previously invited names

        self.invited_attendees = invited_attendees

    def save_new_invites(self, new_invites):
        with open(self.csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(new_invites)

    def click_invite_list_item(self):
        self.driver.get(self.event_url)
        time.sleep(3)

        try:
            share_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//span[contains(@class, "align-items-center display-flex")]/ancestor::button'))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", share_button)
            self.driver.execute_script("arguments[0].click();", share_button)

            invite_list_item = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//ul[@role='menu']/li[1]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", invite_list_item)
            self.driver.execute_script("arguments[0].click();", invite_list_item)
            return True
        except Exception as e:
            logging.error(f"Error interacting with Share or Invite buttons: {e}")
            return False

    def select_profiles_to_invite(self, max_invites=5):
        time.sleep(3)
        global attendees_selected

        try:
            container = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='invitee-picker-results-container']"))
            )
            
            new_invites = []
            logging.info("Starting the selection of profiles to invite.")

            while self.attendees_selected < max_invites:
                # Ensure the internet connection is available before proceeding
                wait_for_internet_connection()

                # After loading more profiles, select attendees
                attendee_elements = container.find_elements(By.XPATH, './/input[@aria-selected="false"]')

                if len(attendee_elements) > 0:
                    for attendee_element in attendee_elements:
                        # Ensure the internet connection is available before each profile selection
                        wait_for_internet_connection()

                        try:
                            invited_status_elements = attendee_element.find_elements(By.XPATH, ".//ancestor::li//div[@class='invitee-picker-connections-result-item__status t-14 t-black--light t-bold mt2']")

                            if invited_status_elements and invited_status_elements[0].text.strip() == "Invited":
                                continue

                            attendee_name_element = attendee_element.find_element(By.XPATH, ".//ancestor::li//div[@class='flex-1 inline-block align-self-center pl2 mr5']/div[1]")
                            attendee_name = attendee_name_element.text.strip()

                            attendee_headline_element = attendee_element.find_element(By.XPATH, ".//ancestor::li//div[@class='flex-1 inline-block align-self-center pl2 mr5']/div[2]")
                            attendee_headline = attendee_headline_element.text.strip()

                            

                            if (attendee_name, attendee_headline) not in self.invited_attendees:
                                self.driver.execute_script("arguments[0].click();", attendee_element)

                                if attendee_element.get_attribute("aria-selected") == "true":
                                    self.invited_attendees.add(attendee_name)
                                    new_invites.append((attendee_name, attendee_headline, time.strftime('%Y-%m-%d %H:%M:%S')))
                                    self.attendees_selected += 1

                                    logging.info(f"Profile selected: {attendee_name}, Total selected: {self.attendees_selected}")

                            # Check if we have selected the maximum number of profiles
                            if self.attendees_selected >= max_invites:
                                logging.info(f"Stopping selection. Reached max_invites: {self.attendees_selected}")
                                break

                        except Exception as e:
                            logging.error(f"Encountered an issue with an element: {e}")
                            continue

                else:
                    # If no new profiles are found, attempt to load more
                    try:
                        load_more_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//div[@class="display-flex p5"]/button/span[@class="artdeco-button__text"]'))
                        )
                        self.driver.execute_script("arguments[0].click();", load_more_button)
                        logging.info("Clicked the button to load more profiles.")
                        time.sleep(2)  # Allow some time for new profiles to load

                    except Exception as e:
                        logging.warning("Load more button not found. Assuming all profiles are loaded or maximum invites reached.")
                        # Exit the loop if the button is not found, assuming no more profiles can be loaded
                        break


            # After selecting profiles, click the invite button
            if self.attendees_selected > 0:
                self.click_invite_button(new_invites)

            return self.attendees_selected

        except TimeoutException:
            logging.error("Element not found within the given time")
            return 0

    def click_invite_button(self, new_invites):
        try:
            invite_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[2]/div/button/span'))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", invite_button)
            self.driver.execute_script("arguments[0].click();", invite_button)
            logging.info("Invite button clicked.")

            time.sleep(5)

            # Check for the confirmation popup
            try:
                confirmation_popup = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="artdeco-toast-item__content"]/p/span'))
                )
                confirmation_text = confirmation_popup.text.strip()
                if "invited to event" in confirmation_text.lower():
                    # If the confirmation is found, save the invites to the CSV
                    logging.info(f"Invitation confirmed: {confirmation_text}")
                    self.save_new_invites(new_invites)
                    logging.info(f"Successfully invited {len(new_invites)} new attendees.")
                    
                elif "something went wrong" in confirmation_text.lower():
                    logging.error(f"Error during invitation: {confirmation_text}")
                    self.attendees_selected = 0
                    
                    # Click the close button for the error popup
                    close_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//div[@id="artdeco-modal-outlet"]/div/div/button'))
                    )
                    self.driver.execute_script("arguments[0].click();", close_button)
                    logging.info("Error popup closed.")

                    # Click the discard button in the confirmation dialog
                    discard_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[@class="artdeco-button artdeco-button--2 artdeco-button--primary ember-view artdeco-modal__confirm-dialog-btn"]'))
                    )
                    self.driver.execute_script("arguments[0].click();", discard_button)
                    logging.info("Invitation discarded due to error. No attendees were invited.")

            except TimeoutException:
                logging.error("Confirmation popup not found. Invites may not have been sent successfully.")
                self.attendees_selected = 0

        except Exception as e:
            logging.error(f"Error clicking the Invite button: {e}")
            self.attendees_selected = 0


    def invite_attendees(self, max_invites=5):
        self.attendees_selected = 0  # Reset the variable at the start of the method
        if self.click_invite_list_item():
            self.select_profiles_to_invite(max_invites=max_invites)
            if self.attendees_selected > 0:
                logging.info(f"Successfully invited {self.attendees_selected} new attendees.")
            else:
                logging.info("No new attendees were selected.")
        else:
            logging.warning("Failed to initiate the invite process.")
