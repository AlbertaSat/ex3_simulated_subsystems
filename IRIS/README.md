# IRIS Simulated Subsystem
## Overview
IRIS is a system on ExAlta3 which is responsible for capturing and storing images of Earth's surface, the OBC will communicate with the IRIS to obtain images to send to the ground station

### Data types:
- Command(list)
    - list is a list representing a command received, contains type of call, command key, and any parameters to be passed
    - Currently, Command requires contents passed in list form where [0] is call type, [1] is key, and then parameters
- IRISSubsytem()
    - All executable commands available through REQUEST:HELP

&nbsp;
## TO-DO
- [ ] Make the server more object-oriented
- [ ] Create a dockerfile associated with the subsystem
- [ ] Implement a photo storage system and begin setting up sending photo transfers
- [ ] Clean up the IRISSubsystem, (potentially make commands and states more object oriented)

### Documentation 
- Currently the subsystem expects commands to be made in the form CALLTYPE:CMD:PARAM:PARAM(S)...
- In order to receive a response, the client must use calltype "REQUEST"
- No command is actually implemented as we do not know the expected returns

## Usage
- The server is run through python PORT is whatever port you wish to use, or leave blank for default port 1821:
```python
python3 ./iris_simulated_server.py PORT
```
- Currently a simple client side is implemented again default port is 1821:
```python
python3 ./iris_client_server.py PORT
```

