class ConnectionProtocol:
    def send(self, data: bytes):
        """
        This method will send data. Force the input to be bytes so that the
        caller must format the data to be bytes already.
        """
        raise NotImplementedError

    def recv(self) -> bytes:
        """
        This method will recieve data. It should return it.

        Fundamental assumption is that this will work with bytes
        """
        raise NotImplementedError
