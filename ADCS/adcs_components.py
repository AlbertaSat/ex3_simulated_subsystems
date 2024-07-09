"""
Holds classes for each type of measurements on the ADCS
"""
# pylint: disable=too-few-public-methods
# pylint: disable=useless-parent-delegation


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
    """Stores the angle in 3D"""

    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z)


class AngularSpeed(ThreeDimensionalMeasurements):
    """Stores the angular speed in 3D"""

    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z)


class MagneticMeasurements(ThreeDimensionalMeasurements):
    """Stores the magnetic measurements in 3D"""

    def __init__(self, x, y, z):
        super().__init__(x, y, z)


class MagneticCurrent(ThreeDimensionalMeasurements):
    """Stores the current in 3D"""

    def __init__(self, x, y, z):
        super().__init__(x, y, z)


class WheelSpeed(ThreeDimensionalMeasurements):
    """Stores the wheels speeds in 3D"""

    def __init__(self, x, y, z):
        super().__init__(x, y, z)


class SystemClock:
    """Stores the time"""

    def __init__(self, time: float):
        self.time = time
