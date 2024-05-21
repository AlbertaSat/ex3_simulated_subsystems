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


class MagneticCurrent(ThreeDimensionalMeasurements):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)


class WheelSpeed(ThreeDimensionalMeasurements):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)


class SystemClock:
    def __init__(self, time: float):
        self.time = time
