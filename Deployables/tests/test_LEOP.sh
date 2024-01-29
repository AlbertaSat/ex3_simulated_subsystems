#!/bin/sh
# Testing script for LEOP with python deployables module
# This script doesnt have any logic and simply sends a request to the
# deployables module to burn a wire and then read the switch


PORTNUM=1811

echo "Starting LEOP test"

# Sends a request to burn a wire
# Arguments:
# 1 - Name of module to print
# 2 - Name of deployable
# 3 - seconds to sleep after switch request (default=1)
send_request() {
	echo "Attempting $1 deployment "
	echo "burnwire_set:${2}:1" | nc -q 1 127.0.0.1 $PORTNUM
	sleep 30
	echo "switch_request:${2}" | nc -q 1 127.0.0.1 $PORTNUM
	sleep ${3:-1}
}

send_request "DFGM" DFGM
send_request "UHF port" UHF_P
send_request "UHF zenith" UHF_Z
send_request "UHF Nadir" UHF_N
send_request "UHF Starboard" UHF_S
send_request "Solar panel Starboard" SOLAR_S
send_request "Solar panel Port" SOLAR_P 0
