""" This program acts like a client to interact with the uhf tranceiver for testing purposes

The port number for server is passed as a commmand line argument.
hostname is assumed to be local host.
will listen and print any incoming messages to socket.
can send messages back to server by simply writing a command in the terminal

Copyright 2024 [Drake Boulianne]. Licensed under the Apache License, Version 2.0
"""


import socket
import sys
import threading

def write_to_server(client, lock):
    """
    uses client and lock to communicate with server. messages are sent by reading 
    standard input and the client sending all
    """
    while True:
        message = bytes(input(), "utf-8")
        try:
            with lock:
                client.sendall(message)
                print(f"Sent {message}")

        except BrokenPipeError as e:
            print(f"Error sending data: {e}")
            client.close()
            break

        except KeyboardInterrupt as e:
            print(f"Error sending data: {e}")
            client.close()
            break

BUFF_SIZE = 128

def main():

    """ main function that sets up generic client. The servers hostname will always be 
    the hosts name (as is in the simulated_uhf.py file) the desired port is given as a command
    line arg. Client created will listen to messages indefinitely and be able to send messages to 
    the server side client by way of the write thread.
        
    Args:
        None

    Returns:
        int: -1 for incorrect amount of cmd args, or not being able to connect to host
            returns 0 for successful exit
 """
    if len(sys.argv) != 2:
        print("Incorrect number of arguments:")
        print("Usage: python3 generic_client.py <port>")
        return -1

    host = '127.0.0.1'
    port = int(sys.argv[1])

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        print(f"Connected to {host}:{port}")

    except OSError as e:
        print(f"Could not connect to hostname: {host} port: {port} - {e}")
        return -1

    client_lock = threading.Lock()
    write_thread = threading.Thread(target=write_to_server, args=(client, client_lock))
    write_thread.start()

    while True:
        try:
            msg = client.recv(BUFF_SIZE)
            if len(msg) > 0:
                print(f"Received: {msg.decode('utf-8')}")

        except BlockingIOError:
            continue

        except KeyboardInterrupt as e:
            print(f"Error receiving data: {e}")
            break
    write_thread.join()
    client.close()
    return 0

if __name__ == "__main__":
    main()


# pylint: disable=duplicate-code
# no error
__author__ = "Drake Boulianne"
__copyright__ = """
    Copyright (C) 2024, [Drake Boulianne]
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."""
