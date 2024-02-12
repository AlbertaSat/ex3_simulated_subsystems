
class InterfaceInterface:
    def connect(self):
        """
        This method will block until a connection
        has been made
        """
        raise NotImplementedError

    def send(self, data):
        """
        This method will send data
        """
        raise NotImplementedError

    def recv(self, data):
        """
        This method will recieve date
        """
        raise NotImplementedError
