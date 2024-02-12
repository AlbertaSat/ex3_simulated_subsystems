# eps_subsystem.py

import logging 

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from Communication.communication_factory import CommunicationFactory
from Communication.communication_interface import CommunicationInterface
from .subsystem import Subsystem

class EPSSubsystem(Subsystem):
    def __init__(self, communication_factory: CommunicationFactory, communication_args):
        communication: CommunicationInterface = communication_factory.create_communication(*communication_args)
        super().__init__(communication)

    def handle_message(self, message):
        try:
            logger.info(f"EPS rcvd message: {message}")
            # Implement the logic to handle the message according to your requirements
        except Exception as e:
            logger.error(f"EPS Error handling message: {e}")

        # # super.handle_message("Response from EPS Subsystem")
        pass

    def dispatch_message(self, response):
        # super.dispatch_message(response)
        # logger.info(f"EPS Subsystem dispatching message: {response}")
        self.communication.send_message("Response from EPS Subsystem")
        pass
