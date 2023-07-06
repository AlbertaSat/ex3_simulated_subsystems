"""This python program represents a simulated version of the DFGM payload component for ExAlta3.

#TODO - explain how dfgm file works

Usage: DFGM_component.py non-default_port_num
"""

import sys
import socket

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1801

'''TODO: Fill state with actual parameters + dummy values'''
default_packet = {
    "MagneticData": 1,
    "HousekeepingData": 2
}

class DFGMSimulator:
    '''TODO - Document class purpose'''

    def __init__(self, client_socket):
        self.client_socket = client_socket

    def start(self):
        '''TODO - Document function purpose'''
        while True:
            try:
                packet = self.generate_packet()
                # TO DO - Force packet to send every 1 second
                self.send_packet(packet)
            except BrokenPipeError:
                print("Client disconnected abruptly")
                break
        self.client_socket.close()

    def generate_packet(self):
        '''TODO - Document function purpose'''
        # packet = default_packet
        packet = "packet" #temp
        return packet

    def send_packet(self, packet):
        '''TODO - Document function purpose'''
        self.client_socket.send(packet) # To do - figure out what format packet should be sent in (maybe bytes, string, etc.)

if __name__ == "__main__":
    # If there is no arg, port is default otherwise use the arg
    PORT = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT

    print(f"Starting DFGM subsystem on port {PORT}")

    # Create a socket and bind it to the port. Listen indefinitely for client connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Tell OS to reuse socket addr if not previously closed
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((DEFAULT_HOST, int(PORT)))
        s.listen()

        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected with {addr}")
                    simulator = DFGMSimulator(conn)
                    simulator.start()
            except BrokenPipeError as e:
                print(f"Client connection closed: {e}")

# The following is program metadata
__author__ = "Daniel Sacro"
__copyright__ = """
    Copyright (C) 2023, University of Alberta.
    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details."""