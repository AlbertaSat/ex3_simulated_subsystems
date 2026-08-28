"""Interface class for the 42 simulation

This class provides an interface to the 42 simulation.
It connects to the 42 simulation via a TCP/IP socket and reads the state data from the simulation.
The state data is then parsed into a dictionary and stored in the state dictionary.
"""

import socket
import time
from os import path
import subprocess
import sys

path_to_script = path.dirname(path.abspath(__file__))
path_to_42 = path.join(path_to_script, "..", "..", "..", "42", "42")
path_to_42_setup = path_to_script + "/ex3"

if __name__ == "__main__":
    sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from ExternalSimulation import ExternalSimulationProvider # pylint: disable=C0413

state_dictionary = {
    'time': 0,
    'magnetometer': [0, 0, 0], # [x, y, z]
    'accelerometer': [0, 0, 0], # [x, y, z]
    'gyroscope': [0, 0, 0], # [x, y, z]
    'gps': {
        "valid": 0,
        "rollover": 0,
        "week": 0,
        "seconds": 0,
        "PosN": [0, 0, 0],
        "VelN": [0, 0, 0],
        "PosW": [0, 0, 0],
        "VelW": [0, 0, 0],
        "Lng": 0,
        "Lat": 0,
        "Alt": 0,
        "WgsLng": 0,
        "WgsLat": 0,
        "WgsAlt": 0,
    }
}

# Interface class for the 42 simulation
class FortyTwo(ExternalSimulationProvider):
    """ExternalSimulationProvider class for the 42 simulation

    This class provides an interface to the 42 simulation.
    Connects to the 42 simulation via a TCP/IP socket and reads the state data from the simulation.
    The state data is then parsed into a dictionary and stored in the state dictionary.
    
    Attributes:
    tx_socket (socket): TCP/IP socket for connecting to the 42 simulation
    simulator (subprocess): 42 simulation process
    
    Methods:
    update: Update the simulation state
    update_state_atomic: Function to read the state of the 42 simulation
    launch_42: Function to launch the 42 simulation
    
    """
    def __init__(self, launch_42=True, exec_path=path_to_42, host='localhost', tx_port=10001):

        # Initialize 42 simulation
        if launch_42:
            self.launch_42(exec_path)

        # # Connect to localhost:10001 TCP/IP socket
        print("Connecting to server")

        count = 0
        while True:
            try:
                self.tx_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.tx_socket.connect((host, tx_port))
                break
            except ConnectionRefusedError:
                count += 1
                if count > 10:
                    print("42 Connection refused. Exiting")
                print("42 Connection refused. Retrying in 1 second")
                time.sleep(1)

        super().__init__("42", state_dictionary)

    def launch_42(self, exec_path=path_to_42):
        """Function to launch the 42 simulation

        Args:
            exec_path (string, optional): Path to the 42 executable. Defaults to path_to_42.
        """
        print(f"Starting 42 simulation at {exec_path}")
        print(f"Using setup file at {path_to_42_setup}")
        # Launch the 42 simulation
        sys.path.append(exec_path)

        # Start the 42 simulation
        self.simulator = subprocess.Popen(
            [exec_path, "../ex3_simulated_subsystems/ExternalSimulation/42/ex3"],
            cwd=exec_path[:-3]
        )

    def update(self):
        while True:
            self.update_state_atomic()
            self.notify()
            time.sleep(0.01)

    def update_state_atomic(self):
        """ Function to read the state of the 42 simulation
        """
        with self.state_mutex:
            # Socket state data from the simulation starts with
            # `TIME: XXXXXXXXXXX` and ends with `[EOF]`
            # Example:
            # TIME 0.0000000000000000
            # DictionaryList[0].Name = x[ y[ z]]
            # DictionaryList[1].Name = x[ y[ z]]
            # ...
            # [EOF]

            # Read message from the simulation
            data = self.tx_socket.recv(1024*128).decode("utf-8")

            print(f"Received: {data}")

            # Split the data into lines
            lines = data.split("\n")

            # Data dictionary initialized in parent class __init__
            self.data = {} # pylint: disable=W0201

            # Parse the data into a dictionary
            for line in lines:
                if line == "[EOF]":
                    break
                if "TIME" in line:
                    # Parse the time
                    self.data["TIME"] = line.split(" ")[1]
                else:
                    # Parse the line into a dictionary
                    line_data = line.split(" = ")
                    name = line_data[0].split("[")[0]
                    field = line_data[0].split("]")[1][1:]
                    i = int(line_data[0].split("[")[1].split("]")[0])
                    values = line_data[1].split(" ")

                    # Check if the name is in the dictionary
                    if name not in self.data:
                        self.data[name] = [{}]

                    # Check if the index is in the dictionary
                    if len(self.data[name]) <= i:
                        self.data[name].append({})

                    # Add the field to the dictionaru
                    if field not in self.data[name][i]:
                        self.data[name][i][field] = []

                    self.data[name][i][field] = values

    def __del__(self):
        if self.tx_socket is not None:
            self.tx_socket.close()
        if self.simulator is not None:
            self.simulator.terminate()

if __name__ == "__main__":
    ft_interface = FortyTwo()
    ft_interface.start()

# pylint: disable=duplicate-code
# no error
__author__ = "Jacques Fourie"
__copyright__ = """
    Copyright (C) 2024, [Jacques Fourie]
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."""