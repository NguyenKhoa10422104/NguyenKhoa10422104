import requests
import time

# Adafruit IO credentials
ADAFRUIT_IO_USERNAME = "NguyenAnhKhoa"
ADAFRUIT_IO_KEY = "aio_LWUU04Yp2NOGKYIIcmtzUwl3SXCY"

# Base URL for Adafruit IO feeds
ADAFRUIT_IO_BASE_URL = f"https://io.adafruit.com/api/v2/{ADAFRUIT_IO_USERNAME}/feeds/"

# Function to upload data to Adafruit IO based on confidence score
def upload_to_adafruit(fruit, confidence_score):
    # Decide which feed to upload based on the confidence score
    if confidence_score < 0.3:
        feed_name = "fruit1"
    elif 0.3 <= confidence_score < 0.66:
        feed_name = "fruit2"
    else:
        feed_name = "fruit3"

    feed_url = ADAFRUIT_IO_BASE_URL + feed_name + "/data"

    payload = {
        "value": confidence_score,
        "fruit": fruit,
    }

    headers = {
        "X-AIO-Key": ADAFRUIT_IO_KEY,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(feed_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for HTTP errors

        # Check for successful request
        if response.status_code == 200:
            print(f"Data uploaded to Adafruit IO feed {feed_url} successfully")
        else:
            print(f"Failed to upload data to Adafruit IO feed {feed_url}. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Example usage
while True:
    # Replace these with actual values obtained from your classification
    fruit = "Apple"
    confidence_score = 0.7

    # Upload data to Adafruit IO based on confidence score
    upload_to_adafruit(fruit, confidence_score)

    # Wait for 5 seconds before the next upload
    time.sleep(5)
