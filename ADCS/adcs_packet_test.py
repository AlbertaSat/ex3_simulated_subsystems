import unittest
from unittest import TestCase
from adcs_packet import AdcsPacket, PacketType

class TestPacket(TestCase):
    def setUp(self):
        self.dut = AdcsPacket()
        return super().setUp()

    def tearDown(self):
        self.dut = None
        return super().tearDown()

    def test_testing_infrastructure(self):
        self.assertTrue(True)

    def test_byte_of_type(self):
        self.assertEqual(self.dut.byte_of_type(PacketType.DATA), b"\x01")
        self.assertEqual(self.dut.byte_of_type(PacketType.CONTROL), b"\x02")



if __name__ == "__main__":
    unittest.main()
