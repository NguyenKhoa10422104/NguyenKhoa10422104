from FruitClassifyExecute import FruitClassifier, ClassificationDataStorage
from AdafruitUpload import AdafruitIOUploader
import cv2

# Initialize objects
classifier = FruitClassifier(model_path="sctr/keras_model.h5", labels_path="sctr/labels.txt")
data_storage = ClassificationDataStorage()
adafruit_uploader = AdafruitIOUploader(
    username="NguyenAnhKhoa",
    key="aio_iSAy13bIQNoqPGtEwiTQlypAKzyD",
    feed_name_1="fruit1",
    feed_name_2="fruit2",
    feed_name_3="fruit3"
)
# Initialize camera
camera = cv2.VideoCapture(0)

while True:
    # Grab the web camera's image.
    ret, image = camera.read()

    # Use the FruitClassifier to classify the image
    class_name, confidence_score = classifier.classify_image(image)

    # Store the classification result
    data_storage.store_classification_result(class_name, confidence_score)

    # Print the classification result
    print("Class:", class_name)
    print("Confidence Score:", confidence_score)

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

# Upload stored data to Adafruit IO
adafruit_uploader.upload_data(data_storage.get_classification_results())
