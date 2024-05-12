class ConnectionProtocol:
    def send(self, data):
        """
        This method will send data
        """
        raise NotImplementedError

    def recv(self):
        """
        This method will recieve data. It should return it.
        """
        raise NotImplementedError
