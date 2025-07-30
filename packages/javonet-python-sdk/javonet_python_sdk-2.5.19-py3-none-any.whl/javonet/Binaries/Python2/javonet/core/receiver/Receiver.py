"""
The Receiver module implements the message receiver.
"""

from javonet.core.interpreter.Interpreter import Interpreter
from javonet.core.protocol.CommandSerializer import CommandSerializer
from javonet.utils.RuntimeLogger import RuntimeLogger
from javonet.utils.connectionData.InMemoryConnectionData import InMemoryConnectionData
from javonet.core.protocol.CommandDeserializer import CommandDeserializer


class Receiver(object):
    """
    Class implementing the message receiver.
    """

    def __init__(self):
        self.connection_data = InMemoryConnectionData()

    def SendCommand(self, message_byte_array_as_string, messageByteArrayLen):
        message_byte_array = bytearray(message_byte_array_as_string)
        response_command = Interpreter().process(message_byte_array)
        serialized_response = CommandSerializer().serialize(response_command, self.connection_data)
        response_byte_array = bytearray(serialized_response)
        return response_byte_array

    def HeartBeat(self, message_byte_array_as_string, messageByteArrayLen):
        message_byte_array = bytearray(message_byte_array_as_string)
        response_byte_array = bytearray(2)
        response_byte_array[0] = message_byte_array[11]
        response_byte_array[1] = message_byte_array[12] - 2
        return response_byte_array

    def GetRuntimeInfo(self):
        return RuntimeLogger().get_runtime_info()