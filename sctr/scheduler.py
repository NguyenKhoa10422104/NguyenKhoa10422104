import schedule
import time
import sys
sys.path.append('/sctr/task')  # Adjust the path based on your actual directory structure
from task.AdafruitUpload import upload_to_adafruit

# Example function to simulate fruit classification
def classify_fruit():
    # Replace this with your actual fruit classification code
    fruit = "Apple"
    confidence_score = 0.7

    # Upload data to Adafruit IO based on confidence score
    upload_to_adafruit(fruit, confidence_score)

# Schedule the fruit classification task every 5 seconds
schedule.every(5).seconds.do(classify_fruit)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)