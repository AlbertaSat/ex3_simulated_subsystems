"""
Stores the enum states of the ADCS
"""

from enum import Enum
from enum import auto


class ADCSState(Enum):
    """
    Enum to represent the states of the ADCS
    """

    OFF = auto()
    WORKING = auto()
