# -*- coding: utf-8 -*-
"""
The ExceptionSerializer class is used for serializing exceptions in Javonet.
"""

import os
import sys
import traceback

from javonet.utils.PythonStringBuilder import PythonStringBuilder
from javonet.utils.ExceptionType import ExceptionType
from javonet.utils.Command import Command
from javonet.utils.CommandType import CommandType


class ExceptionSerializer(object):
    """
    Class for serializing exceptions in Javonet.
    """

    Exception = 0
    IOException = 1
    FileNotFoundException = 2
    RuntimeException = 3
    ArithmeticException = 4
    IllegalArgumentException = 5
    IndexOutOfBoundsException = 6
    NullPointerException = 7

    @staticmethod
    def serialize_exception(exception, command):
        """
        Serializes an exception to Javonet command format.

        :param exception: Exception to serialize
        :param command: Command that caused the exception
        :return: Command containing the serialized exception
        """
        exception_command = Command(command.runtime_name, CommandType.Exception, [])
        
        # In Python 2 there's no __traceback__, we use sys.exc_info()
        _, _, tb = sys.exc_info()
        trace = traceback.extract_tb(tb)
        exception_message = str(exception)
        
        # In Python 2 there's no __cause__, we use the exception type directly
        exception_name = exception.__class__.__name__
        
        stack_classes = PythonStringBuilder()
        stack_methods = PythonStringBuilder()
        stack_lines = PythonStringBuilder()
        stack_files = PythonStringBuilder()

        is_debug = False

        for frame in trace:
            # In Python 2 extract_tb returns tuples (filename, line number, function name, text)
            filename, lineno, name, _ = frame
            if "javonet" not in filename or is_debug:
                stack_classes.append(ExceptionSerializer.format_class_name_from_file(filename)).append("|")
                stack_methods.append(name).append("|")
                stack_lines.append(str(lineno)).append("|")
                stack_files.append(filename).append("|")

        exception_command = exception_command.add_arg_to_payload(ExceptionSerializer.get_exception_code(exception_name))
        exception_command = exception_command.add_arg_to_payload(str(command))
        exception_command = exception_command.add_arg_to_payload(exception_name)
        exception_command = exception_command.add_arg_to_payload(str(exception_message))
        exception_command = exception_command.add_arg_to_payload(stack_classes.__str__())
        exception_command = exception_command.add_arg_to_payload(stack_methods.__str__())
        exception_command = exception_command.add_arg_to_payload(stack_lines.__str__())
        exception_command = exception_command.add_arg_to_payload(stack_files.__str__())

        return exception_command

    @staticmethod
    def get_exception_code(exception_name):
        """
        Returns the exception code based on its name.

        :param exception_name: Exception name
        :return: Exception code
        """
        return ExceptionType.to_enum(exception_name)

    @staticmethod
    def format_class_name_from_file(filename):
        """
        Formats the class name based on the file name.

        :param filename: File name
        :return: Class name
        """
        return os.path.splitext((os.path.split(filename)[1]))[0] 