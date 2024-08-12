"""
This program is a dummy subsystem used with the dummy subsystem handler for development of OBC FSW

It communicates with the dummy subsystem via TCP, by spawning a TCP server and listening for TCP \
client conn request from dummy handler.

Client commands:
- EXIT -> command to terminate its connection.
- QUIT -> command to terminate the server.
- GET_DUMMY_VAR -> command to get the value of DummyVar.
- SET_DUMMY_VAR:<VALUE> -> command to set the value of DummyVar to VALUE.

"""

import socket
import sys

DUMMY_SIM_PORT = 1899

DEFAULT_STATE_VALUES = {
    'DummyVar': 1,     # Dummy variable
}


class DummySubsystem:
    """
    Hold the state of the dummy subsystem

    """

    def __init__(self):
        # Load default state values
        self.state = {
            'DummyVar': DEFAULT_STATE_VALUES['DummyVar'],
        }
        self.updatable_parameters = ['']

    # pylint: disable=C0116
    def set_dummy_var(self, new_value):
        self.state['DummyVar'] = new_value

    # pylint: disable=C0116
    def get_dummy_var(self):
        return self.state['DummyVar']


def start_server(hostname, port):
    """
    Creates a server socket object with given port and name. client que is 5.

    Args:
        hostname(string): hostname for server
        port(int): port bound to server

    Returns:
        server_socket(socket): server socket object
    """

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((hostname, port))
    server_socket.listen(5)
    return server_socket


def handle_read_data(read_data):
    """
    Handles the data received from the client

    Args:
        data(byte): data received from client

    Returns:
        data(string): data received from client
    """

    decoded_data = read_data.decode().strip().split(':')
    command = decoded_data[0]
    print("Received command:", command)
    if command == "GET_DUMMY_VAR":
        print("Returning DummyVar:", Dummy.get_dummy_var())
        return str(Dummy.get_dummy_var())
    if command == "SET_DUMMY_VAR":
        Dummy.set_dummy_var(decoded_data[1])
        print("DummyVar set to:", decoded_data[1])
        return "OK"
    if command == "EXIT":
        return "EXIT"
    if command == "QUIT":
        return "QUIT"
    print("Invalid command read: " + command)
    return "ERR"


if __name__ == "__main__":
    Dummy = DummySubsystem()
    server = start_server('127.0.0.1', DUMMY_SIM_PORT)

    # Continuously listen for incomming data, and respond when request for dummy data is received
    while True:
        conn, addr = server.accept()
        with conn:
            print("Connected by", addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                RES = handle_read_data(data)
                if RES.strip() == "EXIT":
                    break
                if RES.strip() == "QUIT":
                    sys.exit()
                else:
                    RETURN_DATA = str(RES) + "\n"
                    conn.sendall(RETURN_DATA.encode())
