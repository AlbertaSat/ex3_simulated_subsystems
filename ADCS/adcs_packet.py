from enum import Enum, auto

class PacketType(Enum):
    """Specifying the packet type"""
    DATA = auto()
    CONTROL = auto()


class AdcsPacket:
    """This is the class representing the packet that the ADCS will do transaction with"""

    def __init__(self):
        """TODO: Either make a class constructor or a factory object to create
        packets. This way, we ensure that only valid packets are created."""
        self.packet_type = None
        self.data = None

    def to_bytes(self) -> bytes:
        """This function returns the bytes representation of the current packet."""
        raise NotImplementedError

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


if __name__ == "__main__":
    unittest.main()
    
