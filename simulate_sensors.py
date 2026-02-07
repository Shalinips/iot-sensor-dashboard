# simulate_sensors.py

import csv
import random
from datetime import datetime
import time
import os

file_name = "live_sensor_data.csv"

# Create the CSV file with header if it doesn't exist
if not os.path.exists(file_name):
    with open(file_name, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["sensor_id", "temperature", "humidity", "timestamp"])

sensors = ['s1', 's2', 's3', 's4', 's5']

# Generate live sensor data every 1 second
while True:
    sensor_id = random.choice(sensors)
    temperature = random.randint(18, 60)
    humidity = random.randint(35, 85)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(file_name, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([sensor_id, temperature, humidity, timestamp])

    print(f"{sensor_id}, {temperature}°C, {humidity}%, {timestamp}")
    time.sleep(1)
