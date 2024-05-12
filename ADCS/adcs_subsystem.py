# Python stdlib
import sys
from enum import Enum
from enum import auto

# Custom import
from abstract_interface import ConnectionProtocol
from tcp_server import TCPClient
from adcs_components import AngularMeasurement, AngularSpeed, MagneticMeasurements


class ADCSState(Enum):
    """
    Enum to represent the states of the ADCS
    """

    OFF = auto()
    WORKING = auto()


class ADCSSubsystem:
    """
    This class represents the simulated ADCS subsystem.
    """

    def __init__(self, connection_protocol: ConnectionProtocol):
        """
        Base constructor. Uses a dictionary with the default values.
        """
        empty_block = (0, 0, 0)
        self.angle = AngularMeasurement(*empty_block)
        self.angle_speed = AngularSpeed(*empty_block)
        self.magnetic_measurements = MagneticMeasurements(*empty_block)
        self.state = ADCSState.OFF

        self.connection = connection_protocol

    def start(self):
        """This method should start the simulation for the ADCS subsystem."""
        self.connection.send(b"Hi")
        buffer = self.connection.recv()

    def __repr__(self):
        return f"ADCSSubsystem(\n" + f"{self.__dict__!r}" f"\n)"


def command_line_handler(argv) -> tuple[int, str]:
    """
    Control flow for what to return depending on the commandline arg.

    **Change here if you need to change the port and address values**

    Returns:
        (PORT, HOST)
    """

    default_host = "127.0.0.1"
    default_port = 42123

    ret_port = int(argv[1]) if len(argv) > 1 else default_port
    ret_host = argv[2] if len(argv) > 2 else default_host

    return ret_port, ret_host


if __name__ == "__main__":
    port, host = command_line_handler(sys.argv)
    addr = (host, port)

    print(f"Starting ADCS subsystem on port {port}")

    connector = TCPClient(addr)
    connector.set_debug(True)

    adcs_debug = ADCSSubsystem(connector)

    adcs_debug.start()
