""" This Python program represents the server for a simulation of GPS communication.

This sub System communicates with binary strings using SOCK_SEQPACKET and AF_UNIX. 
This server recieves incoming commands from the client and echoes back the requested
information.

At the moment, the three commands are: 
    - time          - Request the time and date
    - latlong       - Request the latitude and longitude information
    - returnstate   - Request the return state (on/off)
    - ping          - Ping the server
    
To test the server/client you must run both files in WSL to ensure the use of a 
UNIX environment. Afterwards you may enter any of the valid commands from the client.
"""
import os
import socket
import sys

PATH="/tmp/server.sock"

def open_server() -> None:
    """
    Opens a listening server
    """
    with socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET) as s:
        s.bind(PATH)
        print(f"Starting server on {PATH}\n")
        while True:
            print(f"Server started on {PATH}\nWaiting for Client.")
            s.listen()
            conn, addr = s.accept()
            with conn:
                print("Client connected.", addr)
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
                        os.remove(PATH)
                        print("Server socket file removed.")
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
        os.remove(PATH)
        print("Server socket file removed.")

if __name__ == "__main__":
    if os.path.exists(PATH):
        os.remove(PATH)
    open_server()
