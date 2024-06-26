# communication_factory.py

from abc import ABC, abstractmethod
from .communication_interface import CommunicationInterface

class CommunicationFactory(ABC):
    @abstractmethod
    def create_communication(self, *args, **kwargs) -> CommunicationInterface:
        pass
