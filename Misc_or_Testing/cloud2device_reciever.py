import time
from azure.iot.device import IoTHubDeviceClient

RECEIVED_MESSAGES = 0
CONNECTION_STRING = "{deviceConnectionString}"  # Replace with your device connection string

def message_listener(message):
    global RECEIVED_MESSAGES
    print(f"Received message: {message.data}")
    RECEIVED_MESSAGES += 1

device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
device_client.on_message_received = message_listener

device_client.connect()
print("Simulated device connected. Waiting for messages...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print(f"Received {RECEIVED_MESSAGES} messages. Disconnecting...")
    device_client.disconnect()
