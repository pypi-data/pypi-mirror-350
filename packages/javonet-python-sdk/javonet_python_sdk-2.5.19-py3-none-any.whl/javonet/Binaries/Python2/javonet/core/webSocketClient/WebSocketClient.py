"""
The WebSocketClient module implements a WebSocket client.
"""

import struct
from websockets.sync.client import connect

from javonet.utils.connectionData.WsConnectionData import WsConnectionData


class WebSocketClient(object):
    """
    Class implementing a WebSocket client.
    """

    def send_message(self, connection_data, serialized_command):
        """
        Sends a message through WebSocket.

        :param connection_data: Connection data
        :param serialized_command: Serialized command
        :return: Server response
        """
        byte_array = struct.pack("B" * len(serialized_command), *serialized_command)
        return self.send(connection_data, byte_array)

    def send(self, connection_data, byte_array):
        """
        Sends data through WebSocket.

        :param connection_data: Connection data
        :param byte_array: Byte array to send
        :return: Server response
        """
        websocket = connect(connection_data.hostname)
        websocket.send(byte_array)
        response = websocket.recv()
        websocket.close()
        return response 