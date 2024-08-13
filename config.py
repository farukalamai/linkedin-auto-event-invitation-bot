# config.py
import os
from datetime import datetime

LINKEDIN_EMAIL = "EMAIL"  # Replace with your LinkedIn email
LINKEDIN_PASSWORD = "PASSWORD"  # Replace with your LinkedIn password
LINKEDIN_EVENT_URL = "EVENT_URL"
# Configuration for the number of maximum invites per run
MAX_INVITES = 10  # You can change this value as needed

INVITED_ATTENDEES_CSV = "invited_attendees.csv"
INVITED_ATTENDEES_FILE = "invited_attendees.pkl"
COOKIES_FILE = "linkedin_cookies.pkl"

# Create a logs directory if it doesn't exist
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Generate a unique log file name with a timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE_PATH = os.path.join(LOG_DIR, f"linkedin_inviter_{timestamp}.log")

