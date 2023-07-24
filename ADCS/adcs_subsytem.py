"""This python program represents a simulated version of the ADCS subsystem component for ExAlta3.

For now the sub system communicates with strings over a TCP socket. The strings are parsed into a 
command type and associated data.

Until we know more system specs I am assuming there are three types of commands that can be sent: 
    - Request - Request a paramater from the state dictionary
    - Update  - Update a parameter in the state dictionary
    - Execute - Execute a command (e.g. reset watchdog timer, deploy magnetometer boom, save img, save config, initiate XXXXXX, etc)

# Example to update the WatchdogResetTime:
     update:WatchdogResetTime:48.0

# Example to request the Voltage:
    request:Voltage

# Example to execute a ResetWatchdogTimer command:
    execute:ResetWatchdogTimer

For now you can test your commands using netcat (nc) from the command line, and piping the command 
to the socket from a seperate text file. 



*************************************************************FOR WINDOWS USERS*************************************************************

I do not believe the netcat (nc) command exists in the Windows Powershell. What I used was MobaXTerm as
I had it installed from a previous course AND it comes with the netcat (nc) command.

There are then two steps required to run this program and send commands to it:

1. Run the python script, I call it from Windows Powershell with this command "python .\eps_subsystem.py"

2. Use the following command in the MobaXTerm terminal to connect to the socket created in the python script "nc [DEFAULT_HOST] [DEFAULT_PORT]" (e.g., nc 127.0.0.1 1801)

*It is important to note that if you give an argument to the python script, it creates a socket using that argument as the port number, so then when calling the 
netcat command, you must use that same argument

From there you simply type your commands into the MobaXTerm terminal (e.g., update:WatchdogResetTime:5.0), and hit enter to send the command to the .py script


"""

import sys
import socket

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1801
COMMAND_DELIMITER = ':'


default_adcs_state = {
    'ATTITUDE_ANGLE_X': 32,         
    'ATTITUDE_ANGLE_Y': 5.24,       
    'ATTITUDE_ANGLE_Z': 1.32,       
    'ERROR_FLAGS': 0b00000000,
    'WatchdogResetTime': 24.0,       # in hours
}

adcs_state = default_adcs_state


class RequestDataCommand():  # pylint: disable=too-few-public-methods
    """Execute a 'request' type command to get the current value of a parameter"""

    def execute(self, params=None):
        """
        Args:
            params (list): Name of the parameter to request from the EPS subsystem state
        Returns:
            str: A string containing the requested parameter and its associated value 
        """
        print("Request command received: " + params[0])
        if params and len(params) == 1 and params[0] in adcs_state:
            return f"{params[0]}:{adcs_state[params[0]]}"
        return "ERROR: Invalid request command \n"


class UpdateParameterCommand():  # pylint: disable=too-few-public-methods
    """Execute an 'update' type command to update a parameter value

    Updateable parameters are defined in the updateable_parameters tuple.
    """

    updatable_parameters = ('WatchdogResetTime', 'ERROR_FLAGS', 'ATTITUDE_ANGLE_X', 'ATTITUDE_ANGLE_Y', 'ATTITUDE_ANGLE_Z')

    def execute(self, params=None):
        """
        Args:
            params (list): Name of the state parameter to update, and the new value

        Returns:
            str: A string containing the updated parameter and its new value 
        """

        print("Update command received: " + params[0])
        if params and len(params) == 2 and params[0] in self.updatable_parameters:
            adcs_state[params[0]] = params[1]
            return f"Updated {params[0]} to {params[1]}"
        return "ERROR: update command \n"


class ExecuteCommand():  # pylint: disable=too-few-public-methods
    """Execute an 'execute' type command to call a function (do something)

    Executable commands are defined in the executable_commands tuple.
    """

    executable_commands = ('ResetDevice',)

    def execute(self, params=None):
        """
        Args:
            params (list): Name of the function to call 

        Returns:
            str: A string containing the return value from the function call 
        """

        print("Execute command received: " + params[0])
        if params and len(params) == 1 and params[0] in self.executable_commands:
            return f"Command {params[0]} executed"
        return "ERROR: Invalid execute command \n"


# Factory pattern: Command Factory
class CommandFactory:  # pylint: disable=too-few-public-methods
    """Factory class to create command objects based on command type"""

    def create_command(self, command_type):
        """Create a command object based on the command type
        Args:
            command_type (str): The type of command to be created

        Returns:
            Command: A command object of the associated command type
        """

        if command_type == 'request':
            return RequestDataCommand()
        if command_type == 'update':
            return UpdateParameterCommand()
        if command_type == 'execute':
            return ExecuteCommand()
        return None


class ADCSCommandHandler:
    """This takes a client socket arg and uses it to listen for commands"""

    def __init__(self, client_socket):
        self.client_socket = client_socket

    def handle_command(self):
        """Listen for commands from the client socket and processes them"""
        while True:
            try:
                data = self.client_socket.recv(1024).decode().strip()
                parsed_command = self.parse_command(data)
                self.process_command(parsed_command)

            except KeyboardInterrupt:
                break

            except BrokenPipeError:
                print("Client disconnected abruptly")
                break

        self.client_socket.close()

    def parse_command(self, command):
        """Parse the command into consituent command type, and associated data

        Args:
            command (str): A decoded and stripped string containing the command

        Returns:
            str: A decoded and stripped string containing the command
        """
        return command.split(COMMAND_DELIMITER)

    def process_command(self, command):
        """Process command data based on the command type

        Command types are either: update, request, or execute. This function 
        relies on the pattern factory to creates a command object for the 
        associated command type.

        Args:
            command_type (str): The type of command to be processed
            params (list): The associated data for the command

        Returns:
            str: A string containing the response to the command
        """

        command_type = command[0]
        params = command[1:]

        command_factory = CommandFactory()
        command_obj = command_factory.create_command(command_type)

        if command_obj is not None:
            response = command_obj.execute(params)
        else:
            response = "ERROR: Invalid command type \n"

        try:
            self.client_socket.sendall(response.encode())
        except BrokenPipeError:
            print("Client disconnected abruptly")
            self.client_socket.close()

if __name__ == "__main__":
    # If there is no arg, port is default otherwise use the arg
    PORT = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT

    print(f"Starting ADCS subsystem on port {PORT}")

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
                    handler = ADCSCommandHandler(conn)
                    handler.handle_command()

            except BrokenPipeError as e:
                print(f"Client connection closed: {e}")
