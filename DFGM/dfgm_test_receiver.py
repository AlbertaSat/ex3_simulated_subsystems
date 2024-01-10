"""This python program represents a simulated part of the OBC meant to handle incoming data
from the DFGM payload on ExAlta3.

The program is meant to be used along with dfgm_subsystem.py and mainly serves as a way to
see how data can be received and read from the subsystem.

The program also utilizes the local host IP '127.0.0.1'.

Usage: dfgm_test_receiver.py

Copyright 2024 [Daniel Sacro]. Licensed under the Apache License, Version 2.0
"""

import socket

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1802

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((DEFAULT_HOST, DEFAULT_PORT))
    while True:
        data = s.recv(1248)
        if not data:
            break

        # Print packet contents into a readable form
        print("Packet contents: ")

        # Packet info
        print("DLE: " + str(data[0]))
        print("STX: " + str(data[1]))
        print("PID: " + str(data[2]))
        print("Packet Type: " + str(data[3]))
        print("Packet Length: " + str(int.from_bytes(data[4:6], "little")))
        print("FS: " + str(int.from_bytes(data[6:8], "little")))
        print("PPS Offset: " + str(int.from_bytes(data[8:12], "little")))

        # Housekeeping data
        print("HK Data:")
        print("\tCore Voltage: " + str(int.from_bytes(data[12:14], "little")))
        print("\tSensor Temperature: " + str(int.from_bytes(data[14:16], "little")))
        print("\tReference Temperature: " + str(int.from_bytes(data[16:18], "little")))
        print("\tBoard Temperature: " + str(int.from_bytes(data[18:20], "little")))
        print("\tPositive Rail Voltage: " + str(int.from_bytes(data[20:22], "little")))
        print("\tInput Voltage: " + str(int.from_bytes(data[22:24], "little")))
        print("\tReference Voltage: " + str(int.from_bytes(data[24:26], "little")))
        print("\tInput Current: " + str(int.from_bytes(data[26:28], "little")))
        print("\tReserved 1: " + str(int.from_bytes(data[28:30], "little")))
        print("\tReserved 2: " + str(int.from_bytes(data[30:32], "little")))
        print("\tReserved 3: " + str(int.from_bytes(data[32:34], "little")))
        print("\tReserved 4: " + str(int.from_bytes(data[34:36], "little")))

        # DFGM Tuple
        print("Mag Data: ")
        mag_tuple = "(" + str(int.from_bytes(data[36:38], "little")) + ", "
        mag_tuple += str(int.from_bytes(data[38:40], "little")) + ", "
        mag_tuple += str(int.from_bytes(data[40:42], "little")) + ", "
        mag_tuple += str(int.from_bytes(data[42:44], "little")) + ", "
        mag_tuple += str(int.from_bytes(data[44:46], "little")) + ", "
        mag_tuple += str(int.from_bytes(data[46:48], "little")) + ")"
        print("\t" + mag_tuple + " * 100 samples")

        # Board info
        print("Board ID: " + str(int.from_bytes(data[1236:1238], "little")))
        print("Sensor ID: " + str(int.from_bytes(data[1238:1240], "little")))
        print("Reserved 1: " + str(data[1240]))
        print("Reserved 2: " + str(data[1241]))
        print("Reserved 3: " + str(data[1242]))
        print("Reserved 4: " + str(data[1243]))
        print("Reserved 5: " + str(data[1244]))
        print("ETX: " + str(data[1245]))
        print("CRC: " + str(int.from_bytes(data[1246:1248], "little")))

        print("\n\n")

# The following is program metadata
__author__ = "Daniel Sacro"
__copyright__ = """
    Copyright (C) 2024, University of Alberta.
    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details."""