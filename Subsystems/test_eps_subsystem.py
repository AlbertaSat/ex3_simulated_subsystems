# test_eps_subsystem.py

import multiprocessing
import time
import pytest
from Communication.communication_factory import CommunicationFactory
from Communication.tcp_communication_factory import TCPCommunicationFactory
from Subsystems.eps_subsystem import EPSSubsystem

def start_eps_subsystem_process(tcp_params):
    communication_factory = TCPCommunicationFactory()
    eps_process = multiprocessing.Process(
        target=EPSProcess,
        args=(EPSSubsystem, communication_factory, tcp_params)
    )
    eps_process.start()
    time.sleep(1)  # Wait for the subsystem to start
    return eps_process

def stop_eps_subsystem_process(eps_process):
    eps_process.terminate()
    eps_process.join()

class EPSProcess:
    def __init__(self, subsystem_class, communication_factory_cls, communication_args):
        communication_factory = communication_factory_cls()
        self.subsystem: EPSSubsystem = subsystem_class(communication_factory, communication_args)
        self.subsystem.communication.start_listening()

    def run(self):
        while True:
            # Implement the main logic of the EPS subsystem
            pass

def test_eps_subsystem():
    # Communication parameters for the EPS subsystem
    tcp_params_eps = ("127.0.0.1", 1801)

    # Start the EPS subsystem process
    eps_process = start_eps_subsystem_process(tcp_params_eps)

    try:
        # Send a test message to the EPS subsystem
        test_message = "update:Temperature:35.0"
        eps_process.subsystem.dispatch_message(test_message)

        # Optionally, add assertions or further testing logic here
        # For example, check if the EPS subsystem handles the message correctly

        # Wait for a moment (you might adjust the time based on your needs)
        time.sleep(2)

    finally:
        # Stop the EPS subsystem process
        stop_eps_subsystem_process(eps_process)

if __name__ == "__main__":
    pytest.main()

