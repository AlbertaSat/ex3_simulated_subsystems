"""This python program represents a simulated version of the EPS payload for ExAlta3.

For now the sub system communicates with strings over a TCP socket. The strings are parsed
into a command type and associated data.

Until we know more system specs I am assuming there are three types of commands that can be sent:
    - Request - Request a paramater from the state dictionary
    - Update  - Update a parameter in the state dictionary
    - Execute - Execute a command (e.g. reset watchdog timer)

# Example to update the WatchdogResetTime:
     update:WatchdogResetTime:48.0

# Example to request the Voltage:
    request:Voltage

# Example to execute a ResetWatchdogTimer command:
    execute:ResetWatchdogTimer

For now you can test your commands using netcat (nc) from the command line, and piping the command
to the socket from a seperate text file.

Usage: ESP_component.py non-default_port_num

Copyright 2023 [Devin Headrick]. Licensed under the Apache License, Version 2.0
"""

import sys
sys.path.append("../")
from socket_stuff import create_socket_and_listen   # pylint: disable=C0413
from command_handler import CommandHandler          # pylint: disable=C0413
from command_factory import CommandFactory          # pylint: disable=C0413


DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1801
COMMAND_DELIMITER = ':'

default_eps_state = {
    'Temperature': 32,           # in degrees C
    'Voltage': 5.24,             # in volts
    'Current': 1.32,             # in amps
    'BatteryState': 'Charging',
    'WatchdogResetTime': 24.0,   # in hours
}

default_subsystem_state = {
    'ADCS': False,
    'Deployables': False,
    'DFGM': False,
    'GPS': False,
    'IRIS': False,
    'UHF': False,
    'AntennaBurnWireGPIO': False,
    'UHFBurnWireGPIO': False
}

class EPSSubsystem: #pylint:disable=too-few-public-methods disable=too-many-instance-attributes
    """Holds the state of the EPS subsystem.

    Tuples are defined that define the executable commands and updatable parameters.
    Functions are defined which are called upon receipt of associated execute commands.
    """

    def __init__(self):
        self.temperature = 32            # in degrees C
        self.voltage = 5.24              # in volts
        self.current = 1.32              # in amps
        self.battery_state = 'Charging'
        self.watchdog_reset_time = 24.0  # in hours
        self.state = {
            'Temperature': self.temperature,
            'Voltage': self.voltage,
            'Current': self.current,
            'BatteryState': self.battery_state,
            'WatchdogResetTime': self.watchdog_reset_time,
        }
        self.updatable_parameters = ['WatchdogResetTime']

        self.subsystems = {
            'ADCS': False,
            'Deployables': False,
            'DFGM': False,
            'GPS': False,
            'IRIS': False,
            'UHF': False,
            'AntennaBurnWireGPIO': False,
            'UHFBurnWireGPIO': False
        }

        self.eps_on = True

        # Changing executable command tuples to dictionaries to point to fxns
        self.executable_commands = {
            'ResetDevice': self.reset_device,
            'ResetSubsystems': self.reset_subsystems_state,
            'SubsystemOn': self.subsystem_on,
            'SubsystemOff': self.subsystem_off

        }

    def turn_on_eps(self):
        """Turn on the EPS subsystem"""
        self.eps_on = True
        print("EPS turned ON\n")
    def turn_off_eps(self):
        """Turn off the EPS subsystem"""
        self.eps_on = False
        print("EPS turned OFF\n")
    def reset_device(self):
        """Reset the device to default state, which is defined at the top of this file."""
        if self.eps_on is False:
            print("ERROR: EPS turned off. Please turn on EPS to execute command\n")
        self.set_state_dict(default_eps_state)
        print("EPS printed to default state\n")
    def reset_subsystems_state(self):
        """Reset the subsystems to default state, which is defined at the top of this file."""
        if self.eps_on is False:
            print("ERROR: EPS turned off. Please turn on EPS to execute command\n")
        self.subsystems = default_subsystem_state.copy()
        print("Subsystems printed to default state\n")

    def subsystem_on(self, subsystem_name):
        """
    Turn off the specified subsystem.

    Args:
        subsystem_name (str): The name of the subsystem to turn off.

    prints:
        str: A message indicating the result of the operation.
    """
        if self.eps_on is False:
            print("ERROR: EPS turned off. Please turn on EPS to execute command\n")
        if subsystem_name in self.subsystems:
            self.subsystems[subsystem_name] = True
            print(f"{subsystem_name} turned ON\n")
        print(f"ERROR: {subsystem_name} is not a valid subsystem\n")
    def subsystem_off(self, subsystem_name):
        """
    Turn off the specified subsystem.

    Args:
        subsystem_name (str): The name of the subsystem to turn off.

    prints:
        str: A message indicating the result of the operation.
    """
        if self.eps_on is False:
            print("ERROR: EPS turned off. Please turn on EPS to execute command\n")
        if subsystem_name in self.subsystems:
            self.subsystems[subsystem_name] = False
            print(f"{subsystem_name} turned OFF\n")
        print(f"ERROR: {subsystem_name} is not a valid subsystem\n")


    def set_state_dict(self, new_state_dict):
        """Set the state dictionary to the provided dictionary

        This can be used to inject states into this subsystem for testing purposes.
        """
        try:
            for key in self.state:
                if key in new_state_dict:
                    self.state[key] = new_state_dict[key]

        except Exception as exeption: # pylint: disable=broad-except
            print("Error setting state dictionary: " + str(exeption) +
                  " \n Reset State to default values.")


if __name__ == "__main__":
    # If there is no arg, port is default otherwise use the arg
    PORT = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT

    print(f"Starting EPS subsystem on port {PORT}")

    # Concrete factory instance relies on subsystem class that contains associated state and fxns
    command_factory = CommandFactory(EPSSubsystem())

    command_handler = CommandHandler(command_factory)

    create_socket_and_listen(host=DEFAULT_HOST, port=PORT, command_handler_obj=command_handler)


# pylint: disable=duplicate-code
# no error
__author__ = "Devin Headrick"
__copyright__ = """
    Copyright (C) 2023, [Devin Headrick]
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."""
