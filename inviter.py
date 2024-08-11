# inviter.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pickle
import os
import config

class LinkedInInviter:
    def __init__(self, driver):
        self.driver = driver
        self.invited_attendees = self.load_invited_attendees()

    def load_invited_attendees(self):
        if os.path.exists(config.INVITED_ATTENDEES_PICKLE):
            with open(config.INVITED_ATTENDEES_PICKLE, "rb") as f:
                return pickle.load(f)
        else:
            return set()

    def save_invited_attendees(self):
        with open(config.INVITED_ATTENDEES_PICKLE, "wb") as f:
            pickle.dump(self.invited_attendees, f)

    def navigate_to_event(self):
        self.driver.get(config.LINKEDIN_EVENT_LINK)

    def click_share_button(self):
        try:
            share_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//span[contains(@class, "align-items-center display-flex")]/ancestor::button'))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", share_button)
            self.driver.execute_script("arguments[0].click();", share_button)
        except Exception as e:
            print(f"Error clicking the Share button: {e}")

    def click_invite_list_item(self):
        try:
            invite_list_item = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//ul[@role='menu']/li[1]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", invite_list_item)
            self.driver.execute_script("arguments[0].click();", invite_list_item)
        except Exception as e:
            print(f"Error clicking the Invite list item: {e}")

    def select_attendees(self, count=10):
        new_invites = []
        attendees_selected = 0

        try:
            while attendees_selected < count:
                # Locate all attendee elements
                attendee_elements = self.driver.find_elements(By.XPATH, '//input[@aria-selected="false"]')

                for attendee_element in attendee_elements:
                    try:
                        # Extract the attendee name
                        name_element = attendee_element.find_element(By.XPATH, ".//ancestor::li//div[@class='flex-1 inline-block align-self-center pl2 mr5']/div[1]")
                        attendee_name = name_element.text.strip()

                        # Extract the attendee headline
                        headline_element = attendee_element.find_element(By.XPATH, ".//ancestor::li//div[@class='flex-1 inline-block align-self-center pl2 mr5']/div[2]")
                        attendee_headline = headline_element.text.strip()

                        # Check if the attendee has already been invited
                        if attendee_name not in self.invited_attendees:
                            # Scroll the element into view
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", attendee_element)

                            # Perform the click using JavaScript to avoid interception issues
                            self.driver.execute_script("arguments[0].click();", attendee_element)

                            # Check if the element is now selected (aria-selected="true")
                            if attendee_element.get_attribute("aria-selected") == "true":
                                # Add the attendee to the invited list
                                self.invited_attendees.add(attendee_name)
                                new_invites.append((attendee_name, attendee_headline))
                                attendees_selected += 1

                            # Break the loop if 10 attendees are selected
                            if attendees_selected >= count:
                                break

                    except Exception as e:
                        print(f"Encountered an issue with an element: {e}")
                        continue

                # Scroll down to load more attendees if fewer than 10 were selected
                if attendees_selected < count:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)  # Give time for new elements to load

        except Exception as e:
            print(f"Error selecting attendees: {e}")
            self.driver.quit()

        return new_invites


    def click_invite_button(self):
        try:
            invite_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[2]/div/button/span'))
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", invite_button)
            self.driver.execute_script("arguments[0].click();", invite_button)
        except Exception as e:
            print(f"Error clicking the Invite button: {e}")

    def invite_attendees(self):
        self.navigate_to_event()
        self.click_share_button()
        self.click_invite_list_item()
        attendees_selected = self.select_attendees()
        if attendees_selected > 0:
            self.click_invite_button()
            print(f"Invited {attendees_selected} new attendees.")
        else:
            print("No attendees were selected.")
        self.save_invited_attendees()
