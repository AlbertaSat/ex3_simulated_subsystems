# Python stdlib
import sys
from queue import SimpleQueue

# Custom import
from abstract_interface import ConnectionProtocol
from tcp_server import TCPClient
from adcs_components import (
    AngularMeasurement,
    AngularSpeed,
    MagneticMeasurements,
    WheelSpeed,
    SystemClock,
    MagneticCurrent,
)
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

        self.rx_buffer = SimpleQueue()
        self.tx_buffer = SimpleQueue()

        self.connection = connection_protocol

        """  TODO: enumarate each function
        This dictionary will contain the "machine code" translations 
        for every possible command.

        List of commands to be added:
        Detumble (skip for now)
        On/off
        X,y,z wheel speed
        Status check/Housekeeping
        X,y,z magnetorquer speed
        Onboard time
        Orientation
        reset
        """
        self.commands = {
            "HELP": self.help,
            "GS": self.get_state,
            "ON": self.turn_on,
            "OFF": self.turn_off,
            "GWS": self.get_wheel_speed,
            "SWS": self.set_wheel_speed,
            "SC": "Status Check",  # TODO: check ex2 documents and find temp, volt, amp ratings
            "GTM": self.get_time,
            "STM": self.set_time,
            "GOR": self.get_orientation,
            "RESET": self.reset
        }

    def __repr__(self):
        return f"ADCSSubsystem(\n" + f"{self.__dict__!r}" f"\n)"

    def start(self):
        """This method should start the simulation for the ADCS subsystem."""
        # Should confirm connection with a handshake
        self.connection.send(b"Hi")
        buffer = self.connection.recv()

        # Start the main loop

    def init_link(self):
        """This method should initiate the protocol connection between the OBC and the ADCS"""
        raise NotImplementedError

    def send_bytes(self, data: bytes) -> None:
        """This method sends bytes to the connected OBC"""
        self.connection.send(data)

    def read_bytes(self) -> bytes:
        """Wrapper function around the connection protocol"""
        return self.connection.recv()

    def turn_on(self):
        """Turns on the ADCS"""
        self.state = ADCSState.WORKING

    def turn_off(self):
        """Puts ADCS in standby"""
        self.state = ADCSState.OFF

    def get_state(self):
        """Returns the state of the ADCS"""
        if (self.state == ADCSState.OFF):
            return "OFF"
        else:  # (self.state == ADCSState.WORKING):
            return "WORKING"

    def get_time(self):
        return self.system_clock.time

    def set_time(self, time):  # TODO: because of how i implemented this "time" is wrapped in an array
        """Sets the clock time"""
        self.system_clock.time = time[0]

    def set_wheel_speed(self, wheels: tuple[str, str, str]):
        """Sets the wheel speed in RPM"""
        float_wheels = [float(x) for x in wheels]
        self.wheel_speed.x = float_wheels[0]
        self.wheel_speed.y = float_wheels[1]
        self.wheel_speed.z = float_wheels[2]

    def get_wheel_speed(self) -> tuple[float, float, float]:
        """Gets the wheel speeds in RPM"""
        return (self.wheel_speed.x, self.wheel_speed.y, self.wheel_speed.z)

    def set_current(self, currents: tuple[str, str, str]):
        """Sets the magnetorquer currents in mA"""
        # TODO: Check if magnetorquer is measured in mA
        float_currents = [float(x) for x in currents]
        self.magnetic_current.x = float_currents[0]
        self.magnetic_current.y = float_currents[1]
        self.magnetic_current.z = float_currents[2]

    def get_current(self) -> tuple[float, float, float]:
        """Gets the magnetorquer currents in mA"""
        return (
            self.magnetic_current.x,
            self.magnetic_current.y,
            self.magnetic_current.z,
        )

    def get_orientation(self):
        """Returns the current angle of the ADCS"""
        return (self.angle.x, self.angle.y, self.angle.z)

    def reset(self):
        """Resets the wheels and magnetorquer"""
        empty_block = (0, 0, 0)
        self.set_wheel_speed(empty_block)
        self.set_current(empty_block)

    def help(self):
        """TODO: finish help command"""
        return 'HELP": help,\n \
        GS | Get State (OFF or WORKING)\n \
        ON | Set state WORKING \
        OFF | Set state OFF \
        GWS | Get wheel speed (tuple) \
        SWS:x:y:z | set wheel speed \
        SC | Status Check (not implemented), \
        GTM | Get time (float) \
        STM:float | Set time \
        GOR | Get orientation (tuple) \
        RESET | Resets wheels and magnetorquer'

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


# TODO: Replace all things with rx (recv) buffers and tx (send) buffers
if __name__ == "__main__":
    port, host = command_line_handler(sys.argv)
    addr = (host, port)

    print(f"Starting ADCS subsystem on port {port}")

    connector = TCPClient(addr)
    connector.set_debug(True)

    adcs_debug = ADCSSubsystem(connector)

    adcs_debug.start()

    while True:  # Commands come in this format COMMAND:ARG1:ARG2:...:ARGN
        data = adcs_debug.connection.recv()
        if not data:
            break
        data = command_parser(data)
        if len(data) == 1:  # No params
            print(adcs_debug.commands[data[0]]())
        else:
            adcs_debug.commands[data[0]](data[1:])
