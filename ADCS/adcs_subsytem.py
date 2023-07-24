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
                    #handler = EPSCommandHandler(conn)
                    #handler.handle_command()

            except BrokenPipeError as e:
                print(f"Client connection closed: {e}")
