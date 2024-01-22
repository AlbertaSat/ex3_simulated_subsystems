"""This program is designed to simulate the UHF transceiver on the Ex-Alta 3 satellite.


"""

import sys
import time
#Constants
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1831
COMMAND_DELIMITER = ':'
DEFAULT_STATE_VALUES = {
    'PowerStatus': 1, #1 for on, 0 for off
    'Transmitting': 0, #1 for transmitting, 0 for off
    'Receiving': 0, #1 for recieving, 0 for off
    'Frequency': 300000, #in Hertz
                    
}


#add shutdown command
#can add while loop to make ping every 30 seconds
class UHFSubsystem:
    """Creates the state values for the UHF tranciever"""
    def __init__(self):
        self.state = {
            'PowerStatus': DEFAULT_STATE_VALUES['PowerStatus'],
            'Transmitting': DEFAULT_STATE_VALUES['Transmitting'],
            'Receiving': DEFAULT_STATE_VALUES['Receiving'],
            'Frequency': DEFAULT_STATE_VALUES['Frequency'],
        }

    def transmit(self, frequency):  #pylint:disable=C0116:missing-function-docstring
        self.state['Transmitting'] = 1
        self.state['Frequency'] = frequency
        print('Transmitting Data')

    def receive(self, frequency):   #pylint:disable=C0116:missing-function-docstring
        self.state['Receiving'] = 1
        self.state['Frequency'] = frequency
        print('Receiving Data')

    def shutdown(self): #pylint:disable=C0116:missing-function-docstring
        self.state['PowerStatus'] = 0
        self.state['Frequency'] = 0
        self.state['Receiving'] = 0
        self.state['Transmitting'] = 0
    
    def ping_call(self, package):
        """This function will simulate a transmission or receiving of a packet of data from the OBC or from the ground-station."""
        
        while True:
            print('System ping for: ',package)
            time.sleep(10)


if __name__ == "__main__":
    # If there is no arg, port is default otherwise use the arg
    PORT = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT
    print(f"Starting EPS subsystem on port {PORT}")
    
    uhf = UHFSubsystem()
    uhf.ping_call(123)
        

__author__ = "Rowan Rasmusson"
__copyright__ = """
    Copyright (C) 2023, [Rowan Rasmusson]
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."""