import sys


class ThreeDimensionalMeasurements:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"({self.x!r}, {self.y!r}, {self.z!r})"


class AngularMeasurement(ThreeDimensionalMeasurements):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)


class AngularSpeed(ThreeDimensionalMeasurements):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)


class MagneticMeasurements(ThreeDimensionalMeasurements):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)


class ADCSSubsystem:
    """
    This class represents the simulated ADCS subsystem.
    """
    def __init__(self):
        """
        Base constructor. Uses a dictionary with the default values.
        """
        empty_block = (0, 0, 0)
        self.angle = AngularMeasurement(*empty_block)
        self.angle_speed = AngularSpeed(*empty_block)
        self.magnetic_measurements = MagneticMeasurements(*empty_block)

    def start(self):
        """This method should start the simulation for the ADCS subsystem.
        """
        raise NotImplementedError

    def send_data(self):
        """This method sends the data through the interface
        """
        raise NotImplementedError

    def __repr__(self):
        return (f"ADCSSubsystem(\n" +
                f"{self.__dict__!r}"
                f"\n)")


def command_line_handler(argv):
    """
    Control flow for what to return depending on the commandline arg.

    **Change here if you need to change the port and address values**

    Returns:
        (PORT, HOST)
    """
    simulated_subsystem = ADCSSubsystem()
    print(simulated_subsystem)

    default_host = "127.0.0.1"
    default_port = 1802

    return (argv[1] if len(argv) > 1 else default_port), default_host


if __name__ == "__main__":
    port, host = command_line_handler(sys.argv)

    print(f"Starting ADCS subsystem on port {port}")
