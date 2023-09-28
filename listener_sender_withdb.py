import paho.mqtt.client as mqtt
from azure.iot.device import IoTHubDeviceClient, Message
import json
import sqlite3
import os

# MQTT Settings
mqtt_broker_address = "192.168.137.3"
mqtt_port = 1883
mqtt_username = "vosko"
mqtt_password = "vosko"
mqtt_topic = "sensor_data"

# Azure IoT Hub Settings
iot_hub_connection_string = "HostName=FreekHub.azure-devices.net;DeviceId=rasp;SharedAccessKey=fHIIUwn+6gQOkAcLYS59gLWBd43BZ5ge/GPfbsswQH4="

# Local Database Settings
db_file = "sensor_data.db"

def create_sensor_data_table():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()

    # Create the sensor_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            temperature REAL,
            humidity REAL,
            pressure REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Callback when MQTT message is received
def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode())
    device_id = payload.get('deviceId')
    temperature = payload.get('temperature')
    humidity = payload.get('humidity')
    pressure = payload.get('pressure')

    # Send data to Azure IoT Hub
    try:
        client = IoTHubDeviceClient.create_from_connection_string(iot_hub_connection_string)
        message = Message(json.dumps(payload))
        client.send_message(message)
        print("Sent to Azure IoT Hub:", payload)
    except Exception as e:
        print("Error sending to Azure IoT Hub:", str(e))

    # Save data to local database (optional)
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sensor_data (device_id, temperature, humidity, pressure) VALUES (?, ?, ?, ?)",
                       (device_id, temperature, humidity, pressure))
        conn.commit()
        conn.close()
        print("Saved to Local Database:", payload)
    except Exception as e:
        print("Error saving to Local Database:", str(e))

# Call the function to create the table
create_sensor_data_table()

# MQTT Client Setup
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username=mqtt_username, password=mqtt_password)
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker_address, mqtt_port)
mqtt_client.subscribe(mqtt_topic)
mqtt_client.loop_forever()