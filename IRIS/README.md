# IRIS Simulated Subsystem
## Overview
IRIS is a system on ExAlta3 which is responsible for capturing and storing images of Earth's surface, the OBC will communicate with the IRIS to obtain images to send to the ground station

### Data types:
- Command(list)
    - list is a list representing a command received, contains type of call, command key, and any parameters to be passed
    - Currently, Command requires contents passed in list form [0] is key, and then [n] parameters
- IRISSubsytem()
    - All executable commands available through HELP

&nbsp;
## TO-DO
- Add more commands

### Documentation 
- Currently the subsystem expects commands to be made in the form CMD:PARAM:PARAM(S)...
- Currently all commands return a response for debugging purposes - may remove this later
- As we do not know the expected returns all responses are just placeholders.

### Commands
    'TKI': take one image
    'RST': reset to default
    'FTI': fetch image, params: # images to fetch 
    'FTH': fetch housekeeping
    'STT': set time, params: time to set
    'HELP': list commands and their params

## Usage
- The server is run through python PORT is whatever port you wish to use, or leave blank for default port 1821:
```python
python3 ./iris_simulated_server.py PORT
```
- Currently a simple client side is implemented again default port is 1821:
```python
python3 ./iris_client_server.py PORT
```

Once running, type CMD:PARAM1:PARAM2:PARAM(s) to run command 'CMD' with parameters 'PARAM1', 'PARAM2'... and receive its output message

Command EXIT closes both server and client

Example Usage:
```python
USR@usr:.../ex3_simulated_subsystems/IRIS$ python3 iris_simulated_client.py
HELP

Receiving response...
Abbrev: #parameters
TKI: 0
RST: 0
FTI: 1
FTH: 0
STT: 1
HELP: 0

Continue Commands

TKI

Receiving response...
Increased NumImages by 1
Continue Commands

TKI

Receiving response...
Increased NumImages by 1
Continue Commands

FAIL

Receiving response...
ERROR: command FAIL invalid, type 'HELP' for more info
Continue Commands

FTI:3

Receiving response...
Successfully saved 2 images

Continue Commands

EXIT
USR@usr:.../ex3_simulated_subsystems/IRIS$
```
