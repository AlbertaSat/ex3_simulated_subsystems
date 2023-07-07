#Testing script for LEOP with python deployables module
# This script doesnt have any logic and simply sends a request to the deployables 
#  module to burn a wire and then read the switch


PORTNUM=1811

echo "Starting LEOP test"

echo "Attempting DFGM deployment "
# Send a request to burn the DFGM burnwire 
echo 'burnwire_set:DFGM:1' | nc -q 1 127.0.0.1 $PORTNUM
sleep 30
echo 'switch_request:DFGM' | nc -q 1 127.0.0.1 $PORTNUM

sleep 1

echo "Attempting UHF port deployment "
# Send a request to burn the UHF port burnwire 
echo 'burnwire_set:UHF_P:1' | nc -q 1 127.0.0.1 $PORTNUM
sleep 30
echo 'switch_request:UHF_P' | nc -q 1 127.0.0.1 $PORTNUM

sleep 1

echo "Attempting UHF zenith deployment "
# Send a request to burn the UHF port burnwire 
echo 'burnwire_set:UHF_Z:1' | nc -q 1 127.0.0.1 $PORTNUM
sleep 30
echo 'switch_request:UHF_Z' | nc -q 1 127.0.0.1 $PORTNUM

sleep 1

echo "Attempting UHF Nadir deployment "
# Send a request to burn the UHF port burnwire 
echo 'burnwire_set:UHF_N:1' | nc -q 1 127.0.0.1 $PORTNUM
sleep 30
echo 'switch_request:UHF_N' | nc -q 1 127.0.0.1 $PORTNUM

sleep 1

echo "Attempting UHF Starboard deployment "
# Send a request to burn the UHF port burnwire 
echo 'burnwire_set:UHF_S:1' | nc -q 1 127.0.0.1 $PORTNUM
sleep 30
echo 'switch_request:UHF_S' | nc -q 1 127.0.0.1 $PORTNUM

sleep 1

echo "Attempting Solar panel Starboard deployment "
# Send a request to burn the UHF port burnwire 
echo 'burnwire_set:SOLAR_S:1' | nc -q 1 127.0.0.1 $PORTNUM
sleep 30
echo 'switch_request:SOLAR_S' | nc -q 1 127.0.0.1 $PORTNUM

sleep 1

echo "Attempting Solar panel Port deployment "
# Send a request to burn the UHF port burnwire 
echo 'burnwire_set:SOLAR_P:1' | nc -q 1 127.0.0.1 $PORTNUM
sleep 30
echo 'switch_request:SOLAR_P' | nc -q 1 127.0.0.1 $PORTNUM

