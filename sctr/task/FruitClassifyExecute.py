from keras.models import load_model
import cv2
import numpy as np

class FruitClassifier:
    def __init__(self, model_path, labels_path):
        self.model = load_model(model_path, compile=False)
        self.class_names = open(labels_path, "r").readlines()

    def classify_image(self, image):
        # Resize the raw image into (224-height,224-width) pixels
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

        # Make the image a numpy array and reshape it to the model's input shape.
        image_array = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

        # Normalize the image array
        image_array = (image_array / 127.5) - 1

        # Predicts the model
        prediction = self.model.predict(image_array)
        index = np.argmax(prediction)
        class_name = self.class_names[index].strip()
        confidence_score = float(prediction[0][index])

        return class_name, confidence_score

class ClassificationDataStorage:
    def __init__(self):
        self.classification_results = []

    def store_classification_result(self, class_name, confidence_score):
        result = {"class_name": class_name, "confidence_score": confidence_score}
        self.classification_results.append(result)

    def get_classification_results(self):
        return self.classification_results
