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


class IRISSubsystem: # pylint: disable=too-few-public-methods disable=too-many-instance-attributes
    """Holds the state of the IRIS subsystem.

    Tuples are provided that define the executable commands and updatable parameters.

    """
    def __init__(self):
        self.power_status = 1           # 1 means powered on, 0 means off
        self.sensor_status = 0          # 1 means sensors are on, 0 means off
        self.temp_vis = 25              # in degree Celsius
        self.temp_nir = 25              # in degree Celsius
        self.temp_flash = 25            # in degree Celsius
        self.temp_gate = 25             # in degree Celsius
        self.num_images = 5             # number of images
        self.max_num_images = 20        # maximum images that can be stored
        self.software_version = 1.0
        self.state = {
            'PowerStatus': self.power_status,
            'SensorStatus': self.sensor_status,
            'TempVIS': self.temp_vis,
            'TempNIR': self.temp_nir,
            'TempFLASH': self.temp_flash,
            'TempGATE': self.temp_gate,
            'NumImages': self.num_images,
            'SoftwareVersion': self.software_version,
        }
        self.updatable_parameters = ['PowerStatus', 'SensorStatus']
        self.executable_commands = {
            'TakeImage': self.take_image,
            'SetTime': self.set_time
        }

    def take_image(self):
        self.state['NumImages'] += 1
        print('Increased NumImages by 1')

    def set_time(self):
        print('Not implemented yet')
        return


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
