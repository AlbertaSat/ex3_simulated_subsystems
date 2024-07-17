""" This program acts like a client to interact with the uhf tranceiver for testing purposes

The port number for server is passed as a commmand line argument.
hostname is assumed to be local host.
will listen and print any incoming messages to socket.
can send messages back to server by simply writing a command in the terminal

Copyright 2023 [Drake Boulianne]. Licensed under the Apache License, Version 2.0
"""


import socket
import sys
import threading

def write_to_server(client, lock):
    while True:
        message = bytes(input(), "utf-8")
        try:
            with lock:
                client.sendall(message)
                print(f"Sent {message}")
        except Exception as e:
            print(f"Error sending data: {e}")
            client.close()
            break

BUFF_SIZE = 128

def main():
    if len(sys.argv) != 2:
        print("Incorrect number of arguments:")
        print("Usage: python3 generic_client.py <port>")
        return 1

    host = socket.gethostname()
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
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

if __name__ == "__main__":
    main()


# pylint: disable=duplicate-code
# no error
__author__ = "Drake Boulianne"
__copyright__ = """
    Copyright (C) 2023, [Drake Boulianne]
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."""