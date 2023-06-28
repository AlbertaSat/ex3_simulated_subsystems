# ex3_simulated_subsystems
Simulated subsystems for use with the simulated software architecture in AlbertaSats ExAlta3 Mission. 

## Simulated system design:
- Each simulated subsystem will be represented by a python program, that will host its own unique TCP/IP server socket.
- Each subsystem will have a dictionary representing its parameters / settings, which may be accessed by our simulated OBC (via Fprime application for now) 
- Each subsystem will have have a command handler, that listens its associated TCP/IP server socket. A command parser will parse received commands, and handle them accordingly. 
- Object Oriented design principles and clean code practices should be used as much possible! See: https://gist.github.com/wojteklu/73c6914cc446146b8b533c0988cf8d29
### Documentation 
- Each command the subsystem is expected to receive should be included in a tuple.

&nbsp;

Please see Contributing_README.md for expectations with contributing, such as branch naming conventions and branching etiquette 


