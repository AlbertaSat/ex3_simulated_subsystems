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
    'HELP': list commands and their params
    ----- System --------
    'ON': turn camera on
    'OFF': turn camera off
    'RST': reset to default
    ----- Images --------
    'TKI': take one image
    'FTI': fetch image, params: # images to fetch 
    'FNI': fetch number of images
    'FSI': fetch size of image, params: image # to fetch size of
    'DTI': delete image, params: image # to delete
    ----- Housekeeping --------
    'STT': set time, params: time to set
    'FTT': fetch current time
    'FTH': fetch housekeeping
    

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
HELP: 0
TKI: 0
RST: 0
FTI: 1
FTH: 0
STT: 1
FNI: 0
FSI: 1
OFF: 0
ON: 0
FTT: 0
DTI: 1

Continue Commands

TKI

Receiving response...
Camera is powered off
Continue Commands

ON

Receiving response...
Camera successfully turned on
Continue Commands

TKI

Receiving response...
Increased NumImages by 1
Continue Commands

TKI

Receiving response...
Increased NumImages by 1
Continue Commands

FTI:2

Receiving response...
Successfully saved 2 images

Continue Commands

FTI:4

Receiving response...
Successfully saved 2 images

Continue Commands

OFF

Receiving response...
Camera successfully turned off
Continue Commands

FTI:1

Receiving response...
Successfully saved 1 images

Continue Commands

FTT

Receiving response...
1707677962
Continue Commands

STT:123

Receiving response...
Time updated to 123
Continue Commands

FTT

Receiving response...
123
Continue Commands

FSI:1

Receiving response...
Image 1 is 6555 bytes.
Continue Commands

FAIL

Receiving response...
ERROR: command FAIL invalid, type 'HELP' for more info or EXIT to exit
Continue Commands

RST

Receiving response...
Factory reset performed.
Continue Commands

FTH 

Receiving response...
PowerStatus: 1 SensorStatus: 0 NumImages: 0 MaxNumImages: 20 Time: 123 Images: ./Server_Photos/ ImageExt: .jpeg TempVIS: 25 TempNIR: 25 TempGATE: 25 TempFLASH: 25 SoftwareVersion: 1.0 DateTime: 1707677962 
Continue Commands

EXIT 
```
