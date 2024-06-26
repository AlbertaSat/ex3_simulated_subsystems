# ex3_simulated_subsystems as known as EX3-S3 (EXalta 3 Simulated Satellite Subsystems)

The EX3-S3 project is a collection of simulated subsystems that will be used to test ExAlta3's flight software (FSW) in-silico.

It can either be hosted: on a PC, allowing the FSW to connect over TCP/IP, or on the Zybo Z7-20, allowing the FSW to connect over the hardware interfaces that the subsystems use (I2C, SPI, etc).

## Simulated Subsystem Manager

## Simulated Subsystem Design Philosophy:

- Each simulated subsystem will be created to run independently from the rest of the simulated system as a full python program.
    - This can be done by creatine a `if __name__ == "__main__":` block in the subsystem's main file where code will go that will start a process that will run the subsystem. This process must either: contain a TCP/IP socket to communicate to a respective flight softwares subsystems TCP/IP interface, or through the proper hardware interface that subsystem uses (I2C, SPI, etc) on the Zybo Z7-20.
- Each simulated subsystem should be a class, one that contains functions representing the methods of interaction with the subsystem.
    -  These should be both accessable through the method provided in the `if __name__ == "__main__":` block through the TCP/IP interface and by importing the python file as a module and calling the methods directly (there should be a method for starting the subsystem, stopping the subsystem, and getting the subsystems state for the s3 manager to use).
- Each subsystem will have a dictionary representing its internal state, which may include parameters, settings.
    - This internal state should be properly managed and updated by the subsystems methods.
- If the External Simulation does not provide data for a given subsystem, the subsystem should be able to run independently of the External Simulation using locally provided data.
- Object Oriented design principles and clean code practices should be used as much possible! See: https://gist.github.com/wojteklu/73c6914cc446146b8b533c0988cf8d29

### Documentation 
- 

&nbsp;

Please see [the contribution guidelines](.github/CONTRIBUTING.md) for expectations with contributing, such as branch naming conventions and branching etiquette.


