"""This library provides the tools required to read configuration from the filesystem.
Using the INI format as it has broad compatabilities.
"""

from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path

from definitions import Subsystems


def get_simulated_config(
    config_file_path: Path, subsystem: Subsystems
) -> dict[str, str]:
    """This function will read the configuration
    file defined by config_file_path and obtain
    the configuration for the defined subsystem.
    """
    config = ConfigParser()
    config.read(config_file_path)

    subsystem_name = subsystem.name.lower()
    return dict(config[subsystem_name])


def make_fresh_config(file_path: Path) -> None:
    """This function creates a new subsystem_config.ini file, in the case that
    a reset must occur.

    Will create configuration for all the subsystems that are defined in the
    definitions.py file.
    """
    config = ConfigParser()
    for index, subsystem in enumerate(Subsystems):
        config[subsystem.name.lower()] = _make_default_subsystem_values(index)

    with open(file_path, "w", encoding="utf-8") as configfile:
        config.write(configfile)


def _make_default_subsystem_values(i: int) -> dict[str, str]:
    """This makes the default port for the simulated subsystem. Takes a port
    offset as parameter.

    NOTE:
    -   Left as a function for potential future extensions.
    -   The port is in the ephemeral range.
    """
    sim_port = 61200 + i

    return {"port": str(sim_port)}
