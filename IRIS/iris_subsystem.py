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

IRIS_COMMAND_SIZE = 1024

DEFAULT_STATE_VALUES = {                # at some point, we should simulate temperature changes
            'PowerStatus': 1,           # 1 means powered on, 0 means off
            'SensorStatus': 0,          # 1 means sensors are on, 0 means off
            'NumImages': 0,             # number of images
            'MaxNumImages': 20,         # maximum images that can be stored
            'DateTime': '1707677962'    # arbitrary value for now (time at which this was written)
        }
""" These are previous C commands used for Ex_Alta_2 for reference
# void get_housekeeping(housekeeping_packet_t *hk);
# void take_image();
# void get_image_count(uint8_t *cnt);
# int get_image_length(uint32_t *image_length, uint8_t index);
# void turn_off_sensors();
# void turn_on_sensors();
# void set_configurations(Iris_config *config);
# int initalize_sensors();
# int onboot_sensors(uint8_t sensor);
# void set_rtc_time(uint32_t obc_unix_time);
# void get_rtc_time(Iris_Timestamp *timestamp);
# int transfer_image_to_nand(uint8_t sensor, uint8_t *file_timestamp);
# int delete_image_file_from_queue(uint16_t index);
# NAND_FILE *get_image_file_from_queue(uint8_t index);
# void set_capture_timestamp(uint8_t *file_timestamp, uint8_t sensor);
# int store_file_infos_in_buffer();
# void flood_cam_spi();
"""
class Command:
    """ Holds a command with its type, abbreviation, and parameters
    """
    def __init__(self, message):
        """Initializes a basic command structure, 
           requires all parameters to be passed as a list

           Args:
           message (list of strings): contains all information for the command
        """
        length = len(message)
        if length < 2:
            raise IndexError
        if message[0] not in ["EXECUTION", "REQUEST", "UPDATE"]:
            raise ValueError

        self.call = message[0]
        self.abbrev = message[1]
        self.parameters = list()
        for index in range(2, length):
            self.parameters.append(message[index])
        self.n_params = length - 2

    def __repr__(self):
        return f"Command({self.__dict__!r})"


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
            'Time': DEFAULT_STATE_VALUES['DateTime'],
            'TempVIS': 25,              # in degree Celsius
            'TempNIR': 25,              # in degree Celsius
            'TempGATE': 25,             # in degree Celsius
            'TempFLASH': 25,            # in degree Celsius
            'SoftwareVersion': 1.0,
        }
        self.updatable_parameters = ['PowerStatus', 'SensorStatus', 'Time']
        self.executable_commands = {
            # Executable commands in tuple form of command() and n_parameters to command
            'TKI': (self.take_image, 0),
            'RST': (self.reset, 0),
            'FTI': (self.get_image, 1),
            'FTH': (self.get_housekeeping, 0),
            'STT': (self.set_time, 1),
            'HELP': (self.command_help,0)
        }

    def get_commands(self):
        """Returns all possible command keys of the simulated IRIS subsystem"""
        return list(self.executable_commands.keys())

    def command_help(self):
        """Returns all possible commands and their # of parameters 
            on the simulated IRIS subsystem, newlines are appended 
            for terminal clarity
        """
        commands = list()
        commands.append("Abbrev: #parameters\n")
        # Note that all commands have a tuple containing their method and # params
        for pair in self.executable_commands.items():
            commands.append(str(pair[0]) + ": " + str(pair[1][1]) + "\n")
        return commands

    def execute_command(self, command):
        """Runs the provided command in the IRIS simualted subsystem if it exists

            command (Command): class containing all information for command
        """
        # Simple error checking
        if not isinstance(command, Command):
            return "ERROR: command must be given using Command class"
        if command.abbrev not in self.get_commands():
            return "ERROR: command " + command.abbrev + " invalid, type 'REQUEST:HELP'"
        execution = self.executable_commands[command.abbrev]
        if command.n_params != execution[1]:
            return "ERROR: command " + command.abbrev + " expects " + str(execution[1]) + " arg(s)"

        if command.n_params == 0:
            return execution[0]()
        else:
            return execution[0](command.parameters)

    # ---- IRIS Simulated Commands, all must be within self.executable_commands ----
    # NOTE: Every executable command expecting parameters takes in a list
    #       and parses it for parameters
    def take_image(self):
        """Simulates taking a picture using the IRIS camera."""
        self.state['NumImages'] += 1
        return 'Increased NumImages by 1'

    def reset(self):
        """Simulates a 'factory reset' of the IRIS subsystem."""
        for key, value in DEFAULT_STATE_VALUES.items():
            self.state[key] = value         # temp is what the temp is, doesn't get reset
        return 'Factory reset performed.'

    def get_image(self, params):
        """Simulates fecthing n_images stored on the IRIS subsystem.
            Expects 1 parameter passed: n_images (int)
        """
        n_images = params[0]
        # print('Fetching', n_images, 'Images...')
        #TO-DO
        return n_images + ' images fetched'

    def get_housekeeping(self):
        """Simulates fecthing the housekeeping data on the IRIS subsystem.
            Note that due to socket handling tuples must be converted into string pairs
        """
        current_state = list()
        for pair in self.state.items():
            current_state.append(str(pair[0]) + ": " + str(pair[1]) + " ")
        return current_state

    def set_time(self, params):
        """Simulates setting the time of the IRIS subsystem
            Expects 1 parameter passed: time (unsigned long)
        """
        time = params[0]
        self.state['Time'] = time
        return 'Time updated to ' + self.state['Time']


# pylint: disable=duplicate-code
# no error
__author__ = "Ben Fisher, Abhishek Naik"
__copyright__ = """
    Copyright (C) 2024, [Ben Fisher, Abhishek Naik]
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."""
