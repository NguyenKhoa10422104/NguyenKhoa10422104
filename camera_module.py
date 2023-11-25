# camera_module.py

import cv2
import numpy as np

def initialize_camera():
    # CAMERA can be 0 or 1 based on the default camera of your computer
    return cv2.VideoCapture(0)

def capture_image(camera):
    # Grab the web camera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    return image
