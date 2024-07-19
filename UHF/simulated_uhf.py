""" This program simulates the UHF tranceiver

information is sent over servers using TCP sockets and shared data buffers between the two servers.
information sent to one server will be echoed to the other. 

Copyright 2024 [Drake Boulianne]. Licensed under the Apache License, Version 2.0
"""

import socket
import threading
import time
import select

DEBUG = 0
BUFF_SIZE = 128
COMMS_SIDE_SERVER_PORT = 1234
GS_SIDE_SERVER_PORT = 1235
COMM_SERVER_HOSTNAME = socket.gethostname()
GS_SERVER_HOSTNAME = socket.gethostname()

# Use lists for shared buffers to allow modification within threads
gs_data = []
comm_data = []


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


def beacon(client, lock):
    """
    continually sends beacon every n seconds

    Args:
        client(socket): the client socket communicating to the ground station
        lock(mutex): the lock used when interacting with client socket

    Returns:
        None
    """

    while True:
        # Send beacon every 5 seconds for testing
        time.sleep(5)
        with lock:
            try:
                client.sendall(b"beacon")
                if DEBUG:
                    print("Sent beacon")

            except BrokenPipeError as e:
                print(f"Error sending beacon: {e}")
                break

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
    server.bind((hostname, port))
    server.listen(5)
    return server


def search_client(server):
    """
    Waits for client to connect to the servver

    Args:
        server(socket): server socket object that waits for connection
    
    Returns:
        client(socket): client socket object
        
    """

    try:
        client, addr = server.accept()
        print("Connected to", addr)
        return client

    except BrokenPipeError as e:
        server.close()
        print(f"Error occurred: {e}")

    except KeyboardInterrupt as e:
        server.close()
        print(f"Error occured {e}")

    except OSError as e:
        server.close()
        print(f"Error occurred: {e}")

    return None




def send_msg(client, buffer, lock):
    """
    sends message from buffer via client socket 

    Args:
        client(socket): client socket object that sends the message
        buffer(list): shared buffer containing message to be sent
        lock(mutex): lock to prevent a race condition on shared data
    
    Returns:
        None
    """

    while True:
        with lock:
            if buffer:
                if DEBUG:
                    print("update:")
                    print(gs_data)
                    print(comm_data)

                try:
                    message = buffer.pop(0)
                    client.sendall(message)
                    if DEBUG:
                        print(f"Sent {message}")
                        print(gs_data)
                        print(comm_data)

                except BrokenPipeError as e:
                    print(f"Error sending message: {e}")
                    client.close()
                    break

                except KeyboardInterrupt as e:
                    print(f"Error sending message: {e}")
                    client.close()
                    break



def receive_msg(client, buffer, lock):
    """
    listens for messages on the client and stores them in the buffer

    Args: 
        client(socket): client socket object that receives the message
        buffer(list): shared buffer used to store received messsages
        lock(mutex): lock to prevent a race condition on shared data

    Returns:
        None
    """

    while True:
        try:
            # Use select to check if data is available to be read
            ready_to_read, _, _ = select.select([client], [], [], 0.5)  # timeout set to 0.5 seconds
            if ready_to_read:
                message = client.recv(BUFF_SIZE)
                if message:
                    if DEBUG:
                        print(f"Received: {message.decode('utf-8')}")
                    with lock:
                        buffer.append(message)
                else:
                    print("Connection closed by the client")
                    break
        except BlockingIOError:
            pass

        except KeyboardInterrupt as e:
            print(f"Error receiving message: {e}")
            client.close()
            break

        except BrokenPipeError as e:
            print(f"Error receiving message: {e}")
            client.close()
            break


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

    comm_client = search_client(comm_server)
    gs_client = search_client(gs_server)

    client_lock = threading.Lock()

    comm_listen = threading.Thread(target=receive_msg, args=(comm_client, gs_data, client_lock))
    gs_listen = threading.Thread(target=receive_msg, args=(gs_client, comm_data, client_lock))

    comm_send = threading.Thread(target=send_msg, args=(comm_client, comm_data, client_lock))
    gs_send = threading.Thread(target=send_msg, args=(gs_client, gs_data, client_lock))

    comm_listen.start()
    gs_listen.start()

    comm_send.start()
    gs_send.start()

    beacon(gs_client, client_lock)



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
