""" This modules contains classes for handling commands. 

Commands are strings sent over TCP sockets. 
They are parsed into a command type and associated data.

Copyright 2023 [Devin Headrick]. Licensed under the Apache License, Version 2.0
"""

# import to support abstract classes
from abc import ABC, abstractmethod # pylint: disable=unused-import


COMMAND_DELIMITER = ':'

# Abstract command factory class - subsystems extend this class based
# on the commands they support
class CommandFactory(): # pylint: disable=too-few-public-methods
    """Factory class to create command objects based on command type"""

    @abstractmethod
    def create_command(self, command_type):
        """Abstract method to create a command object based on command type
        Args:
            command_type (str): The type of command to be created

        Returns:
            Command: A command object of the associated command type
        """


class CommandHandler():
    """This takes a client socket arg and uses it to listen for commands
    
    This class can be used by various subsystems that are 'intelligent'.  
    They may listen for commands from the client socket and process them. 
    """
    client_socket = None

    def __init__(self, command_factory):
        self.command_factory = command_factory

    def set_client_socket(self, client_socket):
        """Set the client socket.

        This method is used to set the client socket after the object has been created.
        Because connection is handled by socket_stuff module, the client socket may 
        change after the object is created.

        Args:
            client_socket (socket): The client socket to use
        """
        self.client_socket = client_socket


    def handle_command(self):
        """Listen for commands from the client socket and processes them"""
        while True:
            try:
                data = self.client_socket.recv(1024).decode().strip()
                if data:
                    print("RAW data received: " + data, flush=True)
                    parsed_command = self.parse_command(data)
                    self.process_command(parsed_command)

                else:
                    break

            except BrokenPipeError:
                print("Client disconnected abruptly", flush=True)
                break

        self.client_socket.close()

    def parse_command(self, command):
        """Parse the command into consituent command type, and associated data

        Args:
            command (str): A decoded and stripped string containing the command

        Returns:
            str: A parsed string containing the command
        """

        return command.split(COMMAND_DELIMITER)

    def process_command(self, command):
        """Process command data based on the command type

        Args:
            command_type (str): The type of command to be processed
            params (list): The associated data for the command

        Returns:
            str: A string containing the response to the command
        """

        command_type = command[0]
        params = command[1:]

        # command_factory = CommandFactory()
        command_obj = self.command_factory.create_command(command_type)

        if command_obj is not None:
            response = command_obj.execute(params)
        else:
            response = "ERROR: Invalid command type \0"

        try:
            self.client_socket.sendall(response.encode())

        except BrokenPipeError:
            print("Client disconnected abruptly")
            self.client_socket.close()


# pylint: disable=duplicate-code
# no error
__author__ = "Devin Headrick"
__copyright__ = """
    Copyright 2023 [Devin Headrick]
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."""
