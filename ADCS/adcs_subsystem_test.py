"""The tutorial comments are done for people who have not taken the classes.

Feel free to remove all the tutorial stuff once the team is familiar with the concepts.
"""

import unittest
from unittest import TestCase
from unittest.mock import Mock
from adcs_subsystem import ADCSSubsystem


class TestAdcsSubsystem(TestCase):
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
        self.communication_interface = Mock()
        self.dut = ADCSSubsystem(self.communication_interface)
        return super().setUp()

    def tearDown(self) -> None:
        """
        Tutorial: This method will reset the class that was being tested"""
        self.communication_interface = None
        self.dut = None
        return super().tearDown()

    def test_setup(self):
        """This test just shows you how the testing infrastructures are working.

        NOTE: I read clean code. The author actually said that it is fine to put multiple asserts in a single test, as long as the asserts are testing the same thing.
        """
        self.assertNotEqual(None, self.dut)

        # Testing the testing helper methods
        if self.communication_interface != None:
            self.set_received(b"\xAB\xCD\x12\x34")
            self.assertEqual(b"\xAB\xCD\x12\x34", self.communication_interface.received)

            self.communication_interface.transmitted = b"0x4242ABAB"
            self.assertEqual(b"0x4242ABAB", self.get_transmitted())

    def test_invalid_state(self):
        """Testing how the simulated subsystem handles invalid state"""
        self.assertEqual(True, False)


if __name__ == "__main__":
    unittest.main()