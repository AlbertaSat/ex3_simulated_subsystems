import time
import logging

from Communication.communication_factory import CommunicationFactory
from Subsystems.eps_subsystem import EPSSubsystem
from Communication.tcp_communication_factory import TCPCommunicationFactory

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    tcp_params_eps = ("127.0.0.1", 1801)

    logger.info("Starting EPS Subsystem..")
    communication_factory = TCPCommunicationFactory()
    eps_subsystem = EPSSubsystem(communication_factory, tcp_params_eps)

    eps_subsystem.communication.start_listening()

    while True:
        # TODO: Implement main logic for the subsystem process
        # For example, check for specific conditions, process messages, etc.
        message = eps_subsystem.communication.receive_message()
        if message:
            eps_subsystem.handle_message(message)

        # if the subsystem is connected to a tcp client, send a  message
        if eps_subsystem.communication.connected_client is not None:
            eps_subsystem.dispatch_message("Response from EPS Subsystem")
            time.sleep(2)
    

        # # Simulate some processing time
        time.sleep(1)

if __name__ == "__main__":
    main()
