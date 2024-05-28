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
        self.packet_type: Union[None, PacketType] = None
        self.data: Union[None, bytes] = None

    def to_bytes(self) -> bytes:
        """This function returns the bytes representation of the current packet."""
        byte_type = self.byte_of_type(self.packet_type)
        byte_length = self.data_length.to_bytes(1, "little")
        byte_data = self.byte_of_data(self.data)

        return b"".join([byte_type, byte_length, byte_data])

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

    @staticmethod
    def byte_of_data(data: Union[str, None]) -> bytes:
        """Converts the data in form of string into byte using UTF-8 encoding.
        UTF-8 allows for language agnostic communications."""
        if data is None:
            raise ValueError("Data value cannot be none")
        return bytes(data, "utf-8")
