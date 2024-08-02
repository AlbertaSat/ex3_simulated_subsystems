""" This program is a dummy subsystem used with the dummy subsystem handler for development of OBC FSW 

It communicates with the dummy subsystem via TCP, by spawning a TCP server and listening for TCP client conn request from dummy handler.

"""

import socket
import time

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

    def set_dummy_var(self, new_value):
        self.state['DummyVar'] = new_value

    def get_dummy_var(self):
        return self.state['DummyVar']


def start_server(hostname, port):
    """
    Creates a server socket object with given port and name. client que is 5.

    Args:
        hostname(string): hostname for server
        port(int): port bound to server

    Returns:
        server(socket): server socket object
    """

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((hostname, port))
    server.listen(5)
    return server


def handle_read_data(read_data):
    """
    Handles the data received from the client

    Args:
        data(byte): data received from client

    Returns:
        data(string): data received from client
    """

    data = read_data.decode().strip().split(':')
    command = data[0]
    print("Received command:", command)
    if command == "GET_DUMMY_VAR":
        print("Returning DummyVar:", Dummy.get_dummy_var())
        return Dummy.get_dummy_var()
    elif command == "SET_DUMMY_VAR":
        Dummy.set_dummy_var(data[1])
        print("DummyVar set to:", data[1])
        return "OK"
    elif command == "EXIT":
        return "EXIT"
    elif command == "QUIT":
        return "QUIT"
    else:
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
                else:
                    res = handle_read_data(data)
                    if res.strip() == "EXIT":
                        break
                    elif res.strip() == "QUIT":
                        quit()
                    else:
                        RETURN_DATA = str(res) + "\n"
                        conn.sendall(RETURN_DATA.encode())
