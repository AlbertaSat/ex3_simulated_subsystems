"""This python program simulates the IRIS payload component for ExAlta3.

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

Copyright 2023 [Abhishek Naik]. Licensed under the Apache License, Version 2.0
"""


import sys
sys.path.append("../ex3_simulated_subsystems")
from socket_stuff import create_socket_and_listen   # pylint: disable=C0413
from command_handler import CommandHandler          # pylint: disable=C0413
from command_factory import CommandFactory          # pylint: disable=C0413


DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1821
DEFAULT_STATE_VALUES = {                # at some point, we should simulate temperature changes
            'PowerStatus': 1,           # 1 means powered on, 0 means off
            'SensorStatus': 0,          # 1 means sensors are on, 0 means off
            'NumImages': 0,             # number of images
            'MaxNumImages': 20          # maximum images that can be stored
        }


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
            'TempVIS': 25,              # in degree Celsius
            'TempNIR': 25,              # in degree Celsius
            'TempGATE': 25,             # in degree Celsius
            'TempFLASH': 25,            # in degree Celsius
            'SoftwareVersion': 1.0
        }
        self.updatable_parameters = ['PowerStatus', 'SensorStatus']
        self.executable_commands = {
            'TakeImage': self.take_image,
            'SetTime': self.set_time,
            'Reset': self.reset
        }

    def take_image(self):
        """Simulates taking a picture using the IRIS camera."""
        self.state['NumImages'] += 1
        print('Increased NumImages by 1')

    def set_time(self):
        """Simulates setting the time for the IRIS subsystem."""
        print('Not implemented yet')

    def reset(self):
        """Simulates a 'factory reset' of the IRIS subsystem."""
        for key, value in DEFAULT_STATE_VALUES.items():
            self.state[key] = value         # temp is what the temp is, doesn't get reset
        print('Factory reset performed.')


if __name__ == "__main__":
    # If there is no arg, port is default otherwise use the arg
    PORT = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT
    print(f"Starting IRIS subsystem on port {PORT}")

    command_factory = CommandFactory(IRISSubsystem())
    handler = CommandHandler(command_factory)

    create_socket_and_listen(host=DEFAULT_HOST, port=PORT,
                             command_handler_obj=handler)


# pylint: disable=duplicate-code
# no error
__author__ = "Abhishek Naik"
__copyright__ = """
    Copyright (C) 2023, [Abhishek Naik]
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."""
