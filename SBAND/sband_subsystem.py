"""TCP server simulating the S-Band transmitter I2C register interface.

The flight S-Band handler talks to the HSTXC over I2C (device 0x26) using:
  write_reg(addr, val) -> send [addr, val]
  read_reg(addr)       -> send [addr], receive [val]

This simulator exposes the same register bank over TCP so a handler client
can configure and read dummy register data without hardware. RF transmit /
SPI buffer fill is intentionally out of scope for now (see issue #79).

Protocol (newline-terminated, colon-delimited):
  read:<addr>           -> OK:<addr>:<value>   or ERROR:...
  write:<addr>:<value>  -> OK:<addr>:<value>   or ERROR:...
  reset                 -> OK:reset
  list                  -> multi-line OK dump of readable registers
  ping                  -> OK:pong
  help                  -> OK:command list
  quit / exit           -> closes the client connection

Addresses and values accept decimal or 0x-prefixed hex.

Copyright (C) 2026 University of Alberta.
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

import socket
import sys

from sband_registers import SBAND_I2C_ADDRESS, SBandRegisterBank

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 1812
COMMAND_DELIMITER = ":"

SUPPORTED_COMMANDS = (
    "read",
    "write",
    "reset",
    "list",
    "ping",
    "help",
    "quit",
    "exit",
)


def parse_byte(token: str) -> int:
    """Parse a decimal or hex byte token into an int 0-255."""
    value = int(token, 0)
    if value < 0 or value > 0xFF:
        raise ValueError(f"byte out of range: {token}")
    return value


class SBandSubsystem:
    """Simulated S-Band I2C register device served over TCP."""

    def __init__(self):
        """Create the subsystem with a fresh register bank."""
        self.registers = SBandRegisterBank()
        self._handlers = {
            "quit": self._cmd_quit,
            "exit": self._cmd_quit,
            "ping": self._cmd_ping,
            "help": self._cmd_help,
            "reset": self._cmd_reset,
            "list": self._cmd_list,
            "read": self._cmd_read,
            "write": self._cmd_write,
        }

    def reset_registers(self) -> None:
        """Public helper to restore default dummy register values."""
        self.registers.reset()

    def handle_command(self, command: str) -> str:
        """Parse and execute one newline-stripped command string.

        Args:
            command: Raw command from the S-Band handler TCP client.

        Returns:
            str: Response body; the server appends ``\\n`` when sending.
        """
        parts = command.strip().split(COMMAND_DELIMITER)
        if not parts or not parts[0]:
            return "ERROR: empty command"

        handler = self._handlers.get(parts[0].lower())
        if handler is None:
            return "ERROR: unknown command (try help)"
        return handler(parts)

    @staticmethod
    def _cmd_quit(_parts):
        return "OK:bye"

    @staticmethod
    def _cmd_ping(_parts):
        return "OK:pong"

    @staticmethod
    def _cmd_help(_parts):
        return (
            "OK:commands "
            + ",".join(SUPPORTED_COMMANDS)
            + f" i2c_addr=0x{SBAND_I2C_ADDRESS:02X}"
        )

    def _cmd_reset(self, _parts):
        self.reset_registers()
        return "OK:reset"

    def _cmd_list(self, _parts):
        lines = ["OK:list"]
        for addr, value in sorted(self.registers.dump().items()):
            name = self.registers.name(addr)
            lines.append(f"0x{addr:02X}:{name}:0x{value:02X}")
        return "\n".join(lines)

    def _cmd_read(self, parts):
        if len(parts) != 2:
            return "ERROR: usage read:<addr>"
        try:
            addr = parse_byte(parts[1])
            value = self.registers.read(addr)
        except (ValueError, KeyError) as exc:
            return f"ERROR: {exc}"
        return f"OK:0x{addr:02X}:0x{value:02X}"

    def _cmd_write(self, parts):
        if len(parts) != 3:
            return "ERROR: usage write:<addr>:<value>"
        try:
            addr = parse_byte(parts[1])
            value = parse_byte(parts[2])
            self.registers.write(addr, value)
            return f"OK:0x{addr:02X}:0x{value:02X}"
        except (ValueError, KeyError) as exc:
            return f"ERROR: {exc}"


def serve(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    """Bind a TCP server and serve S-Band I2C register commands."""
    subsystem = SBandSubsystem()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()
        print(
            f"S-Band simulated I2C interface listening on {host}:{port} "
            f"(device 0x{SBAND_I2C_ADDRESS:02X})",
            flush=True,
        )

        while True:
            try:
                conn, addr = server_socket.accept()
            except KeyboardInterrupt:
                print("Keyboard interrupt. Closing S-Band server.", flush=True)
                break

            with conn:
                print(f"S-Band handler connected: {addr}", flush=True)
                while True:
                    try:
                        data = conn.recv(1024)
                    except ConnectionResetError:
                        print("Client reset connection.", flush=True)
                        break

                    if not data:
                        print("S-Band handler disconnected.", flush=True)
                        break

                    command = data.decode(errors="replace").strip()
                    if not command:
                        continue

                    print(f"RAW command: {command}", flush=True)
                    response = subsystem.handle_command(command)
                    conn.sendall((response + "\n").encode())

                    if command.lower() in ("quit", "exit"):
                        break


def main() -> int:
    """CLI entry point."""
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    try:
        serve(DEFAULT_HOST, port)
    except OSError as exc:
        print(f"Failed to start S-Band server: {exc}", flush=True)
        return 1
    return 0


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
