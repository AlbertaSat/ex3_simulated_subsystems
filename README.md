# ex3_simulated_subsystems

Simulated subsystems for use with the simulated software architecture in AlbertaSats ExAlta3 Mission.

## Simulated system design:

- Each simulated subsystem will be represented by a python program, that will host its own unique TCP/IP server and use a particular socket.
- Each subsystem will have a dictionary representing its parameters / settings, which may be accessed by our simulated OBC FSW
  
- Object Oriented design principles and clean code practices should be used as much possible! See: <https://gist.github.com/wojteklu/73c6914cc446146b8b533c0988cf8d29>

### Documentation

- Each subsystem should define its usage in a docstring at the top of the main subsystem source file.

&nbsp;

Please see [The Contributing README](Contributing_README.md) for expectations with contributing, such as branch naming conventions, branching etiquette, and issue submission.
