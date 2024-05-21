# Python stdlib
import sys

# Custom import
from abstract_interface import ConnectionProtocol
from tcp_server import TCPClient
from adcs_components import AngularMeasurement, AngularSpeed, MagneticMeasurements, WheelSpeed, SystemClock, MagneticCurrent
from adcs_states import ADCSState


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
        self.magnetic_current = MagneticCurrent(*empty_block)
        self.wheel_speed = WheelSpeed(*empty_block)
        self.system_clock = SystemClock(0)
        self.state = ADCSState.OFF

        self.rx_buffer = None
        self.tx_buffer = None

        self.connection = connection_protocol

        """  TODO: enumarate each function
        This dictionary will contain the "machine code" translations 
        for every possible command.
        """
        self.commands = {
            b"get_state": self.get_state,
            b"set": self.set_state,
            b"get_wheel_speed": self.get_wheel_speed,
            b"set_wheel_speed": self.set_wheel_speed
        }

    def __repr__(self):
        return f"ADCSSubsystem(\n" + f"{self.__dict__!r}" f"\n)"

    def start(self):
        """This method should start the simulation for the ADCS subsystem."""
        self.connection.send(b"Hi")
        buffer = self.connection.recv()

    def init_link(self):
        """This method should initiate the protocol connection between the OBC and the ADCS"""
        raise NotImplementedError

    def send_bytes(self, data: bytes) -> None:
        """This method sends bytes to the connected OBC"""
        self.connection.send(data)

    def read_bytes(self) -> bytes:
        """Wrapper function around the connection protocol"""
        return self.connection.recv()

    def set_state(self, state: ADCSState):
        """Set the state"""
        self.state = state

    def get_state(self):
        return self.state

    def set_wheel_speed(self, wheels: tuple[float, float, float]):
        """Sets the wheel speed in RPM"""
        self.wheel_speed.x = wheels[0]
        self.wheel_speed.y = wheels[1]
        self.wheel_speed.z = wheels[2]

    def get_wheel_speed(self) -> tuple[float, float, float]:
        """Gets the wheel speeds in RPM"""
        return (self.wheel_speed.x, self.wheel_speed.y, self.wheel_speed.z)

    def set_current(self, currents: tuple[float, float, float]):
        """Sets the magnetorquer currents in mA"""
        # TODO: Check if magnetorquer is measured in mA
        self.magnetic_current.x = currents[0]
        self.magnetic_current.y = currents[1]
        self.magnetic_current.z = currents[2]

    def get_current(self) -> tuple[float, float, float]:
        """Gets the magnetorquer currents in mA"""
        return (self.magnetic_current.x, self.magnetic_current.y, self.magnetic_current.z)

    def simulate_step(self, time_inc: float):
        """
        This method will simulate stepping 'time_inc' 
        seconds into the future.
        """
        raise NotImplementedError


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


def command_parser(data: bytes):
    """Splits the command from its parameters using colons (:)"""
    parsed = data.split(sep=b":")
    return parsed


if __name__ == "__main__":
    port, host = command_line_handler(sys.argv)
    addr = (host, port)

    print(f"Starting ADCS subsystem on port {port}")

    connector = TCPClient(addr)
    connector.set_debug(True)

    adcs_debug = ADCSSubsystem(connector)

    adcs_debug.start()

    while True:
        data = adcs_debug.connection.recv()
        if not data:
            break
        data = command_parser(data)
        if len(data == 1):  # No params
            print(adcs_debug.commands[data[0]]())
        else:
            adcs_debug.commands[data[0]](*data[1:])
