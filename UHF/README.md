# Simulated UHF Documentation

## Usage

The UHF lies between the communications subsystem and the groundstation in the tall thin architecture. The simulated UHF is designed to be able to connect to 2 TCP clients on ports 1234 (Communications handler) and 1235 (Groundstation). Messages sent from one port will be "echoed" to the other port to simulate the sending of messages between groundstation and space craft (Unless the space craft sends a command, see below section "How to Modify UHF Parameters").

The generic_client.py program can act as a basic simulated groundstation and communications handler. It can send and receive messages through standard IO. This program takes a single command line argument, which is the port it would like to connect to. To test the simulated UHF use the generic client programs like so:

### With Script

Cd to UHF directory within ex3_simulated_subsystems repository:

``` bash
cd UHF
```

Run bash script to boot terminals for simulated UHF and two generic clients.

``` bash
./test_sim_uhf.sh
```

You can confirm the clients connected to the simulated UHF tcp servers by looking out at the output on the terminal for the simulated UHF.

``` text
Connected to ('127.0.0.1', 56812)
Connected to ('127.0.0.1', 60710)
```

Then verify that the beacon is being transmitted to groundstation.

``` text
Connected to 127.0.0.1:1235
Received: beacon
```

Now you can send messages between the groundstation and comms handler by typing messages in their terminal via standard input.

GS Terminal

``` text
Hello from gs
```

you should soon see:

comms handler Terminal

``` text
Received: Hello from gs
```

Next, verify you can send commands to UHF via comms handler side terminal (In reality the gs would send the command and comms handler would direct the command to the UHF handler, which would modify the UHF parameters. This is merely for demonstration/testing purposes).

``` text
UHF:SET_MODE:6
```

to learn more about sending commands see the section below "How to Modify UHF Parameters".

### Without Script

Start the simulated UHF

``` bash
python3 simulated_uhf.py
```

Start Communications handler (In seperate terminal session)

``` bash
python3 generic_client.py 1234
```

Start Groundstation (In seperate terminal session)

``` bash
python3 generic_client.py 1235
```

Now test communication between generic clients by typing a message and hitting enter in either one of the generic client terminal sessions. If it is set up correctly you should see the message received by the other generic client by standard output in the respective terminal session.

In order to use the simulated UHF program with other software the process is much the same. Start by running the simulated_uhf.py program, then connect to the UHF by using a separate program using hostname 127.0.0.1 and ports 1234 and 1235.

## How to Modify UHF Parameters

In order to change the operating parameters of the UHF, the simulated UHF will need to recieve a command (specifically formatted message) from the communications handler TCP client. The command format is as follows:

``` text

system:request:data

```

__system__: The system portion of the message is just the name of the subsystem. The only acceptable possibility for this value is the string "UHF". If any other string is entered a message will be sent to comm handler telling it an invalid system was given. This is merely measure taken in case future functionality needs to be added to the function that processes commands.

__request__: This part of the command is what we are asking the UHF to do. There are 6 possible options currently and more can be added in the future if neccesary.

- "GET_MODE": This command will send back the value of the current mode for the UHF to the comms handler.
- "SET_MODE": This command will set the mode with the value of the "data" portion of the command. Data must be a valid integer to successfully set mode. Otherwise error messge will be returned to comms handler.
- "GET_BEACON": This command will send back the value of the current beacon string for the UHF to the comms handler.
- "SET_BEACON": This command will set the beacon string with the value of the "data" portion of the command.
- "GET_BAUD_RATE": This command will send back the value of the current baud rate for the UHF to the comms handler.
- "SET_MODE": This command will set the baud rate with the value of the "data" portion of the command. Data must be a valid integer to successfully set baud rate. Otherwise error messge will be returned to comms handler.

The command needs to be formatted in this manner because the simulated UHF logic checks for two things upon receiving a message.

1. It checks if the clients port (client that is currently receiving the message) is the communications side client port.
2. It checks if the substring "UHF:" is in the message.

Note that the message is split on the global constant called "DELIMITER" within the simulated_uhf.py file which is assigned a string containing a colon (":"). The colon needs to be used as a delimiter in the command because the program expects it. Failure to use a colon as the delimiter will not successfully change the beacon message.

If a "get" style command is given, the data portion of the command will not be used. but it is still neccesary to add the delimiter at the end of the message, otherwise the action will not be performed. For example if we want to get the value of the beacon, the data portion of the command is not neccesary so we send the following command to the UHF through the comms handler:

``` text

UHF:GET_BEACON:

```

As previously mentioned because the data portion of the command is not use we can also do:

``` text

UHF:GET_BEACON:2132132u

```

Either will successfully send the beacon string value to the comms handler.

__Examples of command using "data" field__:

``` text

UHF:SET_BEACON:This is my new beacon msg

```

``` text

UHF:SET_BAUD_RATE:4500

```

``` text

UHF:SET_MODE:3

```

## Handling Clients Across Threads

During satellite operation we will have times where the UHF loses connection with the groundstation. Because of this the simulated UHF provides
functionality to enable clients to disconnect and reconnect to the server at any time. But because the client socket objects are shared between
multiple threads in the simulated UHF program, we use a mutable data structure in python to act like a pointer to the socket objects. In conjunction with using a lock we can share this dictionary accross threads, so when a client disconnects and the simulated UHF attempts to reconnect (using search_client function) the new client socket object created is shared across threads via the client_pointer dictionary.

Note that when a client disconnects, the simulated UHF will essentially stop all threads and operations and wait for the client to reconnect.
