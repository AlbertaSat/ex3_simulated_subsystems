"""Holds the abstract class ConnectionProtocol"""


class ConnectionProtocol:
    """TODO: We should put the packet serialization and so on be the
    responsibility of the connection protocol, since it will be
    changing as we get further into the project."""

    def send(self, data: bytes):
        """
        This method will send data. Force the input to be bytes so that the
        caller must format the data to be bytes already.
        """
        raise NotImplementedError

    def recv(self, timeout: float) -> bytes:
        """
        This method will recieve data. It should return it.
        timeout specifies in seconds how long the recv function
        should block before raising an exception

        Fundamental assumption is that this will work with bytes
        """
        raise NotImplementedError

    def connect(self):
        """
        This method will start the connection
        """
        raise NotImplementedError
