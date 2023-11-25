# scheduler.py

import sched
import time
import _thread
import requests
from camera_module import initialize_camera, capture_image

# Your Adafruit IO credentials
ADAFRUIT_IO_USERNAME = "<YOUR_ADAFRUIT_IO_USERNAME>"
ADAFRUIT_IO_KEY = "<YOUR_ADAFRUIT_IO_KEY>"

# Base URL for Adafruit IO feeds
ADAFRUIT_IO_BASE_URL = f"https://io.adafruit.com/api/v2/{ADAFRUIT_IO_USERNAME}/feeds/"

# Lock for synchronization between threads
data_lock = _thread.allocate_lock()

# Shared data between fruit classification and IoT upload tasks
shared_data = {
    "fruit": None,
    "confidence": None,
}

# Function to upload data to Adafruit IO
def upload_to_adafruit_io(feed_name):
    feed_url = ADAFRUIT_IO_BASE_URL + feed_name + "/data"

    while True:
        # Retrieve classified fruit and confidence score from shared data
        with data_lock:
            fruit = shared_data["fruit"]
            confidence_score = shared_data["confidence"]

        # Upload data to Adafruit IO
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

        # Add a delay of 5 seconds
        time.sleep(5)

# Function for fruit classification
def classify_fruit(camera):
    while True:
        # Capture an image
        image = capture_image(camera)

        # Simulate image classification
        class_name = "Apple"
        confidence_score = 0.95

        # Update shared data
        with data_lock:
            shared_data["fruit"] = class_name
            shared_data["confidence"] = confidence_score

        # Simulate a delay before capturing the next image
        time.sleep(2)

# Function to start the scheduler
def start_scheduler():
    # Initialize the camera
    camera = initialize_camera()

    # Create a scheduler
    scheduler = sched.scheduler(time.time, time.sleep)

    # Schedule the tasks
    scheduler.enter(0, 1, _thread.start_new_thread, (upload_to_adafruit_io, ("fruit1",)))
    scheduler.enter(0, 1, _thread.start_new_thread, (upload_to_adafruit_io, ("fruit2",)))
    scheduler.enter(0, 1, _thread.start_new_thread, (upload_to_adafruit_io, ("fruit3",)))
    scheduler.enter(0, 2, _thread.start_new_thread, (classify_fruit, (camera,)))

    # Start the scheduler
    scheduler.run()

# Call the start_scheduler function when this script is run as the main module
if __name__ == "__main__":
    start_scheduler()
