""" This Python program represents the server for a simulation of GPS communication.

This sub System communicates with binary strings using SOCK_SEQPACKET and AF_UNIX. 
This server recieves incoming commands from the client and echoes back the requested
information.

At the moment, the three commands are: 
    - time          - Request the time and date
    - latlong       - Request the latitude and longitude information
    - returnstate   - Request the return state (on/off)
    - ping          - Ping the server
    
To test the server/client you must run both files in a UNIX environment.
Afterwards you may enter any of the valid commands from the client.
"""
import os
import socket
import sys

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 1810
def open_server(host, port) -> None:
    """
    Opens a listening server
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        while True:
            print(f"Server started on port {port}\nWaiting for client.")
            server.listen()
            conn, addr = server.accept()
            with conn:
                print("Client connected. Addr:", addr)
                while True:
                    command=conn.recv(1024) #buffsize 1024 bytes
                    command=command.decode("utf-8")
                    print(f"Command recieved: {command}.")
                    data=0

                    if command == "disconnect":
                        print(f"Command recieved: {command}.")
                        print("Client disconnected.")
                        break
                    if command == "terminate":
                        print("Closing connection.")
                        sys.exit(0)

                    if command == "time":
                        data=b"[Server] 12:45 am Friday August 23 2024"
                    elif command == "latlong":
                        data=b"[Server] 53.518291, -113.536530)"
                    elif command == "returnstate":
                        data=b"return state on"
                    elif command == "ping":
                        data=b"[Server] ping successful"
                    else:
                        command="invalid command"
                        data=b"[Server] Invalid command."
                    conn.send(data)

if __name__ == "__main__":
    open_server(DEFAULT_HOST, DEFAULT_PORT)
