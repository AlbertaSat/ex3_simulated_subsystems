# Simulated S-Band Transceiver

TCP stand-in for the Ex-Alta 3 S-Band transmitter's I2C register interface ([issue #79](https://github.com/AlbertaSat/ex3_simulated_subsystems/issues/79)).

The flight handler configures the HSTXC over I2C (device address `0x26`) using the register map from [AlbertaSat/ex2_sband_software](https://github.com/AlbertaSat/ex2_sband_software) (`sTransmitter.h`, HSTXC-01-00090). This simulator exposes that same register bank over TCP so the handler can read/write dummy data without hardware.

RF transmit and SPI buffer fill are **out of scope** for now (per the issue).

---

## Quick start

```bash
# Terminal 1 — simulated I2C device
python3 SBAND/sband_subsystem.py          # default 127.0.0.1:1812
# or: python3 sband_subsystem.py 1812     # from inside SBAND/

# Terminal 2 — handler-style scripted test
python3 SBAND/sband_test_client.py

# Or interact with netcat
nc 127.0.0.1 1812
```

---

## TCP protocol (I2C analogue)

Commands are newline-terminated. Addresses/values accept decimal or `0x` hex.

| Command | I2C analogue | Response |
|---------|--------------|----------|
| `read:<addr>` | `read_reg(addr)` → send `[addr]`, recv `[val]` | `OK:0xAA:0xVV` |
| `write:<addr>:<value>` | `write_reg(addr, val)` → send `[addr, val]` | `OK:0xAA:0xVV` |
| `reset` | write soft-reset register `0x05` | `OK:reset` |
| `list` | dump readable registers | `OK:list` + lines |
| `ping` / `help` / `quit` | — | status / usage / close |

Access rules mirrored from the equipment handler:

- Only control/encoder/PA power/frequency/soft-reset are writable
- Soft-reset (`write:0x05:...` or `reset`) restores defaults
- Encoder (`0x01`) may only be written while CONTROL mode is Configuration (`0x00` bits `[1:0] == 00`)

---

## Register map (HSTXC)

| Addr | Name | Access | Notes |
|------|------|--------|-------|
| `0x00` | CONTROL | R/W | mode `[1:0]`, PA enable bit 7 |
| `0x01` | ENCODER | R/W | rate/mod/filter/scrambler/bit order |
| `0x03` | PAPOWER | R/W | 0–3 → 24/26/28/30 dBm |
| `0x04` | FREQ | R/W | frequency offset byte |
| `0x05` | SOFTRST | W | any write triggers soft reset |
| `0x11` | FWVER | R | dummy `0x71` (7.1) |
| `0x12` | STATUS | R | PA good / lock bits |
| `0x13` | TXREADY | R | transmit ready |
| `0x14`–`0x19` | buffer | R | count / underrun / overrun |
| `0x1A`–`0x29` | housekeeping | R | power, temps, currents, voltages |

---

## Files

| File | Role |
|------|------|
| `sband_registers.py` | HSTXC register map + in-memory bank |
| `sband_subsystem.py` | TCP server (simulated I2C device) |
| `sband_test_client.py` | Scripted S-Band handler test client |
