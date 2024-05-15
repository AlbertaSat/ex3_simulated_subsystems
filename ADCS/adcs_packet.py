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
