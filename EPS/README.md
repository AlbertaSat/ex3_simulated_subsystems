# Usage Instructions for EPS Subsystem

## Overview
The EPS subsystem communicates using TCP sockets. Commands are sent as strings to the socket server, which parses the input and performs actions accordingly. These commands fall into three categories:

1. **Request** - Retrieve the current value of a parameter.
2. **Update** - Modify a parameter's value.
3. **Execute** - Perform an action, such as resetting the device.

## Prerequisites
1. **Python 3.x** installed on your system.
2. **Netcat (nc)** or any TCP client to send commands to the server.
3. Host IP (`127.0.0.1` by default) and port (`1801` by default).

## Starting the EPS Subsystem
1. Clone this repository and navigate to the directory containing `eps_subsystem.py`.
2. Start the subsystem server by running:
   ```bash
   python3 eps_subsystem.py
   ```
   Optionally, specify a custom port:
   ```bash
   python3 eps_subsystem.py 1234
   ```
3. The server will now listen for incoming commands.

## Sending Commands
You can interact with the EPS subsystem by sending commands using `netcat` or any TCP client.

### 1. **Request Commands**
Use these commands to retrieve the value of a parameter.
- **Syntax**: `request:<parameter_name>`
- **Example**:
   ```bash
   echo -n "request:Voltage" | nc 127.0.0.1 1801
   ```
- **Expected Output**:
   ```
   Voltage:5.24
   ```

#### Valid Parameters for Request:
- `Temperature` - Current temperature in degrees Celsius.
- `Voltage` - Current voltage in volts.
- `Current` - Current in amps.
- `BatteryState` - Current state of the battery.
- `WatchdogResetTime` - Time remaining for the watchdog reset in hours.
- `EPSState` - State of EPS (ON/OFF).

### 2. **Update Commands**
Use these commands to modify the value of a parameter.
- **Syntax**: `update:<parameter_name>:<new_value>`
- **Example**:
   ```bash
   echo -n "update:WatchdogResetTime:48.0" | nc 127.0.0.1 1801
   ```
- **Expected Output**:
   ```
   Updated WatchdogResetTime to 48.0
   ```

#### Updatable Parameters:
- `Temperature` - Current temperature in degrees Celsius.
- `Voltage` - Current voltage in volts.
- `Current` - Current in amps.
- `WatchdogResetTime` - Time remaining for the watchdog reset in hours.

### 3. **Execute Commands**
Use these commands to perform predefined actions on the EPS subsystem.
- **Syntax**: `execute:<command_name>`
- **Examples**:

#### a. Reset the Device
Resets the EPS subsystem to its default state.
- **Command**:
   ```bash
   echo -n "execute:ResetDevice" | nc 127.0.0.1 1801
   ```
- **Expected Output**:
   ```
   Device reset to default state
   ```

#### b. Reset All Subsystems
Resets all subsystems to their default state.
- **Command**:
   ```bash
   echo -n "execute:ResetSubsystems" | nc 127.0.0.1 1801
   ```
- **Expected Output**:
   ```
   Subsystems reset to default state
   ```

#### c. Turn On a Subsystem
Turns on a specific subsystem by name.
- **Command**:
   ```bash
   echo -n "execute:SubsystemOn:GPS" | nc 127.0.0.1 1801
   ```
- **Expected Output**:
   ```
   GPS turned ON
   ```

#### d. Turn Off a Subsystem
Turns off a specific subsystem by name.
- **Command**:
   ```bash
   echo -n "execute:SubsystemOff:GPS" | nc 127.0.0.1 1801
   ```
- **Expected Output**:
   ```
   GPS turned OFF
   ```
#### e. Check the state of a Subsystem
Checks if the subsystem is ON or OFF.
- **Command**:
   ```bash
   echo -n "execute:SubsystemState:GPS" | nc 127.0.0.1 1801
   ```
- **Expected Output**:
   ```
   GPS is OFF/ON
   ```

#### f. Turn On EPS
Turns on the EPS.
- **Command**
   ```bash
   echo -n "execute:TurnOnEPS" | nc 127.0.0.1 1801
   ```

#### g. Turn Off EPS
Turns off the EPS.
- **Command**
   ```bash
   echo -n "execute:TurnOffEPS" | nc 127.0.0.1 1801
   ```

#### Supported Subsystems:
- `ADCS`
- `Deployables`
- `DFGM`
- `GPS`
- `IRIS`
- `UHF`
- `AntennaBurnWireGPIO`
- `UHFBurnWireGPIO`

