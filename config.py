# config.py
import os
from datetime import datetime

LINKEDIN_EMAIL = "your_email@example.com"  # Replace with your LinkedIn email
LINKEDIN_PASSWORD = "your_password"  # Replace with your LinkedIn password

# List of event URLs
LINKEDIN_EVENT_URLS = [
    "https://www.linkedin.com/events/7228272784806662144/comments/",
    # Add more event URLs as needed
]

# Configuration for the number of maximum invites per run
MAX_INVITES = 300  # You can change this value as needed

INVITED_ATTENDEES_FILE = "invited_attendees.pkl"
COOKIES_FILE = "linkedin_cookies.pkl"

# Create a logs directory if it doesn't exist
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Create a CSV files directory if it doesn't exist
CSV_DIR = os.path.join(os.path.dirname(__file__), "csv_files")
os.makedirs(CSV_DIR, exist_ok=True)

# Path to the completed events file
COMPLETED_EVENTS_FILE = os.path.join(os.path.dirname(__file__), "completed_events.txt")

