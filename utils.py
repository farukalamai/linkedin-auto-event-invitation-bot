import requests
import time
import os
import csv
import time
import logging
from datetime import datetime
from config import LOG_DIR, CSV_DIR

def wait_for_internet_connection(retry_interval=5):
    """Wait until the internet connection is available."""
    while True:
        try:
            # Check if we can reach a reliable site (e.g., Google's public DNS server)
            response = requests.get("https://www.google.com", timeout=5)
            if response.status_code == 200:
                print("Internet connection established.")
                return True
        except requests.ConnectionError:
            print(f"No internet connection. Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)

def setup_logging(event_name):
    # Create a directory for the event's logs
    event_log_dir = os.path.join(LOG_DIR, event_name)
    os.makedirs(event_log_dir, exist_ok=True)

    # Generate a unique log file name with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = os.path.join(event_log_dir, f"linkedin_inviter_{timestamp}.log")

    # Set up logging using the path for the specific event
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Remove any previous handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Add file handler for the event log file
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # Add the handler to the logger
    logger.addHandler(file_handler)

    logging.info(f"Logging started for event: {event_name}")

def setup_csv(event_name):
    # Create a directory for the event's CSV file
    event_csv_dir = os.path.join(CSV_DIR, event_name)
    os.makedirs(event_csv_dir, exist_ok=True)

    # Define the CSV file path
    csv_file_path = os.path.join(event_csv_dir, "invited_attendees.csv")

    # Check if CSV file exists, if not, create it with headers
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Headline", "Timestamp"])  # Add headers to the CSV file
        logging.info(f"CSV file '{csv_file_path}' created with headers.")

    return csv_file_path