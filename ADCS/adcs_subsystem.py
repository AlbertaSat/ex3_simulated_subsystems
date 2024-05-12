# Python stdlib
import sys
from enum import Enum
from enum import auto

# Custom import
from abstract_interface import InterfaceInterface
from tcp_server import TcpListener


class ADCSState(Enum):
    """
    Enum to represent the states of the ADCS
    """

    OFF = auto()
    WORKING = auto()


class ThreeDimensionalMeasurements:
    """
    Abstract class that deals with having multiple three
    dimensional stored values
    """

    @staticmethod
    def new():
        """Factory method test"""
        return ThreeDimensionalMeasurements(0, 0, 0)

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        """This function is for debugging by printing the object"""
        return f"({self.x!r}, {self.y!r}, {self.z!r})"


class AngularMeasurement(ThreeDimensionalMeasurements):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z)


class AngularSpeed(ThreeDimensionalMeasurements):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z)


class MagneticMeasurements(ThreeDimensionalMeasurements):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)


class ADCSSubsystem:
    """
    This class represents the simulated ADCS subsystem.
    """

    def __init__(self, interface: InterfaceInterface):
        """
        Base constructor. Uses a dictionary with the default values.
        """
        empty_block = (0, 0, 0)
        self.angle = AngularMeasurement(*empty_block)
        self.angle_speed = AngularSpeed(*empty_block)
        self.magnetic_measurements = MagneticMeasurements(*empty_block)
        self.interface = interface
        self.state = ADCSState.OFF

    def start(self):
        """This method should start the simulation for the ADCS subsystem."""
        print(f"Starting ADCS subsystem with interface: {self.interface!r}")
        self.interface.connect()

    def send_data(self):
        """This method sends the data through the interface"""
        raise NotImplementedError

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
    default_port = 1802

    ret_port = int(argv[1]) if len(argv) > 1 else default_port
    ret_host = argv[2] if len(argv) > 2 else default_host

    return ret_port, ret_host


if __name__ == "__main__":
    port, host = command_line_handler(sys.argv)

    simulated_subsystem = ADCSSubsystem(TcpListener(port, host))
    print(simulated_subsystem)

    simulated_subsystem.start()

    print(f"Starting ADCS subsystem on port {port}")
