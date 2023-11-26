# rtos_manager.py

import uasyncio as asyncio
import _thread
import requests
import cv2
import numpy as np

class RTOSManager:
    def __init__(self, username, key):
        self.ADIO_USERNAME = username
        self.ADIO_KEY = key
        self.ADIO_BASE_URL = f"https://io.adafruit.com/api/v2/{self.ADIO_USERNAME}/feeds/"

        self.data_lock = _thread.allocate_lock()
        self.shared_data = {"fruit": None, "confidence": None}
        self.camera = cv2.VideoCapture(0)

    def upload_to_adafruit_io(self, feed_name):
        feed_url = self.ADIO_BASE_URL + feed_name + "/data"

        while True:
            with self.data_lock:
                fruit = self.shared_data["fruit"]
                confidence_score = self.shared_data["confidence"]

            payload = {"value": confidence_score, "fruit": fruit}

            headers = {"X-AIO-Key": self.ADIO_KEY, "Content-Type": "application/json"}

            try:
                response = requests.post(feed_url, headers=headers, json=payload)
                response.raise_for_status()

                if response.status_code == 200:
                    print(f"Data uploaded to Adafruit IO feed {feed_url} successfully")
                else:
                    print(f"Failed to upload data to Adafruit IO feed {feed_url}. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")

            await asyncio.sleep(5)

    def classify_fruit(self):
        while True:
            ret, image = self.camera.read()
            image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

            image_array = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
            image_array = (image_array / 127.5) - 1

            prediction = model.predict(image_array)
            index = np.argmax(prediction)
            class_name = class_names[index].strip()
            confidence_score = prediction[0][index]

            with self.data_lock:
                self.shared_data["fruit"] = class_name
                self.shared_data["confidence"] = confidence_score

            await asyncio.sleep(2)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.upload_to_adafruit_io("fruit1"))
        loop.create_task(self.upload_to_adafruit_io("fruit2"))
        loop.create_task(self.upload_to_adafruit_io("fruit3"))
        loop.create_task(self.classify_fruit())
        loop.run_forever()
