"""The tutorial comments are done for people who have not taken the classes.

Feel free to remove all the tutorial stuff once the team is familiar with the concepts.
"""

import unittest
from adcs_subsystem import ADCSSubsystem
from abstract_interface import ConnectionProtocol


class MockConnection(ConnectionProtocol):
    """This class mocks a connection, but the input and the output can be
    controlled and monitored by the testing framework"""

    def __init__(self):
        """Init Mock object"""
        self.__received = bytes()
        self.__transmitted = bytes()

    def send(self, data: bytes):
        print(f"{data}")

    def recv(self) -> bytes:
        return self.received

    @property
    def received(self) -> bytes:
        """This is the getter for the received property"""
        return self.__received

    @received.setter
    def received(self, received: bytes):
        """This is the setter. Will be used for unit testing

        Enforcing this type to be bytes (Not bytearray)
        """
        if isinstance(received, bytes):
            self.__received = received
        else:
            raise TypeError

    @property
    def transmitted(self) -> bytes:
        return self.__transmitted

    @transmitted.setter
    def transmitted(self, transmitted: bytes):
        self.__transmitted = transmitted


class TestAdcsSubsystem(unittest.TestCase):
    def set_received(self, rx: bytes) -> None:
        """Quick wrapper function to set the mock value"""
        if self.communication_interface != None:
            self.communication_interface.received = rx

    def get_transmitted(self) -> bytes | None:
        """Quick wrapper function to get the value of the received"""
        if self.communication_interface != None:
            return self.communication_interface.transmitted
        else:
            return None

    def setUp(self) -> None:
        """
        Tutorial: This method is used to setup the testing class"""
        self.communication_interface = MockConnection()
        self.dut = ADCSSubsystem(self.communication_interface)
        return super().setUp()

    def tearDown(self) -> None:
        """
        Tutorial: This method will reset the class that was being tested"""
        self.communication_interface = None
        self.dut = None
        return super().tearDown()

    def test_setup(self):
        """This test just shows you how the testing infrastructures are working."""
        self.assertNotEqual(None, self.dut)

        # Testing the testing helper methods
        if self.communication_interface != None:
            self.set_received(b"0xABCD1234")
            self.assertEqual(b"0xABCD1234", self.communication_interface.received)

            self.communication_interface.transmitted = b"0x4242ABAB"
            self.assertEqual(b"0x4242ABAB", self.get_transmitted())


if __name__ == "__main__":
    unittest.main()
