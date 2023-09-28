#!/bin/python3
import paho.mqtt.client as mqtt
import json

# MQTT Broker settings
broker_address = "mqtt_broker_address"
port = 1883
username = "your_username"
password = "your_password"

# Callback function for when a message is received
def on_message(client, userdata, message):
    # Decode the message payload
    data = json.loads(message.payload.decode('utf-8'))

    # Extract data for temperature, humidity, and pressure
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    pressure = data.get('pressure')

    # Now, you can send this data to Azure IoT Hub
    # See step 2 for Azure IoT Hub integration

# Create an MQTT client instance
client = mqtt.Client()

# Set username and password
client.username_pw_set(username, password)

# Set the callback function
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, port)

# Subscribe to the topics
client.subscribe("topic/temperature")
client.subscribe("topic/humidity")
client.subscribe("topic/pressure")

# Start the MQTT client loop
client.loop_forever()