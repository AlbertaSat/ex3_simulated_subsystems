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
            'STT': (self.set_time, 1)
        }
    def get_commands(self):
        """Returns all possible command keys of the IRIS subsystem"""
        return self.executable_commands.keys()

    # ---- IRIS Simulated Commands, all must be within self.executable_commands ----
    def take_image(self):
        """Simulates taking a picture using the IRIS camera."""
        self.state['NumImages'] += 1
        return 'Increased NumImages by 1'

    def reset(self):
        """Simulates a 'factory reset' of the IRIS subsystem."""
        for key, value in DEFAULT_STATE_VALUES.items():
            self.state[key] = value         # temp is what the temp is, doesn't get reset
        return 'Factory reset performed.'

    def get_image(self, n_images):
        """Simulates fecthing n_images stored on the IRIS subsystem."""
        # print('Fetching', n_images, 'Images...')
        #TO-DO
        return n_images + ' images fetched'

    def get_housekeeping(self):
        """Simulates fecthing the housekeeping data on the IRIS subsystem."""
        return self.state.items()

    def set_time(self, time):
        """Simulates setting the time of the IRIS subsystem"""
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
