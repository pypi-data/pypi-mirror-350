import time
import websockets
import numpy as np
import pandas as pd
import lz4.frame as lz4f
import asyncio
import struct
import json


from SharedData.Logger import Logger
from SharedData.IO.SyncTable import SyncTable


class ClientWebSocket():

    """
    '''
    ClientWebSocket provides asynchronous static methods to manage WebSocket connections for subscribing to and publishing data tables.
    
    Methods:
        subscribe_table_thread(table, host, port, lookbacklines=1000, lookbackdate=None, snapshot=False, bandwidth=1e6):
            Continuously attempts to connect to a WebSocket server at the specified host and port to subscribe to updates for a given data table.
            Sends a subscription message and maintains the subscription loop, handling reconnection on errors with a delay.
    
        publish_table_thread(table, host, port, lookbacklines=1000, lookbackdate=None, snapshot=False, bandwidth=1e6):
            Continuously attempts to connect to a WebSocket server at the specified host and port to publish data for a given table.
            Sends a publish message, processes the initial response, and maintains the publishing loop, handling reconnection on errors with a delay.
    
    Parameters for both methods:
        table: The data table object to subscribe or publish.
        host (str): The WebSocket server hostname or IP address.
        port (int): The WebSocket server port number.
        lookbacklines (int, optional): Number of historical lines to request on subscription/publish. Default is 1000.
        lookback
    """
    @staticmethod
    async def subscribe_table_thread(table, host, port,
            lookbacklines=1000, lookbackdate=None, snapshot=False, bandwidth=1e6):

        """
        Asynchronously subscribes to a specified data table via a WebSocket connection, handling reconnections and data streaming.
        
        Parameters:
            table: The data table object to subscribe to.
            host (str): The hostname of the WebSocket server.
            port (int): The port number of the WebSocket server.
            lookbacklines (int, optional): Number of historical lines to retrieve on subscription. Default is 1000.
            lookbackdate (optional): Date from which to start retrieving historical data. Default is None.
            snapshot (bool, optional): Whether to request a snapshot of the current data. Default is False.
            bandwidth (float, optional): Bandwidth limit for the subscription in bits per second. Default is 1e6.
        
        This coroutine continuously attempts to establish a WebSocket connection to the specified server,
        sends a subscription message for the given table, initializes the client, and enters a subscription loop
        to receive data. If the connection fails or an exception occurs, it logs a warning and retries after a delay.
        """
        while True:
            try:
                # Connect to the server
                async with websockets.connect(f"ws://{host}:{port}") as websocket:

                    # Send the subscription message
                    msg = SyncTable.subscribe_table_message(
                        table, lookbacklines, lookbackdate, snapshot, bandwidth)
                    msgb = msg.encode('utf-8')
                    await websocket.send(msgb)

                    # Subscription loop
                    client = json.loads(msg)
                    client['conn'] = websocket
                    client['addr'] = (host, port) 
                    client = SyncTable.init_client(client,table)
                    await SyncTable.websocket_subscription_loop(client)
                    time.sleep(15)

            except Exception as e:
                msg = 'Retrying subscription %s,%s,%s,table,%s!\n%s' % \
                    (table.database, table.period,
                     table.source, table.tablename, str(e))
                Logger.log.warning(msg)
                time.sleep(15)
    
    @staticmethod
    async def publish_table_thread(table, host, port,
            lookbacklines=1000, lookbackdate=None, snapshot=False, bandwidth=1e6):

        """
        '''
        Asynchronously maintains a persistent WebSocket connection to publish updates from a specified table.
        
        This coroutine continuously attempts to connect to a WebSocket server at the given host and port,
        subscribes to updates for the specified table with optional parameters such as lookback lines,
        lookback date, snapshot mode, and bandwidth limit. Upon successful subscription, it listens for
        incoming messages and processes them in a publish loop. If the connection is lost or an error
        occurs, it logs the issue and retries the subscription after a delay.
        
        Parameters:
            table (Table): The table object containing database, period, source, and tablename attributes.
            host (str): The hostname or IP address of the WebSocket server.
            port (int): The port number of the WebSocket server.
            lookbacklines (int, optional): Number of historical lines to retrieve on subscription. Default is 1000.
            lookbackdate (str or None, optional): Date string to specify the starting point for historical data. Default is None.
            snapshot (bool, optional): Whether to request a snapshot of the current table state. Default is False.
            bandwidth (float, optional): Bandwidth limit for the subscription in bits per second. Default is 1e6.
        
        Raises
        """
        while True:
            try:
                # Connect to the server
                async with websockets.connect(f"ws://{host}:{port}") as websocket:

                    # Send the subscription message
                    msg = SyncTable.publish_table_message(
                        table, lookbacklines, lookbackdate, snapshot, bandwidth)
                    msgb = msg.encode('utf-8')
                    await websocket.send(msgb)

                    response = await websocket.recv()
                    if response == b'':
                        msg = 'Subscription %s,%s,%s,table,%s closed  on response!' % \
                            (table.database, table.period,
                                table.source, table.tablename)
                        Logger.log.error(msg)
                        websocket.close()
                        break

                    response = json.loads(response)
                    
                    # Subscription loop
                    client = json.loads(msg)
                    client['conn'] = websocket
                    client['table'] = table
                    client['addr'] = (host, port)
                    client.update(response)
                    client = SyncTable.init_client(client,table)
                    
                    await SyncTable.websocket_publish_loop(client)
                    time.sleep(15)

            except Exception as e:
                msg = 'Retrying subscription %s,%s,%s,table,%s!\n%s' % \
                    (table.database, table.period,
                     table.source, table.tablename, str(e))
                Logger.log.warning(msg)
                time.sleep(15)


if __name__ == '__main__':
    import sys
    from SharedData.Logger import Logger
    from SharedData.SharedData import SharedData
    shdata = SharedData('SharedData.IO.ClientWebSocket', user='master')

    if len(sys.argv) >= 2:
        _argv = sys.argv[1:]
    else:
        msg = 'Please specify IP and port to bind!'
        Logger.log.error(msg)
        raise Exception(msg)

    args = _argv[0].split(',')
    host = args[0]
    port = int(args[1])
    database = args[2]
    period = args[3]
    source = args[4]
    tablename = args[5]
    if len(args) > 6:
        pubsub = int(args[6])
    
    table = shdata.table(database, period, source, tablename)
    if pubsub == 'publish':
        table.publish(host, port)
    elif pubsub == 'subscribe':
        table.subscribe(host, port)

    while True:
        time.sleep(1)        
