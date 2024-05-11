import os
import random
import time
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)

# May try with IoT direct methods
import re
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod, CloudToDeviceMethodResult, Twin


app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

CONNECTION_STR = 'HostName=PiTelemtry.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=dPdh+S7KaQxMm0ho4UQ4O/6ZllMUqECY4AIoTIZWlvA='
DEVICE_ID = 'TheRaspPi'
default_loc = "33.621955642487734,72.95814350678089"
MSG_TXT = "{\"service client sent a message\": %.2f}"

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

def parse_direction(direction):
    match = re.match(
        r'(east|west|north|south|left|right|U-turn),\s*([\d.]+)\s*(km|m)', direction, re.I)
    direction = direction.split(':')[1]
    if match:
        action = match.group(1).lower()
        value = float(match.group(2))
        unit = match.group(3).lower() if match.group(3) else 'm'
        if unit == 'km':
            value *= 1000
        return action, value
    else:
        raise ValueError("Invalid direction format: {}".format(direction))
   
@app.route('/data', methods=['POST'])
def receive_data_from_JS():
    global Directions
    direction_val = request.json
    out_str = ""
    if re.match(r'Dir:(left|right|up|down)', direction_val, re.I):
        print('Manual_Control')
        Directions = direction_val

    elif direction_val != "" or direction_val != Directions:
        Directions = direction_val
        parts = Directions.split('\n')
        for i in parts:
            if i == "":
                continue
            # action, value = parse_direction(i)
            # print(action, " = ", value)
            # out_str += action + '=' + str(value) + ','

    print("current value: ", Directions)
    response_data = {"message": Directions}
    print(response_data)
        # Sending data to Pi
    try:
        registry_manager = IoTHubRegistryManager(CONNECTION_STR)
        print(response_data)
        registry_manager.send_c2d_message(DEVICE_ID, Directions)
    except Exception as ex:
        print ( "Unexpected error {0}" % ex )

    except KeyboardInterrupt:
        print ( "IoT Hub C2D Messaging service sample stopped" )

    return jsonify(response_data)

# async def receive_events():
#     client = EventHubConsumerClient.from_connection_string(
#         conn_str=CONNECTION_STR,
#         consumer_group='$Default'
#     )

#     async with client:
#         try:
#             async def on_event_batch(partition_context, events):
#                 for event in events:
#                     print("Received event from partition: {}.".format(partition_context.partition_id))
#                     print("Telemetry received: ", event.body_as_str())
#                     current_loc = event.body_as_str()
#                     # Process event data here (optional)
#                     # You can extract and use the data from event.body_as_str() or event.properties
#                     # ...

#                 await partition_context.update_checkpoint()

#             async def on_error(partition_context, error):
#                 print(f"An error occurred: {error}")
#                 # Handle errors appropriately (e.g., log or retry)

#             await client.receive_batch(on_event_batch=on_event_batch, on_error=on_error)

#         except Exception as e:
#             print(f"An unexpected error occurred: {e}")
def iothub_devicemethod_GPS():
    METHOD_NAME = "GPS"
    METHOD_PAYLOAD = "{\"method_number\":\"42\"}"
    TIMEOUT = 60
    WAIT_COUNT = 10

    try:
        # Create IoTHubRegistryManager
        registry_manager = IoTHubRegistryManager(CONNECTION_STR)
        print('\n Connection with device Established')

        # Call the direct method.
        deviceMethod = CloudToDeviceMethod(method_name=METHOD_NAME, payload=METHOD_PAYLOAD)
        response = registry_manager.invoke_device_method(DEVICE_ID, deviceMethod)

        print ( "\n Successfully invoked the device to return GPS data. Payload: " )
        print ( response.payload )
        return response.payload
    except:
        print('Error !!!!!!')
        return {'Response': default_loc}


@app.route('/sendDataToJS', methods=['GET'])
def send_data_to_JS():
    # Current = [round(random.uniform(33.621, 33.622), 6),
    #         round(random.uniform(72.95, 72.96), 6)]
    # time.sleep(1.5)
    # print('Waiting to recieve event')
    # await receive_events()
    # print('Finally recieved EVENT')
    # Current = current_loc.split(',')
    Current  = iothub_devicemethod_GPS()
    current_cords = Current['Response'].split(',')
    response_data = {"message": f'{current_cords[0]},{current_cords[1]}'}#{"message": f'Latitude: {Current[0]}\nLongitude: {Current[1]}'}
    #print(response_data)
    default_loc = Current
    return jsonify(response_data)

if __name__ == '__main__':
   app.run()
