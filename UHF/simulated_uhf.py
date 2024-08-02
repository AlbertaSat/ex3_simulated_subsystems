""" This program simulates the UHF tranceiver

information is sent over servers using TCP sockets and shared data buffers between the two servers.
information sent to one server will be echoed to the other. 

Copyright 2024 [Drake Boulianne]. Licensed under the Apache License, Version 2.0
"""

import socket
import threading
import time
import select

DEBUG = 1
BUFF_SIZE = 128
COMMS_SIDE_SERVER_PORT = 1234
GS_SIDE_SERVER_PORT = 1235
COMM_SERVER_HOSTNAME = '127.0.0.1'
GS_SERVER_HOSTNAME = '127.0.0.1'

# Use lists for shared buffers to allow modification within threads
gs_data = []
comm_data = []

# Using mutable type as a makeshift pointer so clients can be modified across threads
client_pointer = {}

# client keys
GS_CLIENT_KEY = "gs_client"
COMM_CLIENT_KEY = "comm_client"

# Disable global statements and invalid names for beacon_string variable
# pylint: disable=global-statement
BEACON_STRING = "beacon"

# Delimiter for command
DELIMITER = ':'


def check_port(port):
    """
    Function to check if port is free for use
    
    Args:
        port(int): port number that is checked
    
    Returns:
        Boolean: returns true if port is free, false if port is in use
    """

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("0.0.0.0", port))
            return True

        except OSError:
            return False


def mod_beacon(message, lock):
    """
    parses the command and modifies the beacon string (BEACON)
    Args:
        msg(string): message sent from comms handler
    Returns:
        None
    """
    # Use of global, valid because no other part of code modifies the beacon_string variable
    global BEACON_STRING

    try:
        command = message.decode("utf-8").strip().split(DELIMITER)
        with lock:
            BEACON_STRING = command[1]

    except TypeError as e:
        print(f"Failed to parse: {e}")

    except IndexError as e:
        print(f"Improper us of Delimiter, Failed to parse: {e}")


def beacon(client_key, server, lock, n=5):
    """
    continually sends beacon every n seconds

    Args:
        client_key(string): key to access the dictionary where client socket object 
        is stored (client_pointer)
        lock(mutex): the lock used when interacting with client socket
        n(integer): the amount of time in seconds between beacon messages
            defult value of 5.
    Returns:
        None
    """

    while True:
        time.sleep(n)
        with lock:
            try:
                client_pointer[client_key].sendall(bytes(BEACON_STRING, "utf-8"))
                if DEBUG:
                    print("Sent beacon")

            except BrokenPipeError as e:
                print(f"Error sending beacon: {e}")
                print("waiting for client to connect")
                client_pointer[client_key].close()
                client_pointer[client_key] = search_client(server, lock)

            except KeyboardInterrupt as e:
                print(f"Error sending beacon: {e}")
                break




def start_server(hostname, port):
    """
    Creates a server socket object with given port and name. client que is 5.

    Args:
        hostname(string): hostname for server
        port(int): port bound to server
    
    Returns:
        server(socket): server socket object
    """

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((hostname, port))
    server.listen(5)
    return server


def search_client(server, lock):
    """
    Waits for client to connect to the servver

    Args:
        server(socket): server socket object that waits for connection
    
    Returns:
        client(socket): client socket object
        
    """
    print("This ran")
    with lock:
        try:
            client, addr = server.accept()
            print("Connected to", addr)
            return client

        except (BrokenPipeError, OSError) as e:
            print(f"Error occurred: {e}")
            return None



def send_msg(client_key, buffer, lock):
    """
    sends message from buffer via client socket 

    Args:
        client_key(string): key to access the dictionary where client socket object 
        is stored (client_pointer)
        buffer(list): shared buffer containing message to be sent
        lock(mutex): lock to prevent a race condition on shared data

    Returns:
        None
    """

    while True:
        try:
            with lock:
                if buffer:
                    if DEBUG:
                        print("update:")
                        print("***** BEFORE *****")
                        print(buffer)
                        print("******************")

                    message = buffer.pop(0)
                    client_pointer[client_key].sendall(message)

                    if DEBUG:
                        print("***** AFTER *****")
                        print(f"Sent {message}")
                        print(buffer)
                        print("******************")


        except KeyboardInterrupt as e:
            print(f"Error sending message: {e}")
            break

        except BrokenPipeError as e:
            print(f"Pipe Broke: {e}")


def receive_msg(client_key, server, buffer, lock):
    """
    listens for messages on the client and stores them in the buffer

    Args: 
        client_key(string): key to access the dictionary where client socket object 
        is stored (client_pointer)
        buffer(list): shared buffer used to store received messsages
        lock(mutex): lock to prevent a race condition on shared data

    Returns:
        None
    """

    while True:
        try:
            # Use select to check if data is available to be read
            ready_to_read, _, _ = select.select([client_pointer[client_key]], [], [], 0.5)

            if ready_to_read:
                message = client_pointer[client_key].recv(BUFF_SIZE)

                if message:
                    if DEBUG:
                        print(f"Received: {message.decode('utf-8')}")

                    _, port = client_pointer[client_key].getsockname()

                    # Primitive check to see if messages intent was to modify UHF params
                    if port == COMMS_SIDE_SERVER_PORT and b"MOD_UHF" in message:
                        mod_beacon(message, lock)

                    else:
                        with lock:
                            buffer.append(message)
                else:
                    client_pointer[client_key].close()
                    client_pointer[client_key] = search_client(server, lock)

        except BlockingIOError:
            pass

        except KeyboardInterrupt as e:
            print(f"Error receiving message: {e}")
            client_pointer[client_key].close()
            break

        except BrokenPipeError as e:
            print(f"Pipe Broke: {e}")
            print("waiting for client to connect")
            client_pointer[client_key].close()
            client_pointer[client_key] = search_client(server, lock)



def main():
    """
    main function for simulating uhf transceiver.
    Args:
        None
    Returns:
        None
    """

    comm_server = start_server(COMM_SERVER_HOSTNAME, COMMS_SIDE_SERVER_PORT)
    gs_server = start_server(GS_SERVER_HOSTNAME, GS_SIDE_SERVER_PORT)

    client_lock = threading.Lock()


    comm_client = search_client(comm_server, client_lock)
    client_pointer[COMM_CLIENT_KEY] = comm_client
    gs_client = search_client(gs_server, client_lock)
    client_pointer[GS_CLIENT_KEY] = gs_client

    if comm_client is None or gs_client is None:
        print("Failed to connect to client")
        return -1

    comm_listen = threading.Thread(target=receive_msg,
                                args=(COMM_CLIENT_KEY, comm_server, gs_data, client_lock))
    gs_listen = threading.Thread(target=receive_msg,
                                args=(GS_CLIENT_KEY, gs_server, comm_data, client_lock))

    comm_send = threading.Thread(target=send_msg,
                                args=(COMM_CLIENT_KEY, comm_data, client_lock))
    gs_send = threading.Thread(target=send_msg,
                                args=(GS_CLIENT_KEY, gs_data, client_lock))

    comm_listen.start()
    gs_listen.start()

    comm_send.start()
    gs_send.start()

    beacon(GS_CLIENT_KEY, gs_server, client_lock)

    comm_listen.join()
    comm_send.join()
    gs_listen.join()
    gs_send.join()

    comm_server.close()
    gs_server.close()


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
