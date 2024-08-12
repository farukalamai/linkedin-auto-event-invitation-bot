import requests
import time

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
