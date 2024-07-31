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
