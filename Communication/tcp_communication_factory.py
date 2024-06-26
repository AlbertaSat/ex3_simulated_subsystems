# tcp_communication_factory.py

from .communication_factory import CommunicationFactory
from .tcp_communication import TCPCommunication

class TCPCommunicationFactory(CommunicationFactory):
    def create_communication(self, host, port) -> TCPCommunication:
        return TCPCommunication(host, port)
