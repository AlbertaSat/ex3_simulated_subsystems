"""Holds the TcpListener class allowing the creation of TCP servers"""

import socket
from abstract_interface import ConnectionProtocol


class TcpListener(ConnectionProtocol):
    """
    The abstract implementation of a TCP server
    """

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
        """Turns on/off the debugging mode of the ADCS"""
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
        """Receives data from the client"""
        buffer_size = 256

        if timeout is None or timeout > 0:
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
