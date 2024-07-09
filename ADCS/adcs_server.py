"""
This will be the main file for the simulated ADCS subsystem.
"""

import sys
import threading
import time

from tcp_server import TcpListener
from adcs_subsystem import ADCSSubsystem

SLEEP_TIME = 5  # in seconds


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


def command_parser(data: str):
    """Splits the command from its parameters using colons (:)"""
    parsed = data.rstrip().split(sep=":")
    return parsed


def listen(adcs: ADCSSubsystem, stop: threading.Event):
    """
    function that will continuously listen for client messages
    when a message is received it will be put onto the rx buffer 
    """
    while not stop.is_set():
        try:
            received = adcs.read_bytes(timeout=SLEEP_TIME)
            if not received:
                stop.set()  # begin closing server
                time.sleep(SLEEP_TIME)
                return
            adcs.rx_buffer.put(received)
        except Exception:
            continue


def handle_input(adcs: ADCSSubsystem, stop: threading.Event):
    """
    function that will continuously check the rx buffer for any
    data if there is it will take the data from the buffer and
    handle it putting any output onto the tx buffer for transmitting
    """
    while not stop.is_set():
        try:
            received = adcs.rx_buffer.get(timeout=SLEEP_TIME)

            decoded = received.decode("utf-8")
            data_list = command_parser(decoded)

            handle_output_thread = threading.Thread(
                target=handle_output, args=(adcs, data_list), daemon=True)
            handle_output_thread.start()
        except Exception:
            continue


def handle_output(adcs: ADCSSubsystem, data_list: list):
    """
    function that will only run when a function thread is spawned.
    Once spawned, it will run its command and push to tx_buffer.
    This prevents tasks with short run times from being blocked by
    longer tasks
    """
    transmit = run_command(data_list, adcs)

    if transmit is not None:
        encoded = str(transmit).encode("utf-8")
        adcs.tx_buffer.put(encoded)


def send(adcs: ADCSSubsystem, stop: threading.Event):
    """
    function that will continuously check the tx buffer for
    any data if there is it will send it back to the server.
    It is assumed that all data in the tx buffer are bytes object.
    """
    while not stop.is_set():
        try:
            transmitting = adcs.tx_buffer.get(timeout=SLEEP_TIME)
            adcs.send_bytes(transmitting)
        except Exception:
            continue


def run_command(data, adcs):
    """
    Given a list of stings this will run an adcs command with
    some given arguments. Returns anything that the adcs command
    wishes to send back to the OBC
    """
    command = data[0]
    try:
        func = adcs.commands[command]
        if len(data) == 1:  # No args
            return func()
        arg_list = data[1:]
        return func(*arg_list)
    except KeyError:
        return "INVALID COMMAND: run \"HELP\" for list of commands\n"


if __name__ == "__main__":
    port, host = command_line_handler(sys.argv)
    addr = (host, port)

    print(f"Starting ADCS subsystem on port {port}")

    server = TcpListener(port, host)
    server.set_debug(True)

    server.connect()

    adcs_debug = ADCSSubsystem(server)

    stop_event = threading.Event()  # used to stop child threads

    rx_thread = threading.Thread(target=listen, args=(
        adcs_debug, stop_event), daemon=True)
    tx_thread = threading.Thread(target=send, args=(
        adcs_debug, stop_event), daemon=True)
    handle_input_thread = threading.Thread(target=handle_input, args=(
        adcs_debug, stop_event), daemon=True)

    rx_thread.start()
    tx_thread.start()
    handle_input_thread.start()

    while not stop_event.is_set():
        try:
            time.sleep(SLEEP_TIME)
        except KeyboardInterrupt:
            stop_event.set()
            time.sleep(SLEEP_TIME)

    rx_thread.join()
    tx_thread.join()
    handle_input_thread.join()
