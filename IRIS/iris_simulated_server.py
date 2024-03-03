"""
This python program sets up a TCP server and simulates the IRIS payload component for ExAlta3.

Until we know more system specs we assume there are three types of commands that can be sent:
    - Request - Request a paramater from the state dictionary
    - Update  - Update a parameter in the state dictionary
    - Execute - Execute a command (e.g. reset watchdog timer)

# Example to toggle the sensors on:
     update:SensorStatus:1

# Example to request the temperature of the visible-light sensor:
    request:TempVIS

# Example to use the camera:
    execute:TakeImage

Usage:
- From one terminal:
    - python IRIS/iris_subsystem.py optional_port_num
- From another terminal:
    - nc host_ip port
    - type commands like 'request:TempVIS' (without the quotes)

Copyright 2024 [Ben Fisher, Abhishek Naik]. Licensed under the Apache License, Version 2.0
"""
import socket
import sys
import threading
import logging
import queue
from iris_subsystem import IRISSubsystem

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1821
MAX_COMMANDSIZE = 1024

LOGGER_FORMAT = "%(asctime)s: %(message)s"

Iris = IRISSubsystem()

def input_listen(port, message_buffer):
    """ Creates a socket and begins a server that continuously listens for connection
        Once connection is received it listens for input and stores it into a FIFO queue
        Once input is terminated it resumes listening for a connection

        This is meant for a seperate thread and to be used in tandem with 
        command handling threads.

        Args:
        port (const uint): The port the socket should be opened on
        message_buffer (SimpleQueue): The FIFO queue the input should be stored in

    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        exit_flag = False
        s.bind((DEFAULT_HOST, port))
        s.listen()
        # Search for connections until told to exit
        while exit_flag is not True:
            conn, addr = s.accept() # Blocks execution until connection found
            with conn:
                logging.info("Connected by %s", addr)
                while True:
                    # Put input into FIFO queue, verify to client command is received
                    # NOTE: This assumes all commands are less than MAX_COMMANDSIZE long
                    data = conn.recv(MAX_COMMANDSIZE)
                    if not data:
                        break
                    conn.sendall(data)
                    message_buffer.put(data) # Stores data into queue as byte encoded
                    if data.decode() == "EXIT":
                        exit_flag = True

    logging.info("Closing socket")
    return


def command_handler(message_buffer, response_buffer):
    """ Checks for when FIFO message queue has information and fetches it and 
        conducts the required operations based on the content.

        This is meant for a seperate thread and to be used in tandem with a server that
        fills the queue with command messages sent from a client

        Args:
        message_buffer (SimpleQueue): The FIFO queue the messages are fetched from

    """
    message = ""
    # Wait for input in the queue until told to exit
    while message != "EXIT":
        message = (message_buffer.get()).decode() # Messages are originally in bytes encoding
        if not message:
            continue
        # TO-DO implement command handling for different commands
        # NOTE: We do not currently know the format of IRIS commands, as such
        # I have taken the liberty to set commands to be 3 letter abbreviations
        # parameters passed to commands should be delimited with ':' and each message
        # should begin with either EXECUTE/REQUEST depending on whether it expects a return
        logging.info("Received %s", message)
        parsed_message = message.split(':')
        command_length = len(parsed_message)
        if command_length < 2:
            logging.info("Requires ':' delimiter between commands")
            continue

        if parsed_message[1] in Iris.get_commands():
            command = Iris.executable_commands[parsed_message[1]][0]
            n_parameters = Iris.executable_commands[parsed_message[1]][1]
            if command_length - 2 != n_parameters:
                logging.info("INVALID COMMAND %s requires %s parameters", parsed_message[1], n_parameters)
                continue
            # Until I figure out how to pass an ever changing number of parameters this will have to do
            match(command_length):
                case 2:
                    state = command()
                case 3:
                    state = command(parsed_message[2])
                case 4:
                    state = command(parsed_message[2], parsed_message[3])
                case _:
                    state = "Did not program more than 2 additional arguements currently"
            if parsed_message[0] == "REQUEST":
                logging.info(state)
                # response_buffer.put(state)
        else:
            logging.info("Invalid Command %s", parsed_message[1])
    logging.info("Ending command processing")
    return


if __name__ == "__main__":
    # If there is no arg, port is default otherwise use the arg
    PORT = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT
    logging.basicConfig(format=LOGGER_FORMAT, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Starting IRIS subsystem on port %s", PORT)
    # Initiate server threads
    messages = queue.SimpleQueue()
    responses = queue.SimpleQueue()
    listener = threading.Thread(target=input_listen, args=(PORT, messages,))
    handler = threading.Thread(target=command_handler, args=(messages,responses,))

    listener.start()
    handler.start()

    # Wait for server to exit
    listener.join()
    handler.join()
    logging.info("Simulated IRIS Server exited")
    # input_listen(PORT, messages)


# pylint: disable=duplicate-code
# no error
__author__ = "Ben Fisher"
__copyright__ = """
    Copyright 2024 [Ben Fisher]
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."""