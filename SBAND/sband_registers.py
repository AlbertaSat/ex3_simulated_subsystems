"""HSTXC S-Band transmitter register map and in-memory register bank.

Register addresses and access rules match AlbertaSat's S-Band equipment
handler (HSTXC-01-00090 / sTransmitter.h in ex2_sband_software):
I2C device address 0x26, 8-bit register accesses.

Copyright (C) 2026 University of Alberta.
Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

# I2C device address used by the flight S-Band handler.
SBAND_I2C_ADDRESS = 0x26

# Register Values (read-write)
S_CONTROL_REG = 0x00
S_ENCODER_REG = 0x01
S_PAPOWER_REG = 0x03
S_FREQ_REG = 0x04

# Register Values (write-only)
S_SOFTRST_REG = 0x05

# Register Values (read-only)
S_FWVER_REG = 0x11
S_STATUS_REG = 0x12
S_TXREADY_REG = 0x13
S_BUFUND_REG_1 = 0x14
S_BUFUND_REG_2 = 0x15
S_BUFOVR_REG_1 = 0x16
S_BUFOVR_REG_2 = 0x17
S_BUFCNT_REG_1 = 0x18
S_BUFCNT_REG_2 = 0x19
S_OUTPWR_REG_1 = 0x1A
S_OUTPWR_REG_2 = 0x1B
S_PATEMP_REG_1 = 0x1C
S_PATEMP_REG_2 = 0x1D
S_TOPTEMP_REG_1 = 0x1E
S_TOPTEMP_REG_2 = 0x1F
S_BOTTEMP_REG_1 = 0x20
S_BOTTEMP_REG_2 = 0x21
S_CURRENT_REG_1 = 0x22
S_CURRENT_REG_2 = 0x23
S_VOLTAGE_REG_1 = 0x24
S_VOLTAGE_REG_2 = 0x25
S_PACURRENT_REG_1 = 0x26
S_PACURRENT_REG_2 = 0x27
S_PAVOLTAGE_REG_1 = 0x28
S_PAVOLTAGE_REG_2 = 0x29

S_LAST_REG = S_PAVOLTAGE_REG_2

# Control / encoder bit helpers (mirrors sTransmitter.h)
S_CONTROL_MODE_BITMASK = 0b11
S_CONTROL_PA_BIT_INDEX = 7
S_CONF_MODE = 0

REGISTER_NAMES = {
    S_CONTROL_REG: "CONTROL",
    S_ENCODER_REG: "ENCODER",
    S_PAPOWER_REG: "PAPOWER",
    S_FREQ_REG: "FREQ",
    S_SOFTRST_REG: "SOFTRST",
    S_FWVER_REG: "FWVER",
    S_STATUS_REG: "STATUS",
    S_TXREADY_REG: "TXREADY",
    S_BUFUND_REG_1: "BUFUND_1",
    S_BUFUND_REG_2: "BUFUND_2",
    S_BUFOVR_REG_1: "BUFOVR_1",
    S_BUFOVR_REG_2: "BUFOVR_2",
    S_BUFCNT_REG_1: "BUFCNT_1",
    S_BUFCNT_REG_2: "BUFCNT_2",
    S_OUTPWR_REG_1: "OUTPWR_1",
    S_OUTPWR_REG_2: "OUTPWR_2",
    S_PATEMP_REG_1: "PATEMP_1",
    S_PATEMP_REG_2: "PATEMP_2",
    S_TOPTEMP_REG_1: "TOPTEMP_1",
    S_TOPTEMP_REG_2: "TOPTEMP_2",
    S_BOTTEMP_REG_1: "BOTTEMP_1",
    S_BOTTEMP_REG_2: "BOTTEMP_2",
    S_CURRENT_REG_1: "CURRENT_1",
    S_CURRENT_REG_2: "CURRENT_2",
    S_VOLTAGE_REG_1: "VOLTAGE_1",
    S_VOLTAGE_REG_2: "VOLTAGE_2",
    S_PACURRENT_REG_1: "PACURRENT_1",
    S_PACURRENT_REG_2: "PACURRENT_2",
    S_PAVOLTAGE_REG_1: "PAVOLTAGE_1",
    S_PAVOLTAGE_REG_2: "PAVOLTAGE_2",
}

READABLE_REGISTERS = frozenset(
    addr for addr in REGISTER_NAMES if addr != S_SOFTRST_REG
)
WRITABLE_REGISTERS = frozenset(
    {
        S_CONTROL_REG,
        S_ENCODER_REG,
        S_PAPOWER_REG,
        S_FREQ_REG,
        S_SOFTRST_REG,
    }
)


def default_register_values() -> dict[int, int]:
    """Return power-on / soft-reset dummy register values.

    Telemetry-style read-only registers are filled with fixed dummy data so
    a handler can exercise housekeeping reads without real RF hardware.
    """
    values = {addr: 0x00 for addr in REGISTER_NAMES}

    # Firmware 7.1 encoded as (major << 4) | minor
    values[S_FWVER_REG] = 0x71
    # PA power good + frequency lock
    values[S_STATUS_REG] = 0x03
    # Transmit ready (buffer not full)
    values[S_TXREADY_REG] = 0x01
    # Amateur-band mid frequency offset: (2425 - 2400) * 2 = 50
    values[S_FREQ_REG] = 0x32
    # Dummy scaled housekeeping raw bytes (not converted here)
    values[S_OUTPWR_REG_1] = 0x05
    values[S_OUTPWR_REG_2] = 0xA0
    values[S_PATEMP_REG_1] = 0x04
    values[S_PATEMP_REG_2] = 0x20
    values[S_TOPTEMP_REG_1] = 0x01
    values[S_TOPTEMP_REG_2] = 0x00
    values[S_BOTTEMP_REG_1] = 0x01
    values[S_BOTTEMP_REG_2] = 0x80
    values[S_CURRENT_REG_1] = 0x00
    values[S_CURRENT_REG_2] = 0x64
    values[S_VOLTAGE_REG_1] = 0x07
    values[S_VOLTAGE_REG_2] = 0x08
    values[S_PACURRENT_REG_1] = 0x00
    values[S_PACURRENT_REG_2] = 0x30
    values[S_PAVOLTAGE_REG_1] = 0x04
    values[S_PAVOLTAGE_REG_2] = 0xF0
    return values


class SBandRegisterBank:
    """In-memory S-Band I2C register bank with HSTXC access rules."""

    def __init__(self):
        """Initialize registers to default dummy values."""
        self._registers = default_register_values()

    def reset(self) -> None:
        """Restore all registers to power-on defaults (soft reset)."""
        self._registers = default_register_values()

    def read(self, address: int) -> int:
        """Read one 8-bit register, matching I2C read_reg behaviour.

        Args:
            address: Register address from the HSTXC map.

        Returns:
            int: Register value in range 0-255.

        Raises:
            KeyError: If the address is unknown or write-only.
        """
        if address not in READABLE_REGISTERS:
            raise KeyError(f"register 0x{address:02X} is not readable")
        return self._registers[address]

    def write(self, address: int, value: int) -> None:
        """Write one 8-bit register, matching I2C write_reg behaviour.

        Encoder writes are only accepted while CONTROL mode is Configuration,
        matching STX_setEncoder in the equipment handler. Writing SOFTRST
        triggers a full soft reset of the register bank.

        Args:
            address: Register address from the HSTXC map.
            value: Byte to store (masked to 8 bits).

        Raises:
            KeyError: If the address is not writable.
            ValueError: If encoder write is attempted outside config mode.
        """
        if address not in WRITABLE_REGISTERS:
            raise KeyError(f"register 0x{address:02X} is not writable")

        value &= 0xFF

        if address == S_SOFTRST_REG:
            self.reset()
            return

        if address == S_ENCODER_REG:
            mode = self._registers[S_CONTROL_REG] & S_CONTROL_MODE_BITMASK
            if mode != S_CONF_MODE:
                raise ValueError(
                    "ENCODER may only be written while CONTROL mode is Configuration"
                )

        self._registers[address] = value

    def dump(self) -> dict[int, int]:
        """Return a copy of all known register values."""
        return dict(self._registers)

    def name(self, address: int) -> str:
        """Return the symbolic name for a register address."""
        return REGISTER_NAMES.get(address, f"UNKNOWN_0x{address:02X}")


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
