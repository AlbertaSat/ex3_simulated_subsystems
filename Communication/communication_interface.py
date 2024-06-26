"""
Abstract class for communication interface between a subsystem and the OBC.

This class is meant to be subclassed by a concrete classses implmenting TCP, I2C, SPI, etc.

Copyright 2024 [Devin Headrick]. Licensed under the Apache License, Version 2.0
"""

# ABC allows the use of abstract methods
from abc import ABC, abstractmethod

class CommunicationInterface(ABC):
    @abstractmethod
    def send_message(self, message):
        pass

    @abstractmethod
    def receive_message(self):
        pass
