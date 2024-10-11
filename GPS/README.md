# GPS Simulated Subsystem

## Overview
This is a set of Python programs that simulate communication to the satellite GPS. The system is a listening server that communicates with binary strings over SOCK_SEQPACKET and AF_UNIX

## Commands
|COMMAND NAME| RETURN MESSAGE | DESCRIPTION |
|-|-|-|
| `time` | 12:45 am Friday August 23 2024 |Responds with the time and date
| `latlong` |53.518291, -113.536530| Responds with latitude and longitude coordinates
| `returnstate` | return state on | Responds with the return state (on)
| `ping` | ping successful| Responds with acknowledgement of ping
| `disconnect` | Client disconnected | Disconnects the client from the server while keeping the server active
| `terminate` | Closing connection. Server socket file removed | Disconnects the client from server and closes server connection. Removes the temporary file made during server startup
| `anything else`| Invalid command | Any command not listed above is considered invalid

## Usage
Start the server by first running `server.py` and then `client.py` in seperate terminals, they will connect automatically. You can then begin issuing commands

## Example Usage
Here is an example of connecting to the server and issuing from the client side: 
1. `time` 
2. `latlong`
3. `disconnect`
4. reconnecting by running `client.py`
5. `terminate`

```
$ python3 client.py
Client connected.
Possible commands: latlong, time, returnstate, ping, disconnect, terminate
>>>time
[Server] 12:45 am Friday August 23 2024
Possible commands: latlong, time, returnstate, ping, disconnect, terminate
>>>latlong
[Server] 53.518291, -113.536530)
Possible commands: latlong, time, returnstate, ping, disconnect, terminate
>>>disconnect
Disconnecting
Client disconnected.
$ python3 client.py
Client connected.
Possible commands: latlong, time, returnstate, ping, disconnect, terminate
>>>terminate
Disconnecting
Client disconnected.