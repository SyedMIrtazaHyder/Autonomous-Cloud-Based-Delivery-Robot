import os
import random
import time
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)

# May try with IoT direct methods
import re
from azure.eventhub import EventHubConsumerClient, TransportType

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

CONNECTION_STR = 'Endpoint=sb://iothub-ns-pitelemtry-55140772-9f69bdc475.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=dPdh+S7KaQxMm0ho4UQ4O/6ZllMUqECY4AIoTIZWlvA=;EntityPath=pitelemtry'
current_loc = 'Nowhere,Nowhere'

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

async def parse_direction(direction):
    match = re.match(
        r'(east|west|north|south|left|right|U-turn),\s*([\d.]+)\s*(km|m)', direction, re.I)
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
async def receive_data_from_JS():
    global Directions
    direction_val = request.json
    if direction_val != "" or direction_val != Directions:
        Directions = direction_val
        parts = Directions.split('\n')
        for i in parts:
            if i == "":
                continue
            action, value = parse_direction(i)
            print(action, " = ", value)


        response_data = {"message": Directions}
        return jsonify(response_data)

async def receive_events():
    client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group='$Default'
    )

    async with client:
        try:
            async def on_event_batch(partition_context, events):
                for event in events:
                    print("Received event from partition: {}.".format(partition_context.partition_id))
                    print("Telemetry received: ", event.body_as_str())
                    current_loc = event.body_as_str()
                    # Process event data here (optional)
                    # You can extract and use the data from event.body_as_str() or event.properties
                    # ...

                await partition_context.update_checkpoint()

            async def on_error(partition_context, error):
                print(f"An error occurred: {error}")
                # Handle errors appropriately (e.g., log or retry)

            await client.receive_batch(on_event_batch=on_event_batch, on_error=on_error)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

@app.route('/sendDataToJS', methods=['GET'])
async def send_data_to_JS():
    # Current = [round(random.uniform(79, 80), 6),
    #         round(random.uniform(79, 80), 6)]
    # time.sleep(1.5)
    print('Waiting to recieve event')
    await receive_events()
    print('Finally recieved EVENT')
    Current = current_loc.split(',')
    response_data = {"message": f'Latitude: {Current[0]}\nLongitude: {Current[1]}'}
    print(response_data)
    return jsonify(response_data)

if __name__ == '__main__':
   app.run()
