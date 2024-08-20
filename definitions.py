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
    DFGM = auto()
    DUMMY = auto()
    EPS = auto()
    IRIS = auto()
    UHF_TO_GS = auto()
    UHF_TO_OBC = auto()
