# LinkedIn Event Auto-Inviter

This script automates the process of inviting attendees to a LinkedIn event using Selenium. It allows you to log into LinkedIn, load event attendees, and automatically send invitations. The script supports logging, making it easier to debug and track the invitation process.

## Getting Started

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/linkedin-inviter.git
cd linkedin-inviter
```
### 2. Set Up a Virtual Environment
On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the Script
Before running the script, you need to edit the `config.py` file to include your LinkedIn credentials, event URL, and other configurations.

- `LINKEDIN_EMAIL`: Your LinkedIn email address.
- `LINKEDIN_PASSWORD`: Your LinkedIn password.
- `LINKEDIN_EVENT_URL`: The URL of the LinkedIn event you want to invite attendees to.
- `MAX_INVITES`: The maximum number of invitations to send per run.

### 5. Running the Script
```bash
python main.py
```
### 6. Viewing Logs
Logs for each run are stored in the `logs` directory. Each log file is named with a timestamp, allowing you to track and debug the script's execution.
