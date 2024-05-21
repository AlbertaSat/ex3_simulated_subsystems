"""
This python program sets up a TCP client terminal and simulates
the commands sent to the IRIS payload component for ExAlta3.

Until we know more system specs we assume
there are three types of commands that can be sent:
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
- From this terminal:
    - python IRIS/command_terminal.py
    - type commands like 'request:TempVIS' (without the quotes)
- From another terminal:
    - python IRIS/iris_simulated_server.py (optional port number)

Copyright 2024 [Ben Fisher]. Licensed under the Apache License, Version 2.0
"""
import socket
import sys

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1821
MAX_RECEIVE = 1024
FLAG_HEADER = 'FLAG'
END_FLAG = "|END" # END_FLAG should have same length as FLAGSIZE
FLAGSIZE = 4
PACKET_DELIMITER = ':'

def main(port):
    """ Creates a socket and attempts to connect to a running server
        Once connection is received it listens for input and sends the input to the server

        Args:
        port (const uint): The port the socket should be opened on

    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((DEFAULT_HOST, port))
        while True:
            user_input = input()
            client.sendall(user_input.encode())
            if user_input == "EXIT":
                break
            if user_input.startswith("REQUEST"):
                print("Receiving response...\n")
                response_listen(client)
                print("\n\nContinue Commands")


def response_listen(conn):
    """ Listens and prints responses from the server through the connected socket
        This is meant to be a daemon thread,
        it is always running and closes once it is the only one left

        Args:
        conn (socket): The connected socket we are listening to

    """
    while True:
        done = check_flag(conn) # This blocks execution until FLAG_HEADER is received
        if done:
            return
        # Start flag received, nextRE element is length of packet
        packet_len = get_packet_length(conn)

        data = conn.recv(packet_len)
        # TO-DO implement packet length tracker that receives packet length before reading
        if data.startswith(b'IMAGES:'):

            n_images = int(data.split(b':')[1])
            if n_images == 0:
                print("No images found")
            elif fetch_images(conn, n_images) == n_images:
                print("Successfully saved "+ str(n_images) +" images")
        else:
            print(data.decode(), end="")

def fetch_images(conn, n_images):
    """ Listens on socket and attempts to read in n_images and write them to client directory
        If invalid image name is given, or something goes wrong :(, flushes buffer and print error


        Args:
        conn (socket): The connected socket we are listening to
        n_images (int): The number of images expected to read

        Returns:
        # : failure to read one of the images, # is the number of images successfully read
        n_images: successfully read all images
    """
    # Will repeat until it processes all images
    for image_count in range(n_images):
        # Wait for next packet
        check_flag(conn)
        packet_len = get_packet_length(conn)

        #Location packet should prepend the image packet
        image_name = conn.recv(packet_len).decode("utf-8")
        if not image_name.startswith('image'):
            # Error in reading images, flush receival data and print error
            conn.setblocking(False)
            while True:
                try:
                    conn.recv(4096)
                except BlockingIOError:
                    break
            conn.setblocking(True)
            print("ERROR: " + image_name + " is not a valid name")
            return image_count

        # Read in the next image
        with open('./Client_Photos/' + image_name, 'wb') as image:
            check_flag(conn)
            packet_len = get_packet_length(conn)

            data = conn.recv(packet_len)
            image.write(data)
            image.close()
    return n_images

def check_flag(conn):
    """ Listens on socket conn and reads one byte at a time
        will listen until it receives a series of bytes that mirrors the FLAG_HEADER
        Once received, returns 1

        Args:
        conn (socket): The connected socket we are listening to

    """
    flag_check = ['0'] * FLAGSIZE
    while True:

        # Scan 1 byte at a time for start flag
        data = conn.recv(1)
        flag_check.append(data.decode("utf-8"))
        flag_check.pop(0)

        counter = 0
        end = 0
        for index in range(FLAGSIZE):
            if flag_check[index] != FLAG_HEADER[index]:
                counter += 1
            if flag_check[index] == END_FLAG[index]:
                end += 1

        if counter == 0:
            return 0
        if end == FLAGSIZE:
            return 1 # END tag found, done receiving

def get_packet_length(conn):
    """ Listens on socket connection and reads in a the length of the next packet
        this is to be called after check_flag successfully finds a flag

        Args:
        conn (socket): The connected socket we are listening to

        Returns:
        legnth of next packet (int)
    """
    packet_len = 0
    data = conn.recv(1) # Fetch first delimiter
    data = conn.recv(1).decode() # Fetch start of second delimiter
    while data != PACKET_DELIMITER:
        if packet_len != 0: #There is another digit
            packet_len *= 10
        packet_len += int(data)
        data = conn.recv(1).decode()
    return packet_len

if __name__ == "__main__":
    PORT = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT
    main(PORT)

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