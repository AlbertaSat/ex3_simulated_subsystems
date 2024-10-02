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

path="/tmp/server.sock"

if os.path.exists(path):
    os.remove(path)

with socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET) as s:
    s.bind(path)
<<<<<<< HEAD

=======
        
>>>>>>> cce6b0273e38e72cc4d15505d5ad85ab689d5948
    while True:
        print(f"Starting server on {path}\nWaiting for client.")
        s.listen()
        conn, addr = s.accept()
        with conn:
            print("Client connected.")
            while True:
                command=conn.recv(1024) #buffsize 1024 bytes
                command=command.decode("utf-8")
<<<<<<< HEAD
                data=0
=======
                data=0      
>>>>>>> cce6b0273e38e72cc4d15505d5ad85ab689d5948
                if command == "time":
                    data=b"[Server] 12:45 am Friday August 23 2024"
                elif command == "latlong":
                    data=b"[Server] 53.518291, -113.536530)"
                elif command == "returnstate":
                    data=b"return state on"
<<<<<<< HEAD
                elif command == "ping":
=======
                elif command == "ping": 
>>>>>>> cce6b0273e38e72cc4d15505d5ad85ab689d5948
                    data=b"[Server] ping successful"
                elif command == "terminate":
                    print("Closing connection.")
                    os.remove(path)
                    print("Server socket file removed.")
                    sys.exit(0)
                elif command == "disconnect":
                    print(f"Command recieved: {command}.")
                    print("Client disconnected.")
                    break
                else:
                    command="invalid command"
                    data=b"[Server] Invalid command."

                print(f"Command recieved: {command}.")
                conn.send(data)

    os.remove(path)
    print("Server socket file removed.")
