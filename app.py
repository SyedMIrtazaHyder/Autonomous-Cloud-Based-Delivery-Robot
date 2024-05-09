import os
import random
import time
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, jsonify)
import re
import asyncio
from azure.eventhub.aio import EventHubConsumerClient

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

CONNECTION_STR = 'Endpoint=sb://iothub-ns-pitelemtry-55140772-9f69bdc475.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=dPdh+S7KaQxMm0ho4UQ4O/6ZllMUqECY4AIoTIZWlvA=;EntityPath=pitelemtry'

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

def parse_direction(direction):
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
def receive_data_from_JS():
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


# @app.route('/sendDataToJS', methods=['GET'])
# def send_data_to_JS():
#     Current = [round(random.uniform(79, 80), 6),
#             round(random.uniform(79, 80), 6)]
#     time.sleep(1.5)
#     response_data = {"message": f'Latitude: {Current[0]}\nLongitude: {Current[1]}'}
#     print(response_data)
#     return jsonify(response_data)

@app.route('/sendDataToJS', methods=['GET'])

async def get_data():
  # Perform asynchronous tasks here
  # For example, simulate a network request with asyncio
    #   async def simulate_network_request():
    #     await asyncio.sleep(2)  # Simulate a 2-second delay
    #     return {'message': 'Data retrieved successfully!'}
    client = EventHubConsumerClient.from_connection_string(
    conn_str=CONNECTION_STR,
    consumer_group="$Default",
    # transport_type=TransportType.AmqpOverWebsocket,  # uncomment it if you want to use web socket
    # http_proxy={  # uncomment if you want to use proxy 
    #     'proxy_hostname': '127.0.0.1',  # proxy hostname.
    #     'proxy_port': 3128,  # proxy port.
    #     'username': '<proxy user name>',
    #     'password': '<proxy password>'
    # }
    )
    async def on_event_batch(partition_context, events):
        for event in events:
            Current = event.body_as_str()
            print('Telemtry recieved: ', Current.split(','))
            response_data = {"message": f'Latitude: {Current[0]}\nLongitude: {Current[1]}'}
        await partition_context.update_checkpoint()
        return response_data

    async def on_error(partition_context, error):
        # Put your code here. partition_context can be None in the on_error callback.
        if partition_context:
            print("An exception: {} occurred during receiving from Partition: {}.".format(
                error,
                partition_context.partition_id
            ))
        else:
            print("An exception: {} occurred during the load balance process.".format(error))

    try:
        data = client.receive_batch(on_event_batch=on_event_batch, on_error=on_error)
        return jsonify(data)
    except:
        print("Some Error occured")



if __name__ == '__main__':
   app.run()