"""Test client that exercises the simulated S-Band I2C TCP interface.

Acts as a stand-in for the S-Band handler: connects to the simulated
subsystem, writes configuration registers, reads them back, and samples
dummy housekeeping / status registers.

Usage:
  Terminal 1: python3 sband_subsystem.py
  Terminal 2: python3 sband_test_client.py [host] [port]

Copyright (C) 2026 University of Alberta.
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

import socket
import sys

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 1812


def exchange(sock: socket.socket, command: str) -> str:
    """Send one command and return the response text."""
    sock.sendall((command + "\n").encode())
    data = sock.recv(4096)
    return data.decode(errors="replace").strip()


def run_handler_tests(host: str, port: int) -> int:
    """Run a scripted handler-style read/write sequence against the simulator."""
    print(f"Connecting to simulated S-Band at {host}:{port}")
    with socket.create_connection((host, port), timeout=5) as sock:
        checks = [
            ("ping", "OK:pong"),
            ("read:0x00", "OK:0x00:0x00"),
            ("write:0x00:0x01", "OK:0x00:0x01"),  # mode = Synchronization
            ("read:0x00", "OK:0x00:0x01"),
            # Encoder write should fail outside Configuration mode
            ("write:0x01:0x04", None),
            ("write:0x00:0x00", "OK:0x00:0x00"),  # back to Configuration
            ("write:0x01:0x04", "OK:0x01:0x04"),
            ("read:0x01", "OK:0x01:0x04"),
            ("write:0x03:0x02", "OK:0x03:0x02"),  # PA power code
            ("write:0x04:0x32", "OK:0x04:0x32"),  # frequency offset
            ("read:0x11", "OK:0x11:0x71"),  # firmware 7.1
            ("read:0x12", "OK:0x12:0x03"),  # status
            ("read:0x13", "OK:0x13:0x01"),  # tx ready
            ("reset", "OK:reset"),
            ("read:0x00", "OK:0x00:0x00"),
        ]

        failures = 0
        for command, expected in checks:
            response = exchange(sock, command)
            print(f"> {command}")
            print(f"< {response}")

            if expected is None:
                if not response.startswith("ERROR:"):
                    print(f"FAIL: expected ERROR for {command}, got {response}")
                    failures += 1
                continue

            if response != expected:
                print(f"FAIL: expected {expected}")
                failures += 1

        list_response = exchange(sock, "list")
        print("> list")
        print(f"< {list_response.splitlines()[0]} ...")
        if not list_response.startswith("OK:list"):
            print("FAIL: list did not return OK:list")
            failures += 1

        exchange(sock, "quit")

    if failures:
        print(f"S-Band handler simulation tests FAILED ({failures})")
        return 1

    print("S-Band handler simulation tests PASSED")
    return 0


def main() -> int:
    """CLI entry point."""
    host = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
    try:
        return run_handler_tests(host, port)
    except OSError as exc:
        print(f"Could not talk to simulated S-Band: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())


# pylint: disable=duplicate-code
# no error
__author__ = "AlbertaSat"
__copyright__ = """
    Copyright (C) 2026, University of Alberta.
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."""
