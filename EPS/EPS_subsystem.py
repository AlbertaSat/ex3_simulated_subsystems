"""
This python program represents a simulated version of the EPS payload component for ExAlta3.

For now the sub system communicates with strings over a TCP socket. The strings are parsed into a command type and associated data.

Until we know more system specifics I am assuming there are three types of commands that can be sent to the EPS subsystem:
    - Request - Request a paramater from the state dictionary
    - Update  - Update a parameter in the state dictionary
    - Execute - Execute a command (e.g. reset watchdog timer)

# Example to update the WatchdogResetTime:
     update:WatchdogResetTime:48.0

# Example to request the Voltage:
    request:Voltage

# Example to execute a ResetWatchdogTimer command:
    execute:ResetWatchdogTimer

For now you can test your commands using netcat (nc) from the command line, and piping the command to the socket from a seperate text file

Usage: ESP_component.py non-default_port_num 
"""

import sys
import socket

default_host = '127.0.0.1'
default_port = 1801
command_delimiter = ':'


default_eps_state = {
    'Temperature': 32,         # in degrees C
    'Voltage': 5.24,       # in volts
    'Current': 1.32,       # in amps
    'State': 'Charging',
    'WatchdogResetTime': 24.0,       # in hours
}

eps_state = default_eps_state


class Request_Data_Command():
    """
        Execute a 'request' type command to get the current value of a parameter from the EPS subsystem state
    """

    def execute(self, params=None):
        print("Request command received: " + params[0])
        if params and len(params) == 1 and params[0] in eps_state:
            return f"{params[0]}:{eps_state[params[0]]}"
        else:
            return "ERROR: Invalid request command \n"


class Update_Parameter_Command():
    """
        Execute an 'update' type command to update a parameter in the EPS subsystem state
        Updateable parameters are defined in the updateable_parameters tuple
    """

    updatable_parameters = ('WatchdogResetTime')

    def execute(self, params=None):
        print("Update command received: " + params[0])

        # TODO - Handle update commands that have more than one parameter
        if params and len(params) == 2 and params[0] in self.updatable_parameters:
            eps_state[params[0]] = params[1]
            return f"Updated {params[0]} to {params[1]}"
        else:
            return "ERROR: update command \n"


class Execute_Command():
    """
        Execute an 'execute' type command to execute a function in the EPS subsystem
    """

    executable_commands = ('ResetDevice')

    def execute(self, params=None):
        print("Execute command received: " + params[0])

        # TODO - Handle execute commands to call associated functions
        if params and len(params) == 1 and params[0] in self.executable_commands:

            return f"Command {params[0]} executed"
        else:
            return "ERROR: Invalid execute command \n"


# Factory pattern: Command Factory
class Command_Factory:
    def create_command(self, command_type):
        if command_type == 'request':
            return Request_Data_Command()
        elif command_type == 'update':
            return Update_Parameter_Command()
        elif command_type == 'execute':
            return Execute_Command()
        else:
            return None


class EPS_Command_Handler:
    """
        This takes a client socket arg and uses to to listen for commands
    """

    def __init__(self, client_socket):
        self.client_socket = client_socket

    # Parse the command into consituent command type, and associated data
    def handle_command(self):
        while True:
            try:
                self.data = self.client_socket.recv(1024).decode().strip()

                if self.data == "quit":
                    break

                parsed_command = self.data.split(command_delimiter)
                self.process_command(parsed_command[0], parsed_command[1:])

            except BrokenPipeError:
                print("Client disconnected abruptly")
                break

        self.client_socket.close()

    def process_command(self, command_type, params):
        """
            Process constituent command data based on command type (either an update, request, or execute)
            Relies on the pattern factory creates a command object for the associated command type
        """
        command_factory = Command_Factory()
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
    port = sys.argv[1] if len(sys.argv) > 1 else default_port

    print(f"Starting EPS subsystem on port {port}")

    # Create a socket and bind it to the port. Listen indefinitely for client connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Tell OS to reuse socket addr if not previously closed
        s.bind((default_host, int(port)))
        s.listen()
        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected with {addr}")
                    handler = EPS_Command_Handler(conn)
                    handler.handle_command()

            except Exception as e:
                print(f"Client connection closed: {e}")
                pass


#The following is program metadata
__author__ = "Devin Headrick"
__copyright__ = """Copyright (C) 2023, University of Alberta.
    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details."""