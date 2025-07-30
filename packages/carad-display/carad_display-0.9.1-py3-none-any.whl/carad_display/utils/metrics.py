import requests
from datetime import datetime, timezone

from carad_display.utils.videos import SERVER_URL
from carad_display.utils.gps import get_gps


def get_machine_id():
    try:
        with open("/etc/machine-id", "r") as f:
            machine_id = f.read().strip()
        return machine_id
    except FileNotFoundError:
        return None


def send_metrica(video_played: str):
    try:
        url = SERVER_URL + 'metrics'  # Replace with your target URL

        # Current time in UTC as a datetime object
        now_utc = datetime.now(timezone.utc)
        # Convert to timestamp in seconds (float)
        timestamp_sec = now_utc.timestamp()
        # Convert to milliseconds (integer)
        timestamp_ms = int(timestamp_sec * 1000)

        # Data to send in the POST request (as a dictionary)
        data = { 
            "machine_id": get_machine_id(),
            "time": timestamp_ms,
            "geo": str(get_gps()),
            "video_played": video_played
        }

        # Send POST request with form-encoded data
        response = requests.post(url, json=data)
        print("Status code:", response.status_code)
        print("Response body:", response.text)

    except Exception as e:
        print(e)
