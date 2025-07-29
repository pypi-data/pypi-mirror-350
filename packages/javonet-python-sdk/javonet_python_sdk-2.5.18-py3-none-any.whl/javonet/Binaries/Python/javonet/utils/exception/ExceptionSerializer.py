import os
import traceback

from javonet.utils.ExceptionType import ExceptionType
from javonet.utils.Command import Command
from javonet.utils.CommandType import CommandType


class ExceptionSerializer:

    @staticmethod
    def serialize_exception(exception, command):
        exception_command = Command(command.runtime_name, CommandType.Exception, [])
        tb = exception.__traceback__
        trace = traceback.extract_tb(tb)
        exception_message = str(exception)
        exception_name = exception.__cause__.__class__.__name__

        # Use lists to collect strings, then join using the pipe separator.
        stack_classes = []
        stack_methods = []
        stack_lines = []
        stack_files = []

        is_debug = False

        for frame_summary in trace:
            if "javonet" not in frame_summary.filename or is_debug:
                stack_classes.append(ExceptionSerializer.format_class_name_from_file(frame_summary.filename))
                stack_methods.append(frame_summary.name)
                stack_lines.append(str(frame_summary.lineno))
                stack_files.append(frame_summary.filename)

        # Join list items with '|' and add a trailing '|' if needed.
        stack_classes_str = "|".join(stack_classes) + "|" if stack_classes else ""
        stack_methods_str = "|".join(stack_methods) + "|" if stack_methods else ""
        stack_lines_str = "|".join(stack_lines) + "|" if stack_lines else ""
        stack_files_str = "|".join(stack_files) + "|" if stack_files else ""

        exception_command = exception_command.add_arg_to_payload(ExceptionSerializer.get_exception_code(exception_name))
        exception_command = exception_command.add_arg_to_payload(str(command))
        exception_command = exception_command.add_arg_to_payload(exception_name)
        exception_command = exception_command.add_arg_to_payload(str(exception_message))
        exception_command = exception_command.add_arg_to_payload(stack_classes_str)
        exception_command = exception_command.add_arg_to_payload(stack_methods_str)
        exception_command = exception_command.add_arg_to_payload(stack_lines_str)
        exception_command = exception_command.add_arg_to_payload(stack_files_str)

        return exception_command

    @staticmethod
    def get_exception_code(exception_name):
        return ExceptionType.to_enum(exception_name)

    Exception = 0
    IOException = 1
    FileNotFoundException = 2
    RuntimeException = 3
    ArithmeticException = 4
    IllegalArgumentException = 5
    IndexOutOfBoundsException = 6
    NullPointerException = 7

    @staticmethod
    def format_class_name_from_file(filename):
        return os.path.splitext(os.path.split(filename)[1])[0]