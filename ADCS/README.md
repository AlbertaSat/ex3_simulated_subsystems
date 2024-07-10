# ADCS Simulated Subsystem

## Overview

The ADCS, also known as the Altitude Determination and Control System, is a
system that controls the orientation of ex3.

The ADCS is used to help steer the satellite.

## Commands
All currently implemented commands are listed in the following table
|COMMAND NAME| PARAMETERS | PARAMETER TYPE | RETURN | RETURN TYPE | DESCRIPTION |
|-|-|-|-|-|-|
| `HELP` | N/A | N/A | list of all commands | string | Returns all working commands
| `GS` | N/A | N/A | State of the ADCS ("WORKING" or "OFF") | string | Gets the current state of the ADCS
| `ON` | N/A | N/A | N/A | N/A | Sets the ADCS state to "WORKING"
| `OFF` | N/A | N/A | N/A | N/A | Sets the ADCS state to "OFF" 
| `GWS` | N/A | N/A | Wheel speed x, y, & z | tuple of floats | Records and sends the wheel speed of the ADCS
| `SWS` | Wheel speed x, y, & z | floats in RPM | N/A | N/A | Sets the ADCS wheel speed on all three axes in RPM
| `SC` | N/A | N/A | House keeping data | string | Generates random number for voltage, current, and temperature of the adcs. Also generates an "OK" or "BAD" overall status
| `SMC` | Magnetorquer current x, y, & z | floats in mA | N/A | N/A | Sets the ADCS's magnetorquer current on all three axes in mA
| `GMC` | N/A | N/A | Magnetorquer current x, y, & z | tuple of floats | Records and sends the magnetorquer currents of the ADCS
| `GTM` | N/A | N/A | Time | float in s | Sends the time recorded by the ADCS
| `STM` | Time | float in s | N/A | N/A | Sets the time currently recorded by the ADCS
| `GOR` | N/A | N/A | ADCS angles x, y, z | tuple of floats | Returns the current orientation of the ADCS in degrees
| `RESET` | N/A | N/A | N/A | N/A | Sets the wheel speeds to 0 RPM, and the magnetorquer currents to 0 mA

## Usage

Start the server by running `adcs_server.py`, and connect to the server using some program/utility such as `nc`

```bash
$ python3 .ADCS/adcs_server.py 8000
Starting ADCS subsystem on port 8000
```
Then in a separate terminal process you can connect to the server on localhost:8000. Note if no host or port is specified the program defaults to localhost:42123

## Example usage
Here is an example of connecting to the server sending the `HELP`, `GWS`, and `SWS` command
```
$ nc localhost 8000

HELP
HELP | help (string)
GS | Get State (OFF or WORKING)
ON | Set state WORKING
OFF | Set state OFF
GWS | Get wheel speed (tuple)
SWS:x:y:z | set wheel speed
GMC | get magnetorquer current (tuple)
SMC:x:y:z | set magnetorquer current
SC | Status Check (string)
GTM | Get time (float)
STM:float | Set time
GOR | Get orientation (tuple)
RESET | Resets wheels and magnetorquer 

GWS
(0, 0, 0)

SWS:10.3:-32.4:13.536

GWS
(10.3, -32.4, 13.536)
```

## TODO

- [ ] Convert to a more realistic packet format using Bach's branch
- [ ] Utilize Bach's unittest structure
- [ ] Make a status report transaction code
- [ ] Implement an echo command
