import paho.mqtt.client as mqtt

# MQTT Broker settings
broker_address = "192.168.137.3"  # Replace with your MQTT broker address
port = 1883  # Default MQTT port
topic = 'bme'  # The MQTT topic you want to subscribe to
username = "vosko"
password = "vosko"

# Callback when the client connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT Broker ({broker_address}:{port})")
        client.subscribe(topic)
    else:
        print(f"Connection failed with code {rc}")

# Callback when a message is received from the MQTT broker
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(f"Received message on topic '{message.topic}': {payload}")

# Create an MQTT client
client = mqtt.Client()

# Set username and password
client.username_pw_set(username, password)

# Set up callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(broker_address, port, keepalive=60)

# Start the MQTT client's loop
client.loop_forever()