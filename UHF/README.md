# Simulated UHF Documentation

## Usage

The UHF lies between the communications subsystem and the groundstation in the tall thin architecture. The simulated UHF is designed to be able to connect to 2 TCP clients on ports 1234 (Communications handler) and 1235 (Groundstation). Messages sent from one port will be "echoed" to the other port to simulate the sending of messages between groundstation and space craft (Unless the space craft sends a command, see below section "How to Modify Beacon Contents").

The generic_client.py program can act as a basic simulated groundstation and communications handler. It can send and receive messages through standard IO. This program takes a single command line argument, which is the port it would like to connect to. To test the simulated UHF use the generic client programs like so:

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

## How to Modify Beacon Contents

In order to change the contents of the beacon message from the default: "beacon", the simulated UHF will need to recieve a command (specifically formatted message) from the communications handler TCP client. The command format is as follows:

``` text

MOD_UHF:<new beacon message here>

```

The command needs to be formatted in this manner because the simulated UHF logic checks for two things upon receiving a message.

1. It checks if the clients port (client that is currently receiving the message) is the communications side client port.
2. It checks if the substring "MOD_UHF" is in the message.

Note that the message is split on the global constant called "DELIMITER" within the simulated_uhf.py file which is assigned a string containing a colon (":"). The colon needs to be used as a delimiter in the command because the program expects it. Failure to use a colon as the delimiter will not successfully change the beacon message.

## Handling Clients Accross Threads

During satellite operation we will have times where the UHF loses connection with the groundstation. Because of this the simulated UHF provides
functionality to enable clients to disconnect and reconnect to the server at any time. But because the client socket objects are shared between
multiple threads in the simulated UHF program, we use a mutable data structure in python to act like a pointer to the socket objects. In conjunction with using a lock we can share this dictionary accross threads, so when a client disconnects and the simulated UHF attempts to reconnect (using search_client function) the new client socket object created is shared across threads via the client_pointer dictionary.

Note that when a client disconnects, the simulated UHF will essentially stop all threads and operations and wait for the client to reconnect.
