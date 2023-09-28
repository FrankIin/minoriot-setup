import os
import json
import sqlite3
import time
from azure.iot.device import IoTHubDeviceClient, Message
import paho.mqtt.client as mqtt

# Define MQTT broker settings
MQTT_BROKER_HOST = "192.168.137.3"
MQTT_BROKER_PORT = 1883
MQTT_USERNAME = "vosko"
MQTT_PASSWORD = "vosko"
MQTT_TOPIC = "sensor_data"

# Define Azure IoT Hub settings
IOT_HUB_CONNECTION_STRING = "HostName=FreekHub.azure-devices.net;DeviceId=rasp;SharedAccessKey=fHIIUwn+6gQOkAcLYS59gLWBd43BZ5ge/GPfbsswQH4="

# Define local database settings
DB_PATH = "sensor_data.db"

# Create a local SQLite database if it doesn't exist
def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deviceId TEXT,
            temperature REAL,
            humidity REAL,
            pressure REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Connect to Azure IoT Hub
def connect_to_iot_hub():
    return IoTHubDeviceClient.create_from_connection_string(IOT_HUB_CONNECTION_STRING)

# MQTT message handler
def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode('utf-8'))
        device_id = payload['deviceId']
        temperature = payload['temperature']
        humidity = payload['humidity']
        pressure = payload['pressure']
        
        # Store data in the local database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sensor_data (deviceId, temperature, humidity, pressure)
            VALUES (?, ?, ?, ?)
        ''', (device_id, temperature, humidity, pressure))
        conn.commit()
        conn.close()
        
        print(f"Received data from {device_id}: Temp={temperature}, Humidity={humidity}, Pressure={pressure}")
        
        # Send data to Azure IoT Hub if the connection is available
        if azure_iot_client.connected:
            message = Message(json.dumps(payload))
            azure_iot_client.send_message(message)
            print("Sent data to Azure IoT Hub")
    except Exception as e:
        print(f"Error processing MQTT message: {str(e)}")

# Initialize the local database
create_database()

# Connect to Azure IoT Hub
azure_iot_client = connect_to_iot_hub()

# Initialize MQTT client
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.on_message = on_message

# Connect to MQTT broker
mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
mqtt_client.subscribe(MQTT_TOPIC, qos=0)

# Start the MQTT loop
mqtt_client.loop_start()

try:
    while True:
        # You can add other logic here if needed
        time.sleep(5)  # Sleep for 5 seconds
except KeyboardInterrupt:
    print("Disconnecting...")
    mqtt_client.disconnect()
    azure_iot_client.disconnect()