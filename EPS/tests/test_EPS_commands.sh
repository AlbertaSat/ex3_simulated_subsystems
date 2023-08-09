#Testing script for EPS commands with python deployables module
# This script doesnt have any logic and simply sends all various types of commands 
#  to the EPS module to test the commands

PORTNUM=1801

echo "Starting EPS test"

echo "Attempting Temperature Request"
echo 'request:Temperature' | nc -q 1 127.0.0.1 $PORTNUM
sleep 3

echo "Attempting WatchdogResetTime Update"
echo 'update:WatchdogResetTime:300' | nc -q 1 127.0.0.1 $PORTNUM
sleep 3

echo "Attempting Reset Device (return state to default values)"
echo 'execute:ResetDevice' | nc -q 1 127.0.0.1 $PORTNUM
