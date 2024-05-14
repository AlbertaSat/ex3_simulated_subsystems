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
import iris_subsystem

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1821
MAX_COMMANDSIZE = 128

LOGGER_FORMAT = "%(asctime)s: %(message)s"

Iris = iris_subsystem.IRISSubsystem()

def input_listen(port, message_buffer, reply_buffer):
    """ Creates a socket and begins a server that continuously listens for connection
        Once connection is received it listens for input and stores it into a FIFO queue
        Once input is terminated it resumes listening for a connection

        This is meant for a seperate thread and to be used in tandem with
        command handling threads.

        Args:
        port (const uint): The port the socket should be opened on
        message_buffer (SimpleQueue): The FIFO queue the input is stored in

    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        exit_flag = False
        server.bind((DEFAULT_HOST, port))
        server.listen()
        # Search for connections until told to exit
        while exit_flag is not True:
            conn, addr = server.accept() # Blocks execution until connection found
            with conn: # Connection is established
                logging.info("Connected by %s", addr)
                responder = threading.Thread(target=output_send, args=(conn, reply_buffer,))
                responder.start()
                while True:
                    # Put input into FIFO queue, verify to client command is received
                    # NOTE: This assumes all commands are less than MAX_COMMANDSIZE long
                    data = conn.recv(MAX_COMMANDSIZE)
                    if not data:
                        break
                    # conn.sendall(data) # For testing
                    message_buffer.put(data) # Stores data into queue as byte encoded
                    if data.decode() == "EXIT":
                        exit_flag = True
                # Connection is lost, close the responder
                responder.join()

    logging.info("Closing socket")

def output_send(conn, reply_buffer):
    """ Receives an established socket and continuously checks for responses to be sent
        Once a response is found, it transmits the response to the client through the socket
        Terminates upon receiving "EXIT" response

        This is meant for a seperate thread and to be used in tandem with
        both command handling threads and input listening threads.

        Args:
        conn (socekt): The socket currently opened.
        reply_buffer (SimpleQueue): The FIFO queue the responses are stored in

    """
    while True:
        reply = reply_buffer.get()
        if not reply:
            continue
        if reply == "EXIT":
            break
        try:
            if isinstance(reply, list):
                for element in reply:
                    # logging.info(element)
                    #TO-DO implement packet length tracker that is sent before a packet
                    header = "FLAG:" + str(len(element)) + ':'
                    if not isinstance(element, bytes):
                        element = element.encode()
                    conn.sendall(header.encode())
                    conn.sendall(element)
                continue
            else:
                header = "FLAG:" + str(len(reply)) + ':'
                conn.sendall(header.encode())
                conn.sendall(reply.encode())
        except BrokenPipeError:
            logging.info("Connection to client lost: Force closing output loop")
            return
        except socket.error as exc: # pylint: disable=bare-except
            # May implement counter for too many failures, (connection not lost but data cant send)
            logging.info("Output socket error %s: connection not lost, continuing responder", exc)
    logging.info("Closing output loop")



def command_handler(message_buffer, response_buffer):
    """ Checks for when FIFO message queue has information and fetches it and
        conducts the required operations based on the content.

        This is meant for a seperate thread and to be used in tandem with a server that
        fills the queue with command messages sent from a client

        Args:
        message_buffer (SimpleQueue): The FIFO queue the messages are fetched from

    """
    # Wait for input in the queue until told to exit
    while True:
        message = (message_buffer.get()).decode() # Messages are originally in bytes encoding
        if not message:
            continue
        if message == "EXIT":
            response_buffer.put("EXIT")
            break
        # NOTE: We do not currently know the format of IRIS commands, as such
        # I have taken the liberty to set commands to be simple abbreviations
        # each term passed should be delimited with ':' and each message
        # should begin with either EXECUTE/REQUEST depending on whether it expects a return
        logging.info("Received %s", message)
        args = message.split(':')
        try:
            command = iris_subsystem.Command(args)
        except IndexError:
            logging.info("ERROR %s Requires ':' delimiter between commands", message)
            response_buffer.put("ERROR Requires ':'")
            continue
        except ValueError:
            logging.info("ERROR %s must begin with REQUEST/EXECUTE/UPDATE", message)
            response_buffer.put("ERROR does not begin with REQUEST/EXECUTE/UPDATE")
            continue

        state = Iris.execute_command(command)

        # Only when the command is requesting a response should response be given
        logging.info(state)
        if command.call == "REQUEST":
            response_buffer.put(state)

    logging.info("Ending command processing")

if __name__ == "__main__":
    # If there is no arg, port is default otherwise use the arg
    PORT = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT
    logging.basicConfig(format=LOGGER_FORMAT, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Starting IRIS subsystem on port %s", PORT)
    # Initiate server threads
    messages = queue.SimpleQueue()
    responses = queue.SimpleQueue()

    # NOTE: listener will create at max 1 sub_thread at a time for responding to the current client
    listener = threading.Thread(target=input_listen, args=(PORT, messages, responses,))
    handler = threading.Thread(target=command_handler, args=(messages, responses,))

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