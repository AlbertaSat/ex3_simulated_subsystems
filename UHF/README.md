# Simulated UHF Documentation

## How to Modify Beacon Contents

In order to change the contents of the beacon message from the default: "beacon", the simulated UHF will need to recieve a command (specifically formatted message) from the communications side TCP client. The command format is as follows:

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
