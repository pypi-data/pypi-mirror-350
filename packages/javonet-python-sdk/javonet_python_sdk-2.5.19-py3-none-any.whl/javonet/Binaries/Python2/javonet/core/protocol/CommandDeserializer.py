# -*- coding: utf-8 -*-
"""
The CommandDeserializer module implements command deserialization.
"""

from javonet.core.protocol.TypeDeserializer import TypeDeserializer
from javonet.utils.Command import Command
from javonet.utils.CommandType import CommandType
from javonet.utils.RuntimeName import RuntimeName
from javonet.utils.Type import Type
from javonet.utils.StringEncodingMode import StringEncodingMode


class CommandDeserializer(object):
    """
    Class responsible for command deserialization.
    """
    position = 0
    buffer = []
    command = 0
    buffer_len = 0

    def __init__(self, buffer):
        """
        Initializes a new command deserializer.

        :param buffer: Buffer with data to deserialize
        """
        self.buffer = buffer
        self.buffer_len = len(buffer)
        self.command = Command(RuntimeName(buffer[0]), CommandType(buffer[10]), [])
        self.position = 11

    def is_at_end(self):
        """
        Checks if the end of buffer has been reached.

        :return: True if end of buffer is reached, False otherwise
        """
        return self.position == self.buffer_len

    def deserialize(self):
        """
        Deserializes a command.

        :return: Deserialized command
        """
        while not self.is_at_end():
            self.command = self.command.add_arg_to_payload(self.read_object(self.buffer[self.position]))
        return self.command

    def read_object(self, type_num):
        """
        Reads an object from the buffer based on its type.

        :param type_num: Type number
        :return: Read object
        """
        type_value = Type(type_num)
        switch = {
            Type.Command: self.read_command,
            Type.JavonetString: self.read_string,
            Type.JavonetInteger: self.read_int,
            Type.JavonetBoolean: self.read_bool,
            Type.JavonetFloat: self.read_float,
            Type.JavonetByte: self.read_byte,
            Type.JavonetChar: self.read_char,
            Type.JavonetLongLong: self.read_longlong,
            Type.JavonetDouble: self.read_double,
            Type.JavonetUnsignedLongLong: self.read_ullong,
            Type.JavonetUnsignedInteger: self.read_uint,
            Type.JavonetNoneType: self.read_none
        }
        return switch.get(type_value, lambda: Exception("Type not supported"))()

    def read_command(self):
        """
        Reads a command from the buffer.

        :return: Read command
        """
        p = self.position
        number_of_elements_in_payload = TypeDeserializer.deserialize_int(self.buffer[p + 1: p + 5])
        runtime = self.buffer[p + 5]
        command_type = self.buffer[p + 6]
        self.position += 7
        return_command = Command(RuntimeName(runtime), CommandType(command_type), [])
        return self.read_command_recursively(number_of_elements_in_payload, return_command)

    def read_command_recursively(self, number_of_elements_in_payload_left, cmd):
        """
        Recursively reads a command from the buffer.

        :param number_of_elements_in_payload_left: Number of elements left to read
        :param cmd: Command to populate
        :return: Populated command
        """
        if number_of_elements_in_payload_left == 0:
            return cmd
        else:
            p = self.position
            cmd = cmd.add_arg_to_payload(self.read_object(self.buffer[p]))
            return self.read_command_recursively(number_of_elements_in_payload_left - 1, cmd)

    def read_string(self):
        """
        Reads a string from the buffer.

        :return: Read string
        """
        p = self.position
        string_encoding_mode = StringEncodingMode(self.buffer[p + 1])
        size = TypeDeserializer.deserialize_int(self.buffer[p + 2:p + 6])
        self.position += 6
        p = self.position
        self.position += size
        return TypeDeserializer.deserialize_string(string_encoding_mode, self.buffer[p:p + size])

    def read_int(self):
        """
        Reads an integer from the buffer.

        :return: Read integer
        """
        size = 4
        self.position += 2
        p = self.position
        self.position += size
        return TypeDeserializer.deserialize_int(self.buffer[p:p + size])

    def read_bool(self):
        """
        Reads a boolean from the buffer.

        :return: Read boolean
        """
        size = 1
        self.position += 2
        p = self.position
        self.position += size
        return TypeDeserializer.deserialize_bool(self.buffer[p:p + size])

    def read_float(self):
        """
        Reads a float from the buffer.

        :return: Read float
        """
        size = 4
        self.position += 2
        p = self.position
        self.position += size
        return TypeDeserializer.deserialize_float(self.buffer[p:p + size])

    def read_byte(self):
        """
        Reads a byte from the buffer.

        :return: Read byte
        """
        size = 1
        self.position += 2
        p = self.position
        self.position += size
        return TypeDeserializer.deserialize_byte(self.buffer[p:p + size])

    def read_char(self):
        """
        Reads a character from the buffer.

        :return: Read character
        """
        size = 1
        self.position += 2
        p = self.position
        self.position += size
        return TypeDeserializer.deserialize_char(self.buffer[p:p + size])

    def read_longlong(self):
        """
        Reads a long long from the buffer.

        :return: Read long long
        """
        size = 8
        self.position += 2
        p = self.position
        self.position += size
        return TypeDeserializer.deserialize_longlong(self.buffer[p:p + size])

    def read_double(self):
        """
        Reads a double from the buffer.

        :return: Read double
        """
        size = 8
        self.position += 2
        p = self.position
        self.position += size
        return TypeDeserializer.deserialize_double(self.buffer[p:p + size])

    def read_ullong(self):
        """
        Reads an unsigned long long from the buffer.

        :return: Read unsigned long long
        """
        size = 8
        self.position += 2
        p = self.position
        self.position += size
        return TypeDeserializer.deserialize_ullong(self.buffer[p:p + size])

    def read_uint(self):
        """
        Reads an unsigned integer from the buffer.

        :return: Read unsigned integer
        """
        size = 4
        self.position += 2
        p = self.position
        self.position += size
        return TypeDeserializer.deserialize_uint(self.buffer[p:p + size])

    def read_none(self):
        """
        Reads a None value from the buffer.

        :return: Read None value
        """
        size = 1
        self.position += 2
        p = self.position
        self.position += size
        return TypeDeserializer.deserialize_none(self.buffer[p:p + size]) 