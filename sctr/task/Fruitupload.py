from keras.models import load_model
import cv2
import numpy as np
import requests

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

# CAMERA can be 0 or 1 based on the default camera of your computer
camera = cv2.VideoCapture(0)

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

    # Print prediction and confidence score
    print("Class:", class_name)
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    # Upload data to the corresponding Adafruit IO feed
    feed_name = f"fruit{index + 1}"
    feed_url = ADAFRUIT_IO_BASE_URL + feed_name + "/data"

    payload = {
        "value": confidence_score * 100,
        "fruit": class_name,
    }

    headers = {
        "X-AIO-Key": ADAFRUIT_IO_KEY,
        "Content-Type": "application/json",
    }

    response = requests.post(feed_url, headers=headers, json=payload)

    # Check for successful request
    if response.status_code == 200:
        print(f"Data uploaded to Adafruit IO feed {feed_name} successfully")

    # Show the image in a window
    cv2.imshow("Webcam Image", image)

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()
