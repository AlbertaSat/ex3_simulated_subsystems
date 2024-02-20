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

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1821
MAX_COMMANDSIZE = 1024
DEFAULT_STATE_VALUES = {                # at some point, we should simulate temperature changes
            'PowerStatus': 1,           # 1 means powered on, 0 means off
            'SensorStatus': 0,          # 1 means sensors are on, 0 means off
            'NumImages': 0,             # number of images
            'MaxNumImages': 20,         # maximum images that can be stored
            'DateTime': '1707677962'    # arbitrary value for now (time at which this was written)
        }

LOGGER_FORMAT = "%(asctime)s: %(message)s"

class IRISSubsystem: # pylint: disable=too-many-instance-attributes
    """Holds the state of the IRIS subsystem.

    Tuples are provided that define the executable commands and updatable parameters.
    """
    def __init__(self):
        self.state = {
            'PowerStatus': DEFAULT_STATE_VALUES['PowerStatus'],
            'SensorStatus': DEFAULT_STATE_VALUES['SensorStatus'],
            'NumImages': DEFAULT_STATE_VALUES['NumImages'],
            'MaxNumImages': DEFAULT_STATE_VALUES['MaxNumImages'],
            'Time': DEFAULT_STATE_VALUES['DateTime'],
            'TempVIS': 25,              # in degree Celsius
            'TempNIR': 25,              # in degree Celsius
            'TempGATE': 25,             # in degree Celsius
            'TempFLASH': 25,            # in degree Celsius
            'SoftwareVersion': 1.0,
        }
        self.updatable_parameters = ['PowerStatus', 'SensorStatus', 'Time']
        self.executable_commands = {
            'TakeImage': self.take_image,
            'Reset': self.reset
        }

    def take_image(self):
        """Simulates taking a picture using the IRIS camera."""
        self.state['NumImages'] += 1
        print('Increased NumImages by 1')

    def reset(self):
        """Simulates a 'factory reset' of the IRIS subsystem."""
        for key, value in DEFAULT_STATE_VALUES.items():
            self.state[key] = value         # temp is what the temp is, doesn't get reset
        print('Factory reset performed.')

    def get_image(self, n_images):
        """Simulates fecthing n_images stored on the IRIS subsystem """
        print('Fetching', n_images, 'Images...')
        #TO-DO
        print(n_images, 'images fetched')

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
                    if data.decode() == "EXIT":
                        exit_flag = True
                    conn.sendall(data)
                    message_buffer.put(data) # Stores data into queue as byte encoded

    logging.info("Closing socket")
    return

def command_handler(message_buffer):
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
        logging.info("Received %s", message)
    logging.info("Ending command processing")
    return


if __name__ == "__main__":
    # If there is no arg, port is default otherwise use the arg
    PORT = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT
    logging.basicConfig(format=LOGGER_FORMAT, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Starting IRIS subsystem on port %s", PORT)
    # Initiate server threads
    messages = queue.SimpleQueue()
    listener = threading.Thread(target=input_listen, args=(PORT, messages,))
    handler = threading.Thread(target=command_handler, args=(messages,))

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