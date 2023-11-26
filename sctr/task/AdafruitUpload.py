import requests

class AdafruitIOUploader:
    def __init__(self, username, key, feed_name_1, feed_name_2, feed_name_3):
        self.username = username
        self.key = key
        self.feed_url_1 = f"https://io.adafruit.com/api/v2/{self.username}/feeds/{feed_name_1}/data"
        self.feed_url_2 = f"https://io.adafruit.com/api/v2/{self.username}/feeds/{feed_name_2}/data"
        self.feed_url_3 = f"https://io.adafruit.com/api/v2/{self.username}/feeds/{feed_name_3}/data"

    def upload_data(self, data):
        headers = {"X-AIO-Key": self.key, "Content-Type": "application/json"}

        for result in data:
            payload = {"value": result["confidence_score"], "fruit": result["class_name"]}

            # Determine which feed to upload based on confidence score
            if 0.0 <= result["confidence_score"] < 0.33:
                feed_url = self.feed_url_1
            elif 0.33 <= result["confidence_score"] <= 0.67:
                feed_url = self.feed_url_2
            else:
                feed_url = self.feed_url_3

            try:
                response = requests.post(feed_url, headers=headers, json=payload)
                response.raise_for_status()

                if response.status_code == 200:
                    print(f"Data uploaded to Adafruit IO feed {feed_url} successfully")
                else:
                    print(f"Failed to upload data to Adafruit IO feed {feed_url}. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
                print(f"Response content: {response.text if response else 'N/A'}")
