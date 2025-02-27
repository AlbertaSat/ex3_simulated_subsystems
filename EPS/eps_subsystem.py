"""This python program represents a simulated version of the EPS payload for ExAlta3."""
import sys
import socket

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1804
COMMAND_DELIMITER = ':'

default_eps_state = {
    'EPSState' : 'ON',
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

class EPSSubsystem:
    """Handles EPS subsystem state and command execution."""

    def __init__(self):
        self.state = default_eps_state.copy()
        self.subsystems = default_subsystem_state.copy()
        self.eps_on = True

    def handle_command(self, command):
        """Handles commands"""
        parts = command.strip().split(COMMAND_DELIMITER)
        cmd_type = parts[0].lower()

        if cmd_type == "request" and len(parts) == 2:
            return str(self.state.get(parts[1], "Unknown parameter"))

        if cmd_type == "update" and len(parts) == 3:
            value = parts[2]
            if value.replace('.', '', 1).isdigit():
                value = float(value)
                self.state[parts[1]] = value
                return f"{parts[1]} updated to {self.state[parts[1]]}"
            return "Unknown parameter"

        if cmd_type == "execute" and len(parts) == 2:
            return self.execute_command(parts[1])
        if cmd_type == "execute" and len(parts) == 3:
            return self.subsystem_commands(parts[1],parts[2])

        return "Invalid command format"

    def execute_command(self, command):
        """Handles all executable commands"""
        if command == "ResetDevice":
            self.state = default_eps_state.copy()
            return "Device reset to default state"
        if command == "ResetSubsystems":
            if self.eps_on is True:
                self.subsystems = default_subsystem_state.copy()
            return "EPS is off" if not self.eps_on else "Subsystems reset to default state"
        if command == "TurnOnEPS":
            self.eps_on = True
            self.state["EPSState"] = "ON"
            return "EPS turned ON"
        if command == "TurnOffEPS":
            self.eps_on = False
            self.state["EPSState"] = "OFF"
            return "EPS turned OFF"
        return "Unknown command"
    def subsystem_commands(self,command,subsystem):
        "Handles on/off for other subsystems"
        if self.eps_on is False:
            return "EPS is off. Turn on EPS to execute subsystem commands"
        if subsystem not in self.subsystems:
            return "Invalid subsystem"
        if command == "SubsystemOn":
            self.subsystems[subsystem] = True
            return f"{subsystem} turned ON"
        if command == "SubsystemOff":
            self.subsystems[subsystem] = False
            return f"{subsystem} turned OFF"
        if command == "SubsystemState":
            return f"{subsystem} is ON" if self.subsystems[subsystem] else f"{subsystem} is OFF"
        return "Unknown command"

if __name__ == "__main__":
    PORT = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT

    print(f"Starting EPS subsystem on port {PORT}")

    eps = EPSSubsystem()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((DEFAULT_HOST, PORT))
        server_socket.listen()
        print("EPS subsystem listening for connections...")
        while True:
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")

            # Keep connection open for multiple commands
            while True:
                try:
                    data = conn.recv(1024).decode().strip()
                    if not data:
                        print("Client disconnected.")
                        break

                    RESPONSE = eps.handle_command(data)
                    if RESPONSE:
                        conn.sendall((RESPONSE + "\n").encode())

                except ConnectionResetError:
                    print("Client disconnected abruptly.")
                    break  # Exit loop if client forcefully disconnects
            conn.close()  # Close the connection after client disconnects
