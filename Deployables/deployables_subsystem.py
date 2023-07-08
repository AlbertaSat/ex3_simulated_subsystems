"""This python program represents a simulated version of the Deployables (GPIOS) subsystem 

Each deployable is associated with a burwire pin, and a single feedback switch pin that indicates 
whether the deployable has been successfully deployed. Each Pin represents a GPIO on the OBC.

Burnwire GPIOS are OUTPUTS
Feedback Switch GPIOS are INPUTS

The Fprime component will read these simulated feeback switches state (HIGH or LOW).
Timers activated upon a burnwire set HIGH simulate the feedback switch state changing.
The Fprime component will be responsible for keeping track of the state of the deployables.

Switches are assumed to be normally open, meaning: 
    A switch pin reading HIGH indicates that the deployable has been successfully deployed.

For now the sub system communicates with the OBC using strings over a TCP socket.

Until we know more system specs I am assuming there are 2 types of commands that can be sent: 
    - Burwire Set - Set a GPIO pin HIGH or LOW (toggle a burnwire)
    - Switch Request - Request a GPIO value (get feedback switch state)

# Example setting the DFGM burnwire active 
    BURNWIRE_SET_COMMAND:DFGM:1

# Example requesting the state of the DFGM feedback switch
    SWITCH_REQUEST_COMMAND:DFGM

For now you can test your commands using netcat (nc) from the command line, and piping the command 
to the socket from a seperate text file. I have also added a brief bash script to test this program.

Usage: deployables_subsystem.py 
"""

import sys
import threading
import random

sys.path.append('..') # Add parent directory to path so we can import modules from there
import socket_stuff # pylint: disable=C0413
import command_handler # pylint: disable=C0413


DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1811


BURNWIRE_SET_COMMAND = "burnwire_set"
SWITCH_REQUEST_COMMAND = "switch_request"

BURNWIRE_PIN = "burnwire_pin"
SWITCH_PIN = "switch_pin"


# Each of the following pins variables represents a gpio.
# 0 = LOW, 1 = HIGH
default_deployables_state = {
    'DFGM': {
        BURNWIRE_PIN: 0,
        SWITCH_PIN: 0,
    },
    'UHF_P': {
        BURNWIRE_PIN: 0,
        SWITCH_PIN: 0,
    },
    'UHF_Z': {
        BURNWIRE_PIN: 0,
        SWITCH_PIN: 0,
    },
    'UHF_N': {
        BURNWIRE_PIN: 0,
        SWITCH_PIN: 0,
    },
    'UHF_S': {
        BURNWIRE_PIN: 0,
        SWITCH_PIN: 0,
    },
    'SOLAR_S': {
        BURNWIRE_PIN: 0,
        SWITCH_PIN: 0,
    },
    'SOLAR_P': {
        BURNWIRE_PIN: 0,
        SWITCH_PIN: 0,
    },
}

# For now just start the program with default state. Later we will want to inject a state on
# startup to test different scenarios
deployables_state = default_deployables_state


def simulate_deployable(deployable_component, burnwire_pin_value):
    """Simulate a deployable by setting the burnwire pin HIGH, and then creating a timer thread  
    that will setting the switch pin HIGH after a delay.

    Args:
        deployable_component (str): The name of the deployable component to simulate
        burnwire_pin_value (int): The value to set the burnwire pin to
    """

    #If  burnwire pin is already high, then ignore
    if burnwire_pin_value == 1 and deployables_state[deployable_component][BURNWIRE_PIN] == 1:
        return "ERROR: Burnwire already set high \0"

    #If burnwire pin is being set high from a low state
    if burnwire_pin_value == 1 and deployables_state[deployable_component][BURNWIRE_PIN] == 0:
        # Set the burnwire pin HIGH (begin burn)
        deployables_state[deployable_component][BURNWIRE_PIN] = 1

        # Pick a random timer value between 5 and 30 seconds
        timer_val = random.randint(5, 30)

        # Create a timer thread to set the switch pin HIGH after a delay
        timer_thread = threading.Timer(timer_val, set_switch_pin_high, args=[deployable_component])
        timer_thread.start()
        return f"Burnwire for {deployable_component} set high. Timer set for {timer_val} \0"

    #If burnwire pin is being set low
    deployables_state[deployable_component][BURNWIRE_PIN] = 0
    return "Burnwire for {deployable_component} set low \0"


def set_switch_pin_high(deployable_component):
    """Set the switch pin high. This means the deployable was deployed successfully.
    Once set high this value will never be changed for the life of the program. 

    This will check that the burnwire pin is still high before setting the switch pin high.
    Otherwise if the burnwire pin is set back to low before timer expires, the switch pin stays low.

    Args:
        deployable_component (str): The name of the deployable component to simulate
    """

    # If the burnwire pin is still high, set the switch pin high
    if deployables_state[deployable_component][BURNWIRE_PIN] == 1:
        deployables_state[deployable_component][SWITCH_PIN] = 1
        print(f"Burnwire sim timer end. \
              Switch pin set HIGH for {deployable_component}", flush=True)
    else:
        print(f"Burnwire sim timer end. \
              Switch pin left LOW for {deployable_component}", flush=True)


class SetBurnwireCommand():  # pylint: disable=too-few-public-methods
    """Execute a 'BURNWIRE_SET_COMMAND' type command to set a GPIO pin to HIGH or LOW"""

    def execute(self, params=None):
        """
        Args:
            params (list): Name of the burnwire pin to set, and the value to set it to

        Returns:
            (str): A string indicating the burnwire setting, or an ERROR message
        """

        if params and len(params) == 2 and params[0] in deployables_state:
            deployable_component = params[0]
            burnwire_pin_value = params[1]
            return simulate_deployable(deployable_component, int(burnwire_pin_value))
        return "ERROR: Invalid burnwire set command \0"

class RequestSwitchCommand():  # pylint: disable=too-few-public-methods
    """Execute a 'SWITCH_REQUEST_COMMAND' type command to get the current value of a GPIO pin"""

    def execute(self, params=None):
        """
        Args:
            params (list): Name of the state parameter to request

        Returns:
            str: A string containing the request parameter value, or an ERROR message
        """

        if params and len(params) == 1 and params[0] in deployables_state:
            deployable_component = params[0]
            return f"{params[0]}:{deployables_state[deployable_component][SWITCH_PIN]}\0"
        return "ERROR: Invalid switch request command \0"


class DeployablesCommandFactory(command_handler.CommandFactory):  # pylint: disable=too-few-public-methods
    """Extends abstract CommandFactory class to create command objects based on command type"""

    def create_command(self, command_type):
        """Create a command object based on the command type
        Args:
            command_type (str): The type of command to be created

        Returns:
            Command: A command object of the associated command type
        """

        if command_type == BURNWIRE_SET_COMMAND:
            return SetBurnwireCommand()
        if command_type == SWITCH_REQUEST_COMMAND:
            return RequestSwitchCommand()
        return None


if __name__ == "__main__":
    # If there is no arg, port is default otherwise use the arg
    PORT = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT

    print(f"\nStarting Deployables subsystem on port {PORT}\n", flush=True)

    command_factory = DeployablesCommandFactory()

    # Pass the command factory concrete implementation into the command handler
    # Initially the 
    command_handler = command_handler.CommandHandler(command_factory)

    # Create a socket and listen for client connections
    socket_stuff.create_socket_and_listen(DEFAULT_HOST, PORT, command_handler)



# The following is program metadata
__author__ = "Devin Headrick"
__copyright__ = """
    Copyright 2023 [Devin Headrick]
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."""
