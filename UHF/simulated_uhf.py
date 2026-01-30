"""
Author: Drake Boulianne

This program simulates a UHF Transceiver radio intended to be used in testing ex3_software.

Generally two different kind of usage for our purposes:
1. When testing on fully simulated (no hardware needed besides your computer)

    When launching the simulated_uhf.py file with python there is no need to provide additional
    command line arguments to specify the IP addresses for the simulated UHF servers to bind to.
    This is because the default IP address is "127.0.0.1".

    Note that this is also the case for integration testing in github actions or locally

2. When testing on a partially simulated setup using a SBC and a ground station computer

    Typically in this scenario the simulated UHF is run on the ground station computer.
    But since the TCP client in the flight software (typically run on the SBC) needs to
    connect to a TCP server on the ground station device we need to expose the UART server address
    so it can be found by the SBC. This can be done by specifying addional command line arguments
    when launching the simulated_uhf.py program.

    First you need the IP address of your ground station computer:

        'ip a'

    Search for your IPV4 address of the interface you want the SBC to connect to 
    (this is normally typically an ethernet interface).

    If you have a firewall you may receive "No route to host" errors when trying to connect
    to the UART server. Consult your firewall program on how to expose a port, since you will
    need to expose the port for the simulated UHF UART server for the FSW to connect to.

    Finally you can specify the IPV4 address for the UHF UART server to bind to using the following command:
        `python3 simulated_uhf.py --uart-ip <ground station IPV4 addr>`

"""

import socket
import threading
import queue
import time
import argparse

UART_PORT = 1805
RADIO_PORT = 1808
BEACON_PORT = 1809

UART_IPADDR = "127.0.0.1"
RADIO_IPADDR = "127.0.0.1"
BEACON_IPADDR = "127.0.0.1"

BEACON_TX_PERIOD = 30
BEACON_CALL_SIGN = "VE6 LRN"
BEACON_TX_CONTENTS = "beacon"
BEACON_TX_MESSAGE = f"{BEACON_CALL_SIGN}{BEACON_TX_CONTENTS}"

RELAY_SERVER_RECV_SIZE = 128

class RelayServer(threading.Thread):
    """
    Server daemon bound to a given port, and IP address.

    Two queues are given to the server, an inbound and outbound queue.
    
    Any data sent by a client connected to the Relay server will be added to the outbound buffer.
    The inbound buffer is periodically polled to for data, if data is in the queue it will be sent
    to the client connected to the relay server without any processing.

    The daemon is setup to only allow for a single client to be connected at a time.
    If a client disconnects, it can reconnect as well without the need to restart the
    Relay Server.
    """

    def __init__(self, name, ipaddr, port, outbound_buffer, inbound_buffer):
        """ Creates a Relay Server"""
        super().__init__(daemon=True)
        self.name = name
        self.ipaddr = ipaddr
        self.port = port
        self.outbound_buffer = outbound_buffer
        self.inbound_buffer = inbound_buffer

    def run(self):
        """
        Binds the Relay Server it to the IP address and port given in the class constructor.

        Connects to at most one client and handles it.

        Supports re-connection without restarting server daemon.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind((self.ipaddr, self.port))
            srv.listen(1)

            while True:
                conn, addr = srv.accept()
                print(f"[{self.name}] client connected: {addr}")

                try:
                    self.handle_client(conn)
                except Exception as e:
                    print(f"[{self.name}] Failed to handle client{e.with_traceback}")
                    print(f"[{self.name}] error: {e}")
                finally:
                    conn.close()
                    print(f"[{self.name}] client disconnected")

    def handle_client(self, conn: socket.socket):
        """
        Constantly polls both the client for incoming data, as well as the inbound
        buffer for any data. If data is sent by the client to the Relay server, pushed into
        the outbound buffer. If any data is found in the inbound buffer, it is sent to the connected client.

        returns if the client has disconnected from the Relay Server.
        """
        conn.settimeout(0.1)

        while True:
            try:
                data = conn.recv(RELAY_SERVER_RECV_SIZE)
                if not data:
                    return
                print(f"[{self.name}] received: {data}")
                self.outbound_buffer.put(data)
            except socket.timeout:
                pass

            try:
                while True:
                    msg = self.inbound_buffer.get_nowait()
                    conn.sendall(msg)
                    print(f"[{self.name}] forwarded: {msg}")
            except queue.Empty:
                pass


class BeaconServer(threading.Thread):
    """
    A server that periodically transmits a predefined message to the connected client.

    The Beacon Server daemon does not listen for any data sent by the client.

    The Beacon Server supports reconnection if the connection is lost.
    """
    def __init__(self, name, ipaddr, port, message, interval=30):
        super().__init__(daemon=True)
        """
        Initialize a beacon server.

        Provide a port and ip address for port to bind to. 
        The given message will be transmitted to a connected
        client every 'interval' seconds (default 30s)
        """
        self.name = name
        self.ipaddr = ipaddr
        self.port = port
        self.message = message
        self.interval = interval

    def run(self):
        """
        Run the beacon server daemon.

        This will create a TCP socket and bind it to the BeaconServer's address and port.
        Only a single client can connect to the server at a time. BeaconServer allows for clients to 
        disconnect and reconnect without restarting the server.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind((self.ipaddr, self.port))
            srv.listen(1)

            while True:
                conn, addr = srv.accept()
                print(f"[{self.name}] client connected: {addr}")

                try:
                    self.handle_client(conn)
                except Exception as e:
                    print(f"[{self.name}] error: {e}")
                finally:
                    conn.close()
                    print(f"[{self.name}] client disconnected")

    def handle_client(self, conn: socket.socket):
        """
        Sends the connected client the given beacon message after every "interval" seconds.
        """
        conn.settimeout(1.0)

        while True:
            try:
                conn.sendall(self.message.encode('utf-8'))
                print(f"{self.name} transmit beacon")
                time.sleep(self.interval)
            except (BrokenPipeError, ConnectionResetError, OSError):
                print(f"{self.name}: client disconnected")
                return


def parse_args():
    """
    Parses command line arguments. Use '--help' flag for more information on usage and description.
    """

    parser = argparse.ArgumentParser(
        description="Simulate a UHF Transceiver Radio with TCP servers"
    )

    parser.add_argument(
        "--radio-ip",
        type=str,
        default=RADIO_IPADDR,
        help=f"Change the IP address the Radio Server binds to (default: {RADIO_IPADDR})"
    )

    parser.add_argument(
        "--uart-ip",
        type=str,
        default=UART_IPADDR,
        help=f"Change the IP address the Uart Server binds to (default: {UART_IPADDR})"
    )

    parser.add_argument(
        "--beacon-ip",
        type=str,
        default=BEACON_IPADDR,
        help=f"Change the IP address the Beacon Server binds to (default: {BEACON_IPADDR})"
    )

    args = parser.parse_args()
    return args

def main():
    """Starts the simulated UHF server daemons and waits forever"""
    args = parse_args()

    uart_buffer = queue.Queue()
    radio_buffer = queue.Queue()

    uart_server = RelayServer("UHF Uart Server", args.uart_ip, UART_PORT, radio_buffer, uart_buffer)
    radio_server = RelayServer("UHF Radio Server", args.radio_ip, RADIO_PORT, uart_buffer, radio_buffer)
    beacon_server = BeaconServer("UHF Beacon Server", args.beacon_ip, BEACON_PORT, BEACON_TX_MESSAGE, BEACON_TX_PERIOD)

    beacon_server.start()
    radio_server.start()
    uart_server.start()

    print("Simulated UHF up. Ctrl+C to stop.")
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
