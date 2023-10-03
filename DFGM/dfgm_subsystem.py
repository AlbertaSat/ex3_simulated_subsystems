"""This python program represents a simulated version of the DFGM payload component for ExAlta3.

#TODO - explain how dfgm file works

Usage: DFGM_component.py non-default_port_num
"""

import sys
import socket
import time
from struct import pack

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1802

house_keeping_data = {
    "Core Voltage": 5000, # HK 0 (mV)
    "Sensor Temperature": 25, # HK 1 (deg C)
    "Reference Temperature": 25, # HK 2 (deg C)
    "Board Temperature": 25, # HK 3 (deg C)
    "Positive Rail Voltage": 5000, # HK 4 (mV)
    "Input Voltage": 5000, # HK 5 (mV)
    "Reference Voltage": 5000, # HK 6 (mV)
    "Input Current": 1000, # HK 7 (mA)
    "Reserved 1": 0, # HK 8 (Unused)
    "Reserved 2": 0, # HK 9 (Unused)
    "Reserved 3": 0, # HK 10 (Unused)
    "Reserved 4": 0, # HK 11 (Unused)
}

# Contains raw data to be processed by OBC
magnetic_field_tuple = {
    "x_DAC": 1, 
    "x_ADC": 1,
    "y_DAC": 2,
    "y_ADC": 2,
    "z_DAC": 3,
    "z_ADC": 3
}

# There are 100 samples in each packet
magnetic_field_data = [magnetic_field_tuple] * 100

default_packet = {
    "DLE": 0x10, # Data Link Escape
    "STX": 0x02, # Start of Text
    "PID": 1, # Packet ID
    "Packet Type": 1, # Type of data inside packet
    "Packet Length": 1248, # In bytes
    "FS": 100, # Sampling Frequency
    "PPS Offset": 1, # "U32 offset in ticks from last PPS edge"
    "HK_data": house_keeping_data,
    "mag_data": magnetic_field_data, 
    "Board ID": 1,
    "Sensor ID": 1,
    "Reserved 1": 55, # Reserverd 1-5 are unused, but reserved for future use
    "Reserved 2": 55,
    "Reserved 3": 55,
    "Reserved 4": 55,
    "Reserved 5": 55,
    "ETX": 0x03, # End of Text
    "CRC": 0x0000 # Packet info
}

class DFGMSimulator:
    '''TODO - Document class purpose'''

    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.is_first_packet = True
        self.packet = None
        self.house_keeping_bytes = None
        self.magnetic_field_bytes = None
        self.packet_bytes = bytearray(b'')

    def start(self):
        '''TODO - Document function purpose'''
        while True:
            try:
                if self.is_first_packet:
                    self.generate_packet()
                    self.is_first_packet = False
                else:
                    self.update_packet()
                self.format_packet()
                self.send_packet()
                self.print_packet()
                time.sleep(1) # Force packet to send every 1 second
            except BrokenPipeError:
                print("Client disconnected abruptly")
                break
        self.client_socket.close()

    def generate_packet(self):
        '''TODO - Document function purpose'''
        if self.is_first_packet:
            self.packet = default_packet
            self.is_first_packet = False
    
    def update_packet(self):
        '''TODO - Document function purpose'''
        self.packet["PID"] += 1

    def format_packet(self):
        '''TODO - Document function purpose'''
        # Force each house keeping data value to be in uint16 form
        self.house_keeping_bytes = bytearray(b'')
        for HK in house_keeping_data:
            self.house_keeping_bytes.extend(pack("H", house_keeping_data[HK]))

        # Force each magnetic field coordinate value to be in uint16 form
        self.magnetic_field_bytes = bytearray(b'')
        for sample in magnetic_field_data:
            for coordinate in sample:
                self.magnetic_field_bytes.extend(pack("H", sample[coordinate]))

        # Combine and format default packet bytes
        self.packet_bytes = bytearray(b'')
        for packet_section in default_packet:
            packet_section_value = default_packet[packet_section]
            if packet_section in ["DLE", "STX", "PID", "Packet Type", "ETX"]:
                # Force these data packet sections to be in uint8 form
                self.packet_bytes.extend(pack("B", packet_section_value))
            elif packet_section in ["Reserved 1", "Reserved 2", "Reserved 3", "Reserved 4", "Reserved 5"]:
                # Force these data packet sections to be in uint8 form
                self.packet_bytes.extend(pack("B", packet_section_value))
            elif packet_section in ["Packet Length", "FS", "Board ID", "Sensor ID", "CRC"]:
                # Force these data packet sections to be in uint16 form
                self.packet_bytes.extend(pack("H", packet_section_value))
            elif packet_section in ["PPS Offset"]:
                # Force these data packet sections to be in uint32 form
                self.packet_bytes.extend(pack("L", packet_section_value))
            elif packet_section in ["HK_data"]:
                # Append previously packed bytes to this array of bytes
                self.packet_bytes.extend(self.house_keeping_bytes)
            elif packet_section in ["mag_data"]:
                # Append previously packed bytes to this array of bytes
                self.packet_bytes.extend(self.magnetic_field_bytes)

    def send_packet(self):
        '''TODO - Document function purpose'''
        self.client_socket.send(self.packet_bytes)

    def print_packet(self):
        '''TODO - Document function purpose'''
        print("Measured packet size: " + str(len(self.packet_bytes)) + "\n")
        print("Packet Bytes (Hexadecimal): \n" + self.packet_bytes.hex() + "\n")
        print("Packet contents: ")

        for param in self.packet:
            if param == "HK_data":
                # Format HK data in a neat way
                hk_data = self.packet[param]
                print("HK Data:")
                for hk_param in hk_data:
                    print("\t" + str(hk_param) + ": " + str(hk_data[hk_param]))
            elif param == "mag_data":
                # Format Mag data in a "neat" way
                print("Mag Data:")
                # all dummy xyz tuples are same
                print("\t" + str(self.packet[param][0]) + " * 100 samples")
            else:
                print(str(param) + ": " + str(self.packet[param]))
        print("\n\n\n") # Separate packets in console

if __name__ == "__main__":
    # If there is no arg, port is default otherwise use the arg
    PORT = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT

    print(f"Starting DFGM subsystem on port {PORT}\n")

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