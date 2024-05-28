from enum import Enum, auto
from typing import Union


class PacketType(Enum):
    """Specifying the packet type"""

    DATA = auto()
    CONTROL = auto()


class AdcsPacket:
    """This is the class representing the packet that the ADCS will do transaction with"""

    @classmethod
    def from_bytes(cls):
        """Constructs an ADCS packet from bytes"""
        raise NotImplementedError

    def __init__(self):
        """TODO: Either make a class constructor or a factory object to create
        packets. This way, we ensure that only valid packets are created."""
        self.packet_type = None
        self.data: Union[None, bytes] = None

    def to_bytes(self) -> bytes:
        """This function returns the bytes representation of the current packet."""
        raise NotImplementedError

    @property
    def data_length(self) -> int:
        """Gets the length field of the packet"""
        return 0 if self.data is None else len(self.data)

    @staticmethod
    def byte_of_type(packet_type: PacketType) -> bytes:
        """Converts a packet type enum into the serial representation"""
        ret: bytes
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

    @staticmethod
    def byte_of_data(data: str) -> bytes:
        """Converts the data in form of string into byte using UTF-8 encoding.
        UTF-8 allows for language agnostic communications."""
        return bytes(data, "utf-8")
