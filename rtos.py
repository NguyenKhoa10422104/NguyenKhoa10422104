# main.py

import _thread
import time  # Use the standard time module instead of utime
import camera_module
import scheduler

# Function to initialize the camera and start image classification
def init_camera_and_classify():
    camera = camera_module.initialize_camera()
    scheduler.classify_fruit(camera)

# Function to start Adafruit IO upload tasks
def start_upload_tasks():
    _thread.start_new_thread(scheduler.upload_to_adafruit_io, ("fruit1",))
    _thread.start_new_thread(scheduler.upload_to_adafruit_io, ("fruit2",))
    _thread.start_new_thread(scheduler.upload_to_adafruit_io, ("fruit3",))

# Start the camera and classification thread
_thread.start_new_thread(init_camera_and_classify, ())

# Start the Adafruit IO upload threads
start_upload_tasks()

# Main loop (optional)
while True:
    # Your main loop logic can go here if needed
    time.sleep(1)
