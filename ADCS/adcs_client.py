"""
This will be the main file for the simulated ADCS subsystem.
"""

import sys
import threading

from tcp_server import TCPClient
from adcs_subsystem import ADCSSubsystem


def command_line_handler(argv) -> tuple[int, str]:
    """
    Control flow for what to return depending on the commandline arg.

    **Change here if you need to change the port and address values**

    Returns:
        (PORT, HOST)
    """

    default_host = "127.0.0.1"
    default_port = 42123

    ret_port = int(argv[1]) if len(argv) > 1 else default_port
    ret_host = argv[2] if len(argv) > 2 else default_host

    return ret_port, ret_host


def command_parser(data: bytes):
    """Splits the command from its parameters using colons (:)"""
    parsed = data.split(sep=":")
    return parsed


def listen(adcs: ADCSSubsystem, stop: threading.Event):
    """
    function that will continuously listen for server messages
    when a message is received it will be put onto the rx buffer 
    """
    while not stop_event.is_set():
        received = adcs.read_bytes()
        adcs.rx_buffer.put(received)


def handle(adcs: ADCSSubsystem, stop: threading.Event):
    """
    function that will continuously check the rx buffer for any
    data if there is it will take the data from the buffer and
    handle it putting any output onto the tx buffer for transmitting
    """
    received = adcs.rx_buffer.get()
    if not received:
        stop.set()  # begin closing client
        return

    decoded = received.decode("utf-8")
    data_list = command_parser(decoded)
    transmit = run_command(data_list)

    if transmit is not None:
        encoded = str(transmit).encode("utf-8")
        adcs_debug.tx_buffer.put(encoded)


def send(adcs: ADCSSubsystem, stop: threading.Event):
    """
    function that will continuously check the tx buffer for
    any data if there is it will send it back to the server.
    It is assumed that all data in the tx buffer are bytes object.
    """
    while not stop.is_set():
        transmitting = adcs.tx_buffer.get()
        adcs.send_bytes(transmitting)


def run_command(data):
    """
    Given a list of stings this will run an adcs command with
    some given arguments. Returns anything that the adcs command
    wishes to send back to the OBC
    """
    command = data[0]
    func = adcs_debug.commands[command]

    if len(data) == 1:  # No args
        return func()

    arg_list = data[1:]
    return func(arg_list)


# if __name__ == "__main__":
port, host = command_line_handler(sys.argv)
addr = (host, port)

print(f"Starting ADCS subsystem on port {port}")

connector = TCPClient(addr)
connector.set_debug(True)

adcs_debug = ADCSSubsystem(connector)
# adcs_debug.start()

# TODO: get threads to end when this is true
stop_event = threading.Event()  # used to stop child threads

rx_thread = threading.Thread(target=listen, args=(
    adcs_debug, stop_event), daemon=True)
tx_thread = threading.Thread(target=send, args=(
    adcs_debug, stop_event), daemon=True)

rx_thread.start()
tx_thread.start()

while not stop_event.is_set():  # Commands come in this format COMMAND:ARG1:ARG2:...:ARGN
    handle(adcs_debug, stop_event)

rx_thread.join()
tx_thread.join()
