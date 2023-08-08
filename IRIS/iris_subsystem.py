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
from socket_stuff import create_socket_and_listen
from command_handler import CommandHandler
from command_factory import CommandFactory


DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1801


class IRISSubsystem:
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
            # ToDo: add time
        }
        self.updatable_parameters = ['PowerStatus', 'SensorStatus']
        self.executable_commands = ['TakeImage', 'SetTime']


class IRISCommandFactory(CommandFactory):
    """Custom command factory for IRIS-specific commands."""

    def command_execute(self, params=None):
        print("Execute command received: " + params[0])
        if params and len(params) == 1 and params[0] in self.subsystem.executable_commands:
            if params[0] == 'TakeImage':
                self.subsystem.state['NumImages'] += 1
                print('Increased NumImages by 1')
                # ToDo: do more stuff here
            return f"Command {params[0]} executed \n"
        return "ERROR: Invalid execute command \n"


if __name__ == "__main__":
    # If there is no arg, port is default otherwise use the arg
    PORT = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT
    print(f"Starting IRIS subsystem on port {PORT}")

    command_factory = IRISCommandFactory(IRISSubsystem())
    handler = CommandHandler(command_factory)

    create_socket_and_listen(host=DEFAULT_HOST, port=PORT,
                             command_handler_obj=handler)
