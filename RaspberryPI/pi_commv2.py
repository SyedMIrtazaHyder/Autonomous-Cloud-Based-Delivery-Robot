import random
import time
import pynmea2
import serial
from azure.iot.device import IoTHubDeviceClient, MethodResponse
import Raspberry_to_Arudino as driver
import re

CONNECTION_STRING = "{IoT_Hub_Shared_Access_Key}"
RECEIVED_MESSAGES = 0

def GPS_reading():
    port = "/dev/ttyAMA0"
    ser = serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata = ser.readline().decode("utf-8", errors="ignore")
    print(newdata)
    if newdata[0:6] == "$GPRMC":
        newmsg = pynmea2.parse(newdata)
        lat = newmsg.latitude
        lng = newmsg.longitude
        Current = str(round(lat, 6)) + "," + str(round(lng, 6))
        print(Current)
    # Temp to send data
    else:
        Current = "33.621955642487734,72.95814350678089" #default location
    return Current

def parse_direction(direction):
    match = re.match(
        r'(east|west|north|south|left|right),\s*([\d.]+)\s*(km|m)', direction, re.I)
    if match:
        action = match.group(1).lower()
        value = float(match.group(2))
        unit = match.group(3).lower() if match.group(3) else 'm'
        # Convert distance to meters if the unit is in kilometers
        if unit == 'km':
            value *= 1000
        return action, value
    else:
        raise ValueError("Invalid direction format: {}".format(direction))
    
def create_client():
    # Instantiate the client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    
    # Define the handler for method requests
    def method_request_handler(method_request):
        if method_request.name == "GPS":
            print('GPS request recieved')
            lat = round(random.uniform(1, 100), 2)
            lng = round(random.uniform(1, 100), 2)
            payload = str(round(random.uniform(33.621, 33.622), 6)) + ',' + str(round(random.uniform(72.95, 72.96), 6))
            #GPS_reading()
            print('Sending payload')
            resp_status = 200
            resp_payload = {"Response": payload}
            method_response = MethodResponse(method_request.request_id, resp_status, resp_payload)
            
        else:
            # Create a method response indicating the method request was for an unknown method
            resp_status = 404
            resp_payload = {"Response": "Unknown method"}
            method_response = MethodResponse(method_request.request_id, resp_status, resp_payload)

        # Send the method response
        client.send_method_response(method_response)

    def message_listener(message):
        global RECEIVED_MESSAGES
        print(f"Received message: {message.data}")
        RECEIVED_MESSAGES += 1
        instrc = message.data[:4].decode('utf-8')
        print(instrc)
        if instrc == 'Path':
            path_to_navigate = message.data[5:].decode('utf-8')
            print(path_to_navigate)
            #for i in path_to_navigate:
                #if i == "":
                #    continue
                #action, value = parse_direction(i)
                #print(action, " = ", value)
                # Add path decryting logic here
                #driver.run_driver(action, value) 
        elif instrc == 'Dir:':
            action = message.data[4:].decode('utf-8')
            print(action)
            value = 1
            if action == 'up':
                driver.straight()
            elif action == 'down':
                driver.back()
            elif action == "right":
                driver.right()
            elif action == "left":
                driver.left()
            driver.stop()

    try:
        # Attach the handler to the client
        print('Connecting Client')
        client.connect()
        print('Client Connected')
        client.on_method_request_received = method_request_handler
        client.on_message_received = message_listener

    except:
        print('ERROR')
        # In the event of failure, clean up
        client.shutdown()

    return client

def main():
    print ("Starting..")
    client = create_client()

    print ("Waiting for commands, press Ctrl-C to exit")
    try:
        # Wait for program exit
        while True:
            time.sleep(1000) # time in seconds
    except KeyboardInterrupt:
        print("IoTHubDeviceClient sample stopped")
    finally:
        # Graceful exit
        print("Shutting down IoT Hub Client")
        client.shutdown()

if __name__ == '__main__':
    main()
