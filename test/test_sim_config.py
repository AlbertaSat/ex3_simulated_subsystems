"""Tests for the config reader helper library"""

from __future__ import annotations

from configparser import ConfigParser

import definitions
from simconfig import get_simulated_config, make_fresh_config

TEST_PATH = definitions.PROJECT_ROOT / "test.ini"


def test_make_default_simconfig() -> None:
    """Tests if we could make a clean configuration file"""
    checks = tuple(x.name.lower() for x in definitions.Subsystems)
    make_fresh_config(TEST_PATH)
    read_config = ConfigParser()
    read_config.read(TEST_PATH)

    for index, subsystem in enumerate(checks):
        config_port = read_config[subsystem]["port"]
        # There is a hardcoded testing value for the port. At risk of change
        assert int(config_port) == 61200 + index, f"{subsystem}"

    TEST_PATH.unlink()


def test_obtain_default_ports() -> None:
    """Testing if we could read from the config file, and
    obtain the ports"""
    checks = tuple(x for x in definitions.Subsystems)
    make_fresh_config(TEST_PATH)
    read_config = ConfigParser()
    read_config.read(TEST_PATH)

    for index, subsystem in enumerate(checks):
        config_dict = get_simulated_config(TEST_PATH, subsystem)
        # There is a hardcoded testing value for the port. At risk of change
        assert (
            "port" in config_dict
        ), f"Missing port for {subsystem.name}, a required field"
        assert int(config_dict["port"]) == 61200 + index, f"{subsystem}"

    TEST_PATH.unlink()
