
""" This Python program represents the client for a simulation of GPS communication.

This sub System communicates with binary strings using SOCK_SEQPACKET and AF_UNIX. 
This server recieves incoming commands from the client and echoes back the requested
information.

At the moment, the three commands are:
    - time          - Request the time and date
    - latlong       - Request the latitude and longitude information
    - returnstate   - Request the return state (on/off)
    - ping          - Ping the server
    - disconnect    - closes connection to server
    - terminate     - terminates the server and closes connection

    
To test the server/client you must run both files in a UNIX environment.
Afterwards you may enter any of the valid commands from the client.
"""
import socket
import sys

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1999
PATH="/tmp/fifo_socket_gps_device"

def connect(host, port) -> None:
    """
    Connects to server and allows for communication.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        print("Client connected.")

        while True:
            print("Possible commands: latlong, time, returnstate, ping, disconnect, terminate")
            commandstr=input(">>>")
            command = commandstr.encode('utf-8')
            client.send(command)

            if commandstr in ("terminate", "disconnect"):
                print("Disconnecting")
                break
            data=client.recv(1024)
            print(data.decode('utf-8'))

    print("Client disconnected.")
    sys.exit(0)

if __name__ == "__main__":
    connect(DEFAULT_HOST, DEFAULT_PORT)
