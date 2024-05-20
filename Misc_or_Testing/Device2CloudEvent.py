import asyncio
from azure.eventhub.aio import EventHubConsumerClient

CONNECTION_STR = "{IoT_Hub_endpoint}"
async def on_event_batch(partition_context, events):
    for event in events:
        print("Received event from partition: {}.".format(partition_context.partition_id))
        print("Telemetry received: ", event.body_as_str())
        print("Properties (set by device): ", event.properties)
        print("System properties (set by IoT Hub): ", event.system_properties)
        print()
    await partition_context.update_checkpoint()

async def on_error(partition_context, error):
    # Put your code here. partition_context can be None in the on_error callback.
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            error,
            partition_context.partition_id
        ))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


def main():
    loop = asyncio.get_event_loop()
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
    try:
        loop.run_until_complete(client.receive_batch(on_event_batch=on_event_batch, on_error=on_error))
    except KeyboardInterrupt:
        print("Receiving has stopped.")
    finally:
        loop.run_until_complete(client.close())
        loop.stop()
    

if __name__ == '__main__':
    main()