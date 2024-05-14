# ADCS Simulated Subsystem

## Overview

The ADCS, also known as the Altitude Determination and Control System, is a
system that controls the orientation of ex3.

The ADCS is used to help steer the satellite.

## Data types
- x,y,z angle
  - Representable as a triplet?
- x,y,z angular speed
  - Same representation as the x,y,z angle?
- ECI/ECEF/LLH position/velocity (Need definition)
- Coarse and fine sun vector (Need definition)
- Wheel speed
- Magnetic Field (IMU?)
- Comm status
- Rate sensor temperature (sensor measuring the wheel speed?)

## Payload design

- TODO

## TODO
- [ ] Make a status report transaction code
- [ ] Implement an echo command

## Usage

Note: We are missing docker setups for running the unit test. Run using your local environment for now.

_There is now a dockerfile associated with this subsystem, and you are able to
run it using the following command on powershell (please have docker installed)_


```powershell
docker build -t adcs_server .
```

```powershell
docker run -dp 127.0.0.1:8838:8838 adcs_server
```

## Testing Table

| Test Name | Test Description |
| --- | --- | 
| `test_setup` | This test makes sure that the unit testing framework, and mocked objects are functioning as expected. |
