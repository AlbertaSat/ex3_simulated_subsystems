"""
Holds the ADCSSubsystem class
"""

# Python stdlib
from queue import SimpleQueue
import random

# Custom import
from abstract_interface import ConnectionProtocol
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

        self.rx_buffer = SimpleQueue()
        self.tx_buffer = SimpleQueue()

        self.connection = connection_protocol

        # For full list of commands go here:
        # https://docs.google.com/spreadsheets/d/1rWde3jjrgyzO2fsg2rrVAKxkPa2hy-DDaqlfQTDaNxg/edit?gid=0#gid=0
        self.commands = {
            "HELP": self.help,
            "GS": self.get_state,
            "ON": self.turn_on,
            "OFF": self.turn_off,
            "GWS": self.get_wheel_speed,
            "SWS": self.set_wheel_speed,
            "SC": self.status_check,
            "SMC": self.set_magnetorquer_current,
            "GMC": self.get_magnetorquer_current,
            "GTM": self.get_time,
            "STM": self.set_time,
            "GOR": self.get_orientation,
            "RESET": self.reset
        }

    def __repr__(self):
        return f"ADCSSubsystem(\n" + f"{self.__dict__!r}" f"\n)"

    def init_link(self):
        """This method should initiate the protocol connection between the OBC and the ADCS"""
        self.connection.connect()

    def send_bytes(self, data: bytes) -> None:
        """This method sends bytes to the connected OBC"""
        self.connection.send(data)

    def read_bytes(self, timeout: float = None) -> bytes:
        """This method reads bytes from the OBC"""
        return self.connection.recv(timeout)

    def turn_on(self):
        """Turns on the ADCS"""
        self.state = ADCSState.WORKING

    def turn_off(self):
        """Puts ADCS in standby"""
        self.state = ADCSState.OFF

    def status_check(self):
        """Generates random numbers for a status"""
        voltage = random.random() * 2 + 8
        current = random.random() * 5 + 10
        temp = random.random() * 10 + 30
        status = "OK" if random.random() >= 0.2 else "BAD"

        return f"Voltage: {voltage} V\nCurrent: {current} mA\
\nTemperature: {temp} C\nOverall Status: {status}\n"

    def get_state(self):
        """Returns the state of the ADCS"""
        return "OFF" if self.state == ADCSState.OFF else "WORKING"

    def get_time(self):
        """Gets the clock time"""
        return self.system_clock.time

    def set_time(self, time):
        """Sets the clock time"""
        self.system_clock.time = time

    def set_wheel_speed(self, wheels_x, wheels_y, wheels_z):
        """Sets the wheel speed in RPM"""
        self.wheel_speed.x = float(wheels_x)
        self.wheel_speed.y = float(wheels_y)
        self.wheel_speed.z = float(wheels_z)

    def get_wheel_speed(self) -> tuple[float, float, float]:
        """Gets the magnetorquer current in mA"""
        return (self.wheel_speed.x, self.wheel_speed.y, self.wheel_speed.z)

    def set_magnetorquer_current(self, current_x, current_y, current_z):
        """Sets the magnetorquer current in mA"""
        self.wheel_speed.x = float(current_x)
        self.wheel_speed.y = float(current_y)
        self.wheel_speed.z = float(current_z)

    def get_magnetorquer_current(self) -> tuple[float, float, float]:
        """Gets the wheel speeds in RPM"""
        return (self.wheel_speed.x, self.wheel_speed.y, self.wheel_speed.z)

    def set_current(self, currents_x, currents_y, currents_z):
        """Sets the magnetorquer currents in mA"""
        self.magnetic_current.x = float(currents_x)
        self.magnetic_current.y = float(currents_y)
        self.magnetic_current.z = float(currents_z)

    def get_current(self) -> tuple[float, float, float]:
        """Gets the magnetorquer currents in mA"""
        return (self.magnetic_current.x, self.magnetic_current.y, self.magnetic_current.z)

    def get_orientation(self):
        """Returns the current angle of the ADCS"""
        return (self.angle.x, self.angle.y, self.angle.z)

    def reset(self):
        """Resets the wheels and magnetorquer"""
        empty_block = (0, 0, 0)
        self.set_wheel_speed(*empty_block)
        self.set_current(*empty_block)

    def help(self):
        """Returns a string with commands"""
        return 'HELP | help (string)\n\
GS | Get State (OFF or WORKING)\n\
ON | Set state WORKING\n\
OFF | Set state OFF\n\
GWS | Get wheel speed (tuple)\n\
SWS:x:y:z | set wheel speed\n\
GMC | get magnetorquer current (tuple)\n\
SMC:x:y:z | set magnetorquer current\n\
SC | Status Check (string)\n\
GTM | Get time (float)\n\
STM:float | Set time\n\
GOR | Get orientation (tuple)\n\
RESET | Resets wheels and magnetorquer\n'
