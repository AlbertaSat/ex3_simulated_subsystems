import socket
from typing import Optional
from abstract_interface import ConnectionProtocol


class TcpListener(ConnectionProtocol):
    def __init__(self, port: int, host: str):
        """ """
        self.listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_sock.bind((host, port))

        # For book keeping
        self.host = host
        self.port = port

        self.connection_socket = None
        self.client_addr = None

        self.debug = False

    def set_debug(self, mode: bool):
        self.debug = mode

    def connect(self):
        """
        Abstract method implementation to establish a connection
        Make the server start to listen
        """
        self.listening_sock.listen()
        self.connection_socket, self.client_addr = self.listening_sock.accept()

    def send(self, data):
        """"Sends data from the host"""
        self.connection_socket.sendall(data)
        if self.debug:
            print(f"SENT {data}")

    def recv(self, timeout: float) -> bytes:
        """Recieves data from the client"""
        buffer_size = 256
        if (timeout > 0):
            self.connection_socket.settimeout(timeout)
        buffer = self.connection_socket.recv(buffer_size)
        self.connection_socket.settimeout(None)
        if self.debug:
            print(f"RECV f{buffer}")
        return buffer

    def __repr__(self):
        return f"TcpListener({self.__dict__!r})"

    def __del__(self):
        """
        TcpListener destructor. When no longer used, we should free up resources.
        """
        self.listening_sock.close()


class TCPClient(ConnectionProtocol):
    def __init__(self, addr):
        self.addr = addr
        self.debug = False
        self.socket = socket.create_connection(self.addr)

    def set_debug(self, mode: bool):
        self.debug = mode

    def send(self, data):
        """Please give input in the form of a list of bytes"""
        self.socket.sendall(data)
        if self.debug:
            print(f"Sent: {data}")

    def recv(self):
        """Received from the connection and returns the data"""
        buffer = self.socket.recv(4096)
        if self.debug:
            print(f"Received: {buffer}")
        return buffer
