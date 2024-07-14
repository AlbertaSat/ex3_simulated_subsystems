"""This file contains definitions that will be used throughout the entire
project
"""

from __future__ import annotations

from pathlib import Path
from enum import Enum, auto

PROJECT_ROOT = Path(__file__).parent


class Subsystems(Enum):
    """enum of the simulated subsystems."""

    ADCS = auto()
    EPS = auto()
    IRIS = auto()
    UHF = auto()
