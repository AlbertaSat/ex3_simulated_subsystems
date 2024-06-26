"""
This python script is a connector interface between Kerbal Space Program (KSP) and the EX3 Simulated Subsystem.

For now it communicates with strings over a TCP socket. The strings are parsed
into a command type and associated data.

The command format is as follows:

<command_type>:<subsystem>:<variable>[:<data>]

where:
    <command_type> is the type of command to be processed `request`, `update`, `execute`
    <subsystem> is the subsystem to which the command is for 
    <variable> is the data point to be processed (TODO: change the wording of this to make sense)
    <data> is the data associated with the command
    
example:

request:daedalus:gps
request:daedalus:temperature
execute:daedalus:solar_s
execute:daedalus:uhf_n
"""

import time
import krpc
import sys
import json
import socketserver

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 3000

class DaedalusInterface:
    def __init__(self, conn):
        self.conn = conn
        
    def process_command(self, command_type, command):
        """Processes the command for the Daedalus subsystem

        Args:
            command_type (string): Type of command to be processed (request, update, execute)
            command (string): Command to be processed (gps, temperature, etc.)

        Returns:
            json or null: will return the data requested or null if no data is returned
        """
        # Logic for multi part commands
        try:
            func = None
            if "solar" in command or "uhf" in command:
                command = command.split("_")
                print(f"Multi part command: {command_type}_{command[0]}")
                func = getattr(self, f"{command_type}_{command[0]}")
                if func:
                    print(f"Executing multi part command: {command_type}_{command[0]}")
                    return func(command[1])
            else:
                func = getattr(self, f"{command_type}_{command}")
                if func:
                    return func()
        except AttributeError:
            print(f"Invalid command: {command}")
            return {"error": "Invalid command"}

    def request_gps(self):
        """Gets the GPS data of the Daedalus module

        Returns:
            object: GPS data object with latitude, longitude, altitude, and UTC time
        """
        gps_data = {
            "latitude": self.conn.space_center.active_vessel.flight().latitude,
            "longitude": self.conn.space_center.active_vessel.flight().longitude,
            "altitude": self.conn.space_center.active_vessel.flight().mean_altitude,
            "UTC": time.time()
        }
        return gps_data
    
    def execute_solar(self, side):
        """Deploys solar panels

        Args:
            side (string): the side of the cubesat the solar panel is on
        """
        print(f"Deploying solar panel on {side}")
        panels = self.conn.space_center.active_vessel.parts.with_tag(f"solar_{side}")
        if panels and len(panels) > 0:
            for panel in panels:
                for module in panel.modules:
                    if module.name == "ModuleROSolar":
                        module.set_action("Extend Solar Panel", True)

    def execute_dfgm(self):
        """Deploys the DFGM
        """
        print("Deploying DFGM")
        dfgm = self.conn.space_center.active_vessel.parts.with_tag("dfgm")
        if dfgm and len(dfgm) > 0:
            for part in dfgm:
                for module in part.modules:
                    if module.name == "Experiment":
                        module.set_action("start: Magnetic Scan", True)

    def execute_uhf(self, side):
        """Deploys UHF antennas

        Args:
            side (string): the side of the cubesat the UHF antenna is on
        """
        print(f"Deploying UHF antenna on {side}")
        antennas = self.conn.space_center.active_vessel.parts.with_tag(f"uhf_{side}")
        if antennas and len(antennas) > 0:
            for antenna in antennas:
                for module in antenna.modules:
                    if module.name == "ModuleAnimateGeneric":
                        module.trigger_event("Extend")

    def request_temperature(self):
        """Gets the temperature of the Daedalus module in degrees Celsius

        Returns:
            float: Temperature in degrees Celsius
        """
        print("Getting daedalus temperature")
        test = self.conn.space_center.active_vessel.parts.with_tag("daedalus")[0]
        
        for module in test.modules:
            if module.name == "Sensor":
                if 'temperature' in module.fields.keys():
                    print(module.fields)
                    print(f"Temperature: {module.fields['temperature']}")
                    return float(module.fields['temperature'].replace(" K", "")) - 273.15

class EX3Interface:
    def __init__(self) -> None:
        self.conn = krpc.connect(name="EX3_SIMULATED_SUBSYSTEM_INTERFACE")
        
        # Load the initial state of the game
        self.reset()
        
        self.exalta3 = self.conn.space_center.active_vessel
        self.daedalus = DaedalusInterface(self.conn)
        
    def reset(self):
        # Resets game state to the initial state
        self.conn.space_center.load("initial_state")
        pass
    
    def status(self):
        return self.exalta3.met
    
    def process_command(self, command):
        command_type = command[0]
        subsystem = getattr(self, command[1]) if hasattr(self, command[1]) and not command[1] == "exalta3" else command[1]
        command = command[2]
    
        if subsystem == "exalta3":
            if command_type == "execute" and command == "reset":
                self.reset()
            elif command_type == "request" and command == "status":
                print("Status of Exalta3")
                return self.status()
            else:
                print(f"Invalid command: {command}")
                return {"error": "Invalid command"}
        elif subsystem:
            return subsystem.process_command(command_type, command)

class TCPServerHandler(socketserver.StreamRequestHandler):
    def __init__(self, request, client_address, server):
        self.ex3_interface = EX3Interface()
        super().__init__(request, client_address, server)
    
    def handle(self) -> None:
        self.wfile.write(b"Welcome to the KSP Interface\n")
        
        while True:
            data = self.rfile.readline().strip()
            print(f"Data: {data}")
            if not data:
                self.wfile.write(json.dumps({"error": "Invalid command"}).encode("utf-8"))
                continue
            print(f"Received: {data}")
            ret = self.process_data(data)
            print(f"Return: {ret}")
            self.wfile.write(ret)
    
    def process_data(self, data):
        print(f"Processing data: {data}")
        command = data.decode("utf-8").split(":")
        
        if command and len(command) >= 3:
            print(f"Command: {command}")
            return json.dumps(self.ex3_interface.process_command(command)).encode("utf-8")
        else:
            print(f"Invalid command: {data}")
            return json.dumps({"error": "Invalid command"}).encode("utf-8")
        

if __name__ == "__main__":
    # If there is no arg, port is default. Otherwise use the arg
    PORT = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    print(f"Starting KSP simulated subsytem interface on port {PORT}\n")
    
    server = socketserver.TCPServer((DEFAULT_HOST, PORT), TCPServerHandler)
    server.serve_forever()

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

                