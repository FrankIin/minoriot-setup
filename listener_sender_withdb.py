import json
import sqlite3
import paho.mqtt.client as mqtt
from azure.iot.device import IoTHubDeviceClient, Message

# MQTT Broker Configuration
mqtt_broker_host = "192.168.137.3"  # or the IP address of your Raspberry Pi
mqtt_broker_port = 1883
mqtt_username = "vosko"
mqtt_password = "vosko"

# Azure IoT Hub Configuration
azure_iot_hub_connection_string = "HostName=FreekHub.azure-devices.net;DeviceId=rasp;SharedAccessKey=fHIIUwn+6gQOkAcLYS59gLWBd43BZ5ge/GPfbsswQH4="

# SQLite Database Configuration
db_file = "sensor_data.db"

# MQTT Callback when a message is received
def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode())
        save_data_to_local_db(payload)
        send_data_to_azure_iot_hub(payload)
    except Exception as e:
        print(f"Error processing MQTT message: {str(e)}")

# Function to save data to the local SQLite database
def save_data_to_local_db(data):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sensor_data (deviceId, temperature, humidity, pressure) VALUES (?, ?, ?, ?)",
                   (data['deviceId'], data['temperature'], data['humidity'], data['pressure']))
    conn.commit()
    conn.close()

# Function to send data to Azure IoT Hub
def send_data_to_azure_iot_hub(data):
    try:
        device_client = IoTHubDeviceClient.create_from_connection_string(azure_iot_hub_connection_string)
        message = Message(json.dumps(data))
        device_client.send_message(message)
        print("Sent data to Azure IoT Hub:", json.dumps(data))
    except Exception as e:
        print(f"Error sending data to Azure IoT Hub: {str(e)}")

# Initialize and connect to MQTT Broker
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username=mqtt_username, password=mqtt_password)
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker_host, mqtt_broker_port)
mqtt_client.subscribe("sensor_data")
mqtt_client.loop_start()

# Main loop
while True:
    # Check for unsent data in the local database and send it to Azure IoT Hub
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor_data")
    rows = cursor.fetchall()
    for row in rows:
        data = {
            "deviceId": row[0],
            "temperature": row[1],
            "humidity": row[2],
            "pressure": row[3]
        }
        send_data_to_azure_iot_hub(data)
        cursor.execute("DELETE FROM sensor_data WHERE rowid=?", (row[4],))
        conn.commit()
    conn.close()