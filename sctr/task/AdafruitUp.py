from keras.models import load_model
import cv2
import numpy as np
import requests
import threading

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()


# Adafruit IO credentials
ADAFRUIT_IO_USERNAME = "NguyenAnhKhoa"
ADAFRUIT_IO_KEY = "aio_zBFH82fGLNKAcqf1TlhK6EE5lddH"

# Base URL for Adafruit IO feeds
ADAFRUIT_IO_BASE_URL = f"https://io.adafruit.com/api/v2/{ADAFRUIT_IO_USERNAME}/feeds/"

# Lock for synchronization between threads
data_lock = threading.Lock()

# Shared data between fruit classification and IoT upload tasks
shared_data = {
    "fruit": None,
    "confidence": None,
}

# IoT Task for uploading data to Adafruit IO
class IoTUploadTask:
    def __init__(self, feed_name):
        self.feed_url = ADAFRUIT_IO_BASE_URL + feed_name + "/data"

    def run(self):
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
                response = requests.post(self.feed_url, headers=headers, json=payload)
                response.raise_for_status()  # Raise an error for HTTP errors

                # Check for successful request
                if response.status_code == 200:
                    print(f"Data uploaded to Adafruit IO feed {self.feed_url} successfully")
                else:
                    print(f"Failed to upload data to Adafruit IO feed {self.feed_url}. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")

    def start(self):
        upload_thread = threading.Thread(target=self.run)
        upload_thread.start()

# CAMERA can be 0 or 1 based on the default camera of your computer
camera = cv2.VideoCapture(0)

# Instantiate IoT upload tasks for three separate feeds
upload_task1 = IoTUploadTask("fruit1")
upload_task2 = IoTUploadTask("fruit2")
upload_task3 = IoTUploadTask("fruit3")

# Start the upload tasks
upload_task1.start()
upload_task2.start()
upload_task3.start()

while True:
    # Grab the web camera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Make the image a numpy array and reshape it to the model's input shape.
    image_array = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image_array = (image_array / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image_array)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]

    # Convert confidence_score to a standard Python data type (e.g., float)
    confidence_score = float(confidence_score)

    # Print prediction and confidence score
    print("Class:", class_name)
    print("Confidence Score:", confidence_score)

    # Update shared data
    with data_lock:
        shared_data["fruit"] = class_name
        shared_data["confidence"] = confidence_score

    # Show the image in a window
    cv2.imshow("Webcam Image", image)

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

# Release the camera and close all windows
camera.release()
cv2.destroyAllWindows()