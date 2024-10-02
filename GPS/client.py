
""" This Python program represents the client for a simulation of GPS communication.

This sub System communicates with binary strings using SOCK_SEQPACKET and AF_UNIX. 
This server recieves incoming commands from the client and echoes back the requested
information.

At the moment, the three commands are:
    - time          - Request the time and date
    - latlong       - Request the latitude and longitude information
    - returnstate   - Request the return state (on/off)
    - ping          - Ping the server
    - null string   - closes connection
    
To test the server/client you must run both files in WSL to ensure the use of a 
UNIX environment. Afterwards you may enter any of the valid commands from the client.
"""
import socket
path="/tmp/server.sock"

with socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET) as s:
    s.connect(path)
    print("Client connected.")

    commandstr=input("Possible commands: latlong, time, returnstate, ping\n")
    while True:
        command = commandstr.encode('utf-8')
        s.send(command)

        if commandstr == ('terminate' or "disconnect"):
            break
        data=s.recv(1024)
        print(data.decode('utf-8'))
        commandstr=input("possible commands: latlong, time, returnstate, ping\n")

print("Client disconnected.")
sys.exit(0)
