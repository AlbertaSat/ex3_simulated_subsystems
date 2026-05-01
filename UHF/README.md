# simulated_uhf.py

Simulates a UHF transceiver radio as a set of TCP servers for testing satellite flight software without physical hardware. An interactive fault injection CLI lets you corrupt, drop, delay, or duplicate packets on either side of the link at any time during a test.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Architecture](#architecture)
3. [Launch Options](#launch-options)
4. [Fault Injection CLI](#fault-injection-cli)
5. [Testing Scenarios](#testing-scenarios)

---

## Quick Start

**Fully simulated — single machine, no hardware:**
```bash
python3 simulated_uhf.py
```

**Partially simulated — SBC running FSW, ground station computer running this simulator:**
```bash
# Find the LAN IP of your ground station machine
ip a

# Expose the UART server on that interface so the SBC can reach it
python3 simulated_uhf.py --uart-ip <ground-station-IPv4>
```
> If you get "No route to host" errors, check that your firewall is allowing the UART port (1805).

Once running, the fault injection prompt appears immediately:
```
uhf-fault>
```

---

## Architecture

The simulator exposes three TCP servers. The ground station client connects to the Radio Server and the satellite/FSW client connects to the UART Server. Packets flow between the two through shared queues, with the fault injector sitting in the middle.

```
Ground Station Client               Satellite / FSW Client
        │                                     │
        │ TCP :1808                           │ TCP :1805
        ▼                                     ▼
 ┌──────────────┐    radio_buffer    ┌──────────────┐
 │ Radio Server │ ─────────────────► │  UART Server │
 │   (GS side)  │ ◄───────────────── │  (SAT side)  │
 └──────────────┘    uart_buffer     └──────────────┘
                            │
                     ┌──────┴──────┐
                     │ FaultState  │ ◄── CLI thread arms faults here
                     └─────────────┘

 Beacon Server (:1809) — independently transmits call sign every 30s
```

**Ports:**

| Port | Server | Who connects |
|------|--------|--------------|
| 1805 | UART Server | Satellite / FSW |
| 1808 | Radio Server | Ground station |
| 1809 | Beacon Server | Ground station |

---

## Launch Options

| Flag | Default | Description |
|------|---------|-------------|
| `--uart-ip <addr>` | `127.0.0.1` | IP the UART server binds to (satellite-facing) |
| `--radio-ip <addr>` | `127.0.0.1` | IP the Radio server binds to (GS-facing) |
| `--beacon-ip <addr>` | `127.0.0.1` | IP the Beacon server binds to |

---

## Fault Injection CLI

Faults are **armed in advance** — you set a counter and the fault fires automatically on the next qualifying packet. You don't need to time commands to coincide with traffic.

### Directions

Every command takes a direction that controls which side of the link is affected:

| Direction | Packets affected |
|-----------|-----------------|
| `gs` | Packets being delivered **to the ground station** |
| `sat` | Packets being delivered **to the satellite** |
| `both` | Both directions simultaneously |

---

### Commands

#### `corrupt <gs|sat|both> <n> <m>`
Flips `n` consecutive bits in the **next packet**, starting at bit offset `m`. Bit 0 is the MSB of the first byte.

```
uhf-fault> corrupt sat 4 0
  [CLI] Will corrupt 4 bits at bit offset 0 next packet -> ['sat']
```

#### `drop <gs|sat|both> <n>`
Silently discards the next `n` packets. The receiving side gets nothing — no error, no disconnection.

```
uhf-fault> drop gs 3
  [CLI] Will drop next 3 packet(s) -> ['gs']
```

#### `delay <gs|sat|both> <n> <ms>`
Holds each of the next `n` packets for `ms` milliseconds before forwarding.

```
uhf-fault> delay both 1 2000
  [CLI] Will delay next 1 packet(s) by 2000.0ms -> ['gs', 'sat']
```

#### `duplicate <gs|sat|both> <n>`
Sends the next packet `n` times (i.e. `n=2` means the packet arrives twice).

```
uhf-fault> duplicate sat 2
  [CLI] Will duplicate next packet 2 times -> ['sat']
```

#### `status`
Shows pending fault counters and how many times each fault has fired this session.

```
uhf-fault> status

  Pending faults:
    [gs ] corrupt=0 drop=3 delay=0@0.0ms duplicate=0
    [sat] corrupt=4 drop=0 delay=0@0.0ms duplicate=0

  Total fired:
    [gs ] corrupt=1 drop=5 delay=2 duplicate=0
    [sat] corrupt=3 drop=0 delay=0 duplicate=2
```

#### `clear`
Cancels all pending faults on both links immediately.

#### `help` / `quit` / `exit`
Print command reference or shut down the simulator.

---

## Testing Scenarios

### does the satellite retry after a dropped command?
```
uhf-fault> drop sat 1
```
Send a command from the GS. The satellite receives nothing. Observe whether the FSW retries or the GS times out and re-sends.

---

### does the FSW reject a corrupted packet?
```
uhf-fault> corrupt sat 8 0
```
Corrupts the first byte of the next command sent to the satellite. The FSW should detect a bad checksum and reject it rather than acting on garbage data.

To target a specific field in your packet structure, calculate the bit offset of that field and use it as `m`. For example, to corrupt 4 bits starting at byte 2:
```
uhf-fault> corrupt sat 4 16
```

---

### does the GS handle a slow telemetry response?
```
uhf-fault> delay gs 1 3000
```
If the GS expects a reply within 2 seconds, this will cause it to time out. Verify it fails gracefully rather than hanging.

---

### does the FSW handle a duplicate command safely?
```
uhf-fault> duplicate sat 2
```
The satellite receives the next command twice. Verify the FSW doesn't execute it twice (e.g. no double-fire of an actuator, no double-increment of a counter).

---

### simulate a link blackout and restoration:
```
uhf-fault> drop both 10
# ... traffic flows, both sides receive nothing ...
uhf-fault> clear
# link restored
```

---

### Chaining faults
Fault counters are independent, so you can arm multiple types at once:
```
uhf-fault> corrupt sat 1 0
uhf-fault> drop sat 1
```
The next packet toward the satellite will be corrupted; the one after that will be dropped.
