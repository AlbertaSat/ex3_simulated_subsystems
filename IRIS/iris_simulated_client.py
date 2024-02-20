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

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1821

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((DEFAULT_HOST, DEFAULT_PORT))
    user_input = input()
    while user_input != "EXIT":
        s.sendall(user_input.encode())
        data = s.recv(1024)
        print(f"Received {data!r}")
        user_input = input()


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