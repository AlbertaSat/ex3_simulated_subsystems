from enum import Enum, auto
from typing import Union


class PacketType(Enum):
    """Specifying the packet type"""

    DATA = auto()
    CONTROL = auto()


class AdcsPacket:
    """This is the class representing the packet that the ADCS will do transaction with"""

    @classmethod
    def from_bytes(cls, input_stream: bytes):
        """Constructs an ADCS packet from bytes"""
        ret = cls()
        ret.packet_type = cls.type_of_byte(input_stream[0].to_bytes(1, "little"))
        data_len = input_stream[1]
        ret.data = input_stream[2 : (2 + data_len)]
        return ret

    def __init__(self):
        """TODO: Either make a class constructor or a factory object to create
        packets. This way, we ensure that only valid packets are created."""
        self.packet_type: None | PacketType = None
        self.data: None | bytes = None

    def to_bytes(self) -> bytes:
        """This function returns the bytes representation of the current packet."""
        if self.packet_type is None or self.data is None:
            raise RuntimeError("The packet type cannot be None")
        byte_type = self.byte_of_type(self.packet_type)
        byte_length = self.data_length.to_bytes(1, "little", signed=False)

        return b"".join([byte_type, byte_length, self.data])

    @property
    def data_length(self) -> int:
        """Gets the length field of the packet"""
        return 0 if self.data is None else len(self.data)

    @staticmethod
    def byte_of_type(packet_type: PacketType) -> bytes:
        """Converts a packet type enum into the serial representation"""
        ret: bytes
        if packet_type is None:
            raise RuntimeError("packet_type cannot be None")
        match packet_type:
            case PacketType.DATA:
                ret = b"\x01"
            case PacketType.CONTROL:
                ret = b"\x02"
            case _:
                ret = b"\x00"
        return ret

    @staticmethod
    def type_of_byte(packet_byte: bytes) -> PacketType:
        """Converts serial data back into a python enum"""
        ret: PacketType
        if len(packet_byte) != 1:
            raise ValueError("type_of_byte", "Input not single byte")
        match packet_byte:
            case b"\x01":
                ret = PacketType.DATA
            case b"\x02":
                ret = PacketType.CONTROL
            case b"\x00":
                raise RuntimeError("The generating end found an unhandled PacketType")
            case _:
                raise RuntimeError("Like error during transmission")
        return ret

    def __eq__(self, value: object, /) -> bool:
        if type(value) is type(self):
            return value.packet_type == self.packet_type and value.data == self.data
        else:
            return False
