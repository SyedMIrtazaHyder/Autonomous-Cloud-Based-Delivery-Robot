import random
from azure.iot.device import IoTHubDeviceClient, MethodResponse

CONNECTION_STRING = "{IoT_Hub_Connection_String}"
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
            # ...and patching the reported properties
            # current_time = str(datetime.datetime.now())
            # reported_props = {"rebootTime": current_time}
            # client.patch_twin_reported_properties(reported_props)
            # print( "Device twins updated with latest rebootTime")

            # Create a method response indicating the method request was resolved
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

    try:
        # Attach the handler to the client
        client.on_method_request_received = method_request_handler
    except:
        # In the event of failure, clean up
        client.shutdown()

    return client

def main():
    print ("Starting the IoT Hub Python sample...")
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