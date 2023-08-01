"""This python program represents a simulated version of the IRIS payload component for ExAlta3.

For now the sub system communicates with strings over a TCP socket. The strings are parsed into a
command type and associated data.

Until we know more system specs I am assuming there are three types of commands that can be sent:
    - Request - Request a paramater from the state dictionary
    - Update  - Update a parameter in the state dictionary
    - Execute - Execute a command (e.g. reset watchdog timer)

# Example to toggle the sensors on:
     update:SensorStatus:1

# Example to request the temperature of the visible-light sensor:
    request:TempVIS

# Example to use the camera:
    execute:TakeImage

For now you can test your commands using netcat (nc) from the command line,
for instance, nc localhost 1801 <<< text

Usage: ESP_component.py non-default_port_num

Copyright 2023 [Abhishek Naik]. Licensed under the Apache License, Version 2.0
"""

import sys
import socket


DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1801
COMMAND_DELIMITER = ':'

default_iris_state = {
    'PowerStatus': 1,           # 1 means powered on, 0 means off
    'SensorStatus': 0,          # 1 means sensors are on, 0 means off
    'TempVIS': 25,              # in degree Celsius
    'TempNIR': 25,              # in degree Celsius
    'TempFLASH': 25,            # in degree Celsius
    'TempGATE': 25,             # in degree Celsius
    'NumImages': 5,             # number of images
    'SoftwareVersion': 1.0
}

iris_state = default_iris_state


class RequestDataCommand():  # pylint: disable=too-few-public-methods
    """Execute a 'request' type command to get the current value of a parameter"""

    def execute(self, params=None):
        """
        Args:
            params (list): Name of the parameter to request from the IRIS subsystem state
        Returns:
            str: A string containing the requested parameter and its associated value
        """
        print("Request command received: " + params[0])
        if params and len(params) == 1 and params[0] in iris_state:
            return f"{params[0]}:{iris_state[params[0]]}\n"
        return "ERROR: Invalid request command \n"


class UpdateParameterCommand():  # pylint: disable=too-few-public-methods
    """Execute an 'update' type command to update a parameter value

    Updateable parameters are defined in the updateable_parameters tuple.
    """

    updatable_parameters = ['PowerStatus', 'SensorStatus']

    def execute(self, params=None):
        """
        Args:
            params (list): Name of the state parameter to update, and the new value

        Returns:
            str: A string containing the updated parameter and its new value
        """

        print("Update command received: " + params[0])
        if params and len(params) == 2 and params[0] in self.updatable_parameters:
            iris_state[params[0]] = params[1]
            return f"Updated {params[0]} to {params[1]}\n"
        return "ERROR: update command \n"


class ExecuteCommand():  # pylint: disable=too-few-public-methods
    """Execute an 'execute' type command to call a function (do something)

    Executable commands are defined in the executable_commands tuple.
    """

    executable_commands = ['TakeImage', 'SetTime']

    def execute(self, params=None):
        """
        Args:
            params (list): Name of the function to call

        Returns:
            str: A string containing the return value from the function call
        """

        print("Execute command received: " + params[0])
        if params and len(params) == 1 and params[0] in self.executable_commands:
            return f"Command {params[0]} executed \n"
        return "ERROR: Invalid execute command \n"


# Factory pattern: Command Factory
class CommandFactory:  # pylint: disable=too-few-public-methods
    """Factory class to create command objects based on command type"""

    def create_command(self, command_type):
        """Create a command object based on the command type
        Args:
            command_type (str): The type of command to be created

        Returns:
            Command: A command object of the associated command type
        """

        if command_type == 'request':
            return RequestDataCommand()
        if command_type == 'update':
            return UpdateParameterCommand()
        if command_type == 'execute':
            return ExecuteCommand()
        return None


class IRISCommandHandler:
    """This takes a client socket arg and uses it to listen for commands"""

    def __init__(self, client_socket):
        self.client_socket = client_socket

    def handle_command(self):
        """Listen for commands from the client socket and processes them"""
        while True:
            try:
                data = self.client_socket.recv(1024).decode().strip()
                parsed_command = self.parse_command(data)
                self.process_command(parsed_command)

            except KeyboardInterrupt:
                break

            except BrokenPipeError:
                print("Client disconnected abruptly")
                break

        self.client_socket.close()

    def parse_command(self, command):
        """Parse the command into consituent command type, and associated data

        Args:
            command (str): A decoded and stripped string containing the command

        Returns:
            str: A decoded and stripped string containing the command
        """
        return command.split(COMMAND_DELIMITER)

    def process_command(self, command):
        """Process command data based on the command type

        Command types are either: update, request, or execute. This function
        relies on the pattern factory to creates a command object for the
        associated command type.

        Args:
            command_type (str): The type of command to be processed
            params (list): The associated data for the command

        Returns:
            str: A string containing the response to the command
        """

        command_type = command[0]
        params = command[1:]

        command_factory = CommandFactory()
        command_obj = command_factory.create_command(command_type)

        if command_obj is not None:
            response = command_obj.execute(params)
        else:
            response = "ERROR: Invalid command type \n"

        try:
            self.client_socket.sendall(response.encode())
        except BrokenPipeError:
            print("Client disconnected abruptly")
            self.client_socket.close()


if __name__ == "__main__":
    # If there is no arg, port is default otherwise use the arg
    PORT = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT

    print(f"Starting IRIS subsystem on port {PORT}")

    # Create a socket and bind it to the port. Listen indefinitely for client connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Tell OS to reuse socket addr if not previously closed
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((DEFAULT_HOST, int(PORT)))
        s.listen()
        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected with {addr}")
                    handler = IRISCommandHandler(conn)
                    handler.handle_command()

            except BrokenPipeError as e:
                print(f"Client connection closed: {e}")


# pylint: disable=duplicate-code
# no error
__author__ = "Devin Headrick"
__copyright__ = """
    Copyright (C) 2023, University of Alberta.
    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details."""
