
"""This module contains functions for creating a socket and listening for client connections"""

import socket


def create_socket_and_listen(host, port, command_handler):
    """Create a socket and bind it to the port. Listen indefinitely for client connections

    Args:
        host (str): The host address to bind the socket to
        port (int): The port to bind the socket to
        command_handler (CommandHandler): The command handler to use to process commands

    Returns:
        socket: The socket object created
    """

   # Create a socket and bind it to the port. Listen indefinitely for client connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_obj:
        # Tell OS to reuse socket addr if not previously closed
        socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_obj.bind((host, int(port)))
        socket_obj.listen()
        while True:
            try:
                conn, addr = socket_obj.accept()
                with conn:
                    print(f"Connected with {addr}", flush=True)
                    command_handler_obj = command_handler(conn)
                    command_handler_obj.handle_command()

            except KeyboardInterrupt:
                print("Keyboard interrupt detected. Closing socket.", flush=True)
                socket_obj.close()
                break

            except BrokenPipeError as error_msg:
                print(f"Client connection closed: {error_msg}", flush=True)
                socket_obj.close()


# The following is program metadata
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
