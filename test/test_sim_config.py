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


def test_root_defaults() -> None:
    config_path = definitions.PROJECT_ROOT / "simulated_config.ini"
    expected = {
        definitions.Subsystems.ADCS: 1803,
        definitions.Subsystems.UHF_TO_GS: 1235,
        definitions.Subsystems.UHF_TO_OBC: 1234,
        definitions.Subsystems.DFGM: 1802,
        definitions.Subsystems.IRIS: 1806,
        definitions.Subsystems.DUMMY: 1807,
    }

    for subsys, expected_port in expected.items():
        found_port = get_simulated_config(config_path, subsys)["port"]
        assert (
            found_port is not None
        ), "Expected port for {} to exist, but found None".format(subsys.name)
        assert (
            int(found_port) == expected_port
        ), "Expected to see {}, but got {}".format(expected_port, found_port)
