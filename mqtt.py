import paho.mqtt.client as mqtt
import json
from azure.iot.device import IoTHubDeviceClient, Message

# Azure IoT Hub connection details
CONNECTION_STRING = "HostName=FreekHub.azure-devices.net;DeviceId=rasp;SharedAccessKey=fHIIUwn+6gQOkAcLYS59gLWBd43BZ5ge/GPfbsswQH4="

# MQTT Broker settings
MQTT_BROKER_HOST = "192.168.137.3"
MQTT_BROKER_PORT = 1883 # Default MQTT port
MQTT_TOPIC = "bme"
username = "vosko"
password = "vosko"

# Define the callback function for when a message is received from MQTT
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    try:
        data = json.loads(payload)
        temperature = data.get("temperature")
        humidity = data.get("humidity")
        pressure = data.get("pressure")

        if temperature is not None and humidity is not None and pressure is not None:
            send_to_azure_iot_hub(temperature, humidity, pressure)
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

# Azure IoT Hub client
azure_iot_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

# Function to send data to Azure IoT Hub
def send_to_azure_iot_hub(temperature, humidity, pressure):
    payload = {
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
    }
    message = Message(json.dumps(payload))
    azure_iot_client.send_message(message)
    print("Data sent to Azure IoT Hub:", payload)

# Start the MQTT client loop
mqtt_client.loop_forever()