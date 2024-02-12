import socket
from abstract_interface import InterfaceInterface

class TcpListener(InterfaceInterface):
    def __init__(self, port:int, host:str):
        """
        
        """
        self.listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_sock.bind((host, port))

        # For book keeping
        self.host = host
        self.port = port

        self.connection_socket = None
        self.client_addr = None

    def connect(self):
        """
        Abstract method implementation to establish a connection
        Make the server start to listen
        """
        self.listening_sock.listen()
        self.connection_socket, self.client_addr = self.listening_sock.accept();

    def __repr__(self):
        return f"TcpListener(addr: {self.host!r}, port: {self.port!r})"
        

    def __del__(self):
        """
        TcpListener destructor. When no longer used, we should free up resources.
        """
        self.listening_sock.close()
