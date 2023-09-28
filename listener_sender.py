#!/bin/python3
import paho.mqtt.client as mqtt
import json
from azure.iot.device import IoTHubDeviceClient, Message
from azure.iot.device.exceptions import ConnectionFailedError, ConnectionDroppedError, OperationTimeout, OperationCancelled, NoConnectionError
from log import console, log

# Azure IoT Hub connection details
CONNECTION_STRING = "HostName=FreekHub.azure-devices.net;DeviceId=rasp;SharedAccessKey=fHIIUwn+6gQOkAcLYS59gLWBd43BZ5ge/GPfbsswQH4="

# MQTT Broker settings
MQTT_BROKER_HOST = "192.168.137.3"
MQTT_BROKER_PORT = 1883 # Default MQTT port
MQTT_TOPIC = "sensor_data"
username = "vosko"
password = "vosko"

# Define the callback function for when a message is received from MQTT
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    try:
        data = json.loads(payload)
        deviceId = data.get("deviceId")
        temperature = data.get("temperature")
        humidity = data.get("humidity")
        pressure = data.get("pressure")

        if temperature is not None and humidity is not None and pressure is not None and deviceId is not None:
            try:
                send_to_azure_iot_hub(temperature, humidity, pressure, deviceId)
            except KeyboardInterrupt:
                # Shut down the device client when Ctrl+C is pressed
                log.error("Shutting down", exit_after=False)
                azure_iot_client.shutdown()
        else:
            print("Incomplete data received:", data)

    except json.JSONDecodeError:
        print("Invalid JSON received:", payload)

# Initialize the MQTT client
mqtt_client = mqtt.Client()

# Set username and password
mqtt_client.username_pw_set(username, password)

mqtt_client.on_message = on_message

# Connect to the MQTT broker
mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
mqtt_client.subscribe(MQTT_TOPIC)

with console.status("Connecting to IoT Hub with Connection String", spinner="arc", spinner_style="blue"):
    # Create instance of the device client using the connection string
    # Azure IoT Hub client
    azure_iot_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    # Connect the device client.
    azure_iot_client.connect()
log.success("Connected to IoT Hub")

# Function to send data to Azure IoT Hub
def send_to_azure_iot_hub(temperature, humidity, pressure, deviceId):
    payload = {
        "deviceId": deviceId,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
    }
    message = Message(json.dumps(payload))
    try:
        azure_iot_client.send_message(message)
    except (ConnectionFailedError, ConnectionDroppedError, OperationTimeout, OperationCancelled, NoConnectionError):
        log.warning("Message failed to send, skipping")
    else:
        log.success("Message successfully sent!", message)

# Start the MQTT client loop
mqtt_client.loop_forever()