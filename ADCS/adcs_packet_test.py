import unittest
from unittest import TestCase
from adcs_packet import AdcsPacket, PacketType


class TestPacket(TestCase):
    def setUp(self):
        self.dut = AdcsPacket()
        return super().setUp()

    def tearDown(self):
        del self.dut
        return super().tearDown()

    def test_byte_of_type(self):
        self.assertEqual(self.dut.byte_of_type(PacketType.DATA), b"\x01")
        self.assertEqual(self.dut.byte_of_type(PacketType.CONTROL), b"\x02")

    def test_type_of_byte(self):
        test_eq = lambda x, y: self.assertEqual(self.dut.type_of_byte(x), y)

        test_eq(b"\x01", PacketType.DATA)
        test_eq(b"\x02", PacketType.CONTROL)

        with self.assertRaises(RuntimeError):
            self.dut.type_of_byte(b"\x00")

        with self.assertRaises(RuntimeError):
            self.dut.type_of_byte(b"\x77")

        with self.assertRaises(ValueError):
            self.dut.type_of_byte(b"\xDE\xAD\xBE\xEF")

    def test_data_lenth(self):
        """Testing if we can get the length field from a packet object"""
        self.assertEqual(self.dut.data_length, 0)
        self.dut.data = b"\xDE\xAD\xBE\xEF"
        self.assertEqual(self.dut.data_length, 4)


if __name__ == "__main__":
    unittest.main()
