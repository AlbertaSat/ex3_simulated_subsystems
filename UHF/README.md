# simulated_uhf.py — Usage & Reference

Simulates a UHF transceiver radio as a set of TCP servers, allowing both sides of a satellite communications link (ground station and satellite/FSW) to be exercised without physical hardware. Includes an interactive fault-injection CLI for reliability and error-handling testing.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Architecture Overview](#architecture-overview)
3. [Launch Options](#launch-options)
4. [Fault Injection CLI](#fault-injection-cli)
   - [Directions](#directions)
   - [Commands](#commands)
   - [Examples](#examples)
5. [Fault Types Explained](#fault-types-explained)
6. [Testing Scenarios](#testing-scenarios)

---

## Quick Start

**Fully simulated (single machine):**
```bash
python3 simulated_uhf.py
```

**Partially simulated (SBC satellite + ground station computer):**
```bash
# On the ground station machine — expose the UART server on the LAN interface
python3 simulated_uhf.py --uart-ip 192.168.1.50
```

Once running, the fault injection prompt appears:
```
uhf-fault>
```

---

## Architecture Overview

The simulator runs three independent daemon threads and one interactive CLI thread:

```
Ground Station Client          Satellite / FSW Client
        │                               │
        │ TCP :1808                     │ TCP :1805
        ▼                               ▼
 ┌─────────────────┐           ┌─────────────────┐
 │  Radio Server   │           │   UART Server   │
 │  (GS side)      │           │   (SAT side)    │
 └────────┬────────┘           └────────┬────────┘
          │  radio_buffer →             │
          │        ← uart_buffer        │
          └──────────────┬──────────────┘
                         │
                  ┌──────┴──────┐
                  │  FaultState │  ← CLI thread arms faults here
                  └─────────────┘

 Beacon Server (:1809) — transmits call sign every 30s independently
```

**Data flow:** A packet sent by the GS client arrives at the Radio Server, is placed in `uart_buffer`, and is picked up by the UART Server to be forwarded to the satellite client — and vice versa. Every packet transiting this path passes through `FaultState.apply_faults()` before being sent, which is where injected faults fire.

**Ports:**

| Port | Server | Purpose |
|------|--------|---------|
| 1805 | UART Server | Satellite / FSW connection |
| 1808 | Radio Server | Ground station connection |
| 1809 | Beacon Server | Periodic beacon transmission |

---

## Launch Options

| Flag | Default | Description |
|------|---------|-------------|
| `--uart-ip <addr>` | `127.0.0.1` | IP the UART server binds to (satellite-facing) |
| `--radio-ip <addr>` | `127.0.0.1` | IP the Radio server binds to (GS-facing) |
| `--beacon-ip <addr>` | `127.0.0.1` | IP the Beacon server binds to |

For single-machine testing all defaults are fine. For SBC testing, set `--uart-ip` to the ground station's LAN IPv4 address so the SBC can reach the UART server across the network.

---

## Fault Injection CLI

After launch, the simulator prints the command reference and drops into the interactive prompt:

```
uhf-fault>
```

All faults are **armed in advance** — you set a counter, and the next N qualifying packets trigger the fault automatically. There is no need to time your keystrokes to coincide with traffic.

### Directions

Every command takes a `<direction>` argument that controls which link leg is affected:

| Direction | Meaning |
|-----------|---------|
| `gs` | Packets being delivered **to the ground station** (uplink replies, telemetry) |
| `sat` | Packets being delivered **to the satellite** (commands, uplink data) |
| `both` | Both legs simultaneously |

Think of it as "who will *receive* the corrupted or missing packet."

### Commands

#### `corrupt <direction> <n>`
Arms bit-flip corruption for the next `n` packets on the chosen link. Between 1 and 8 bits are flipped at random positions in each affected packet.

```
uhf-fault> corrupt sat 3
  [CLI] Will corrupt next 3 packet(s) -> ['sat']
```

#### `drop <direction> <n>`
Arms packet dropping for the next `n` packets. Dropped packets are silently discarded — the receiving side gets nothing, with no TCP error or disconnection.

```
uhf-fault> drop gs 1
  [CLI] Will drop next 1 packet(s) -> ['gs']
```

#### `delay <direction> <n> <ms>`
Arms an artificial delay for the next `n` packets. Each affected packet is held for `<ms>` milliseconds before forwarding. Useful for triggering timeout logic.

```
uhf-fault> delay both 2 500
  [CLI] Will delay next 2 packet(s) by 500.0ms -> ['gs', 'sat']
```

#### `duplicate <direction> <n>`
Arms duplication for the next `n` packets. Each affected packet is forwarded twice in immediate succession.

```
uhf-fault> duplicate sat 1
  [CLI] Will duplicate next 1 packet(s) -> ['sat']
```

#### `status`
Prints both the **pending** fault counters (faults still waiting to fire) and the **total fired** counts for the session.

```
uhf-fault> status

  Pending faults:
    [gs ] corrupt=0 drop=1 delay=0@0.0ms duplicate=0
    [sat] corrupt=3 drop=0 delay=0@0.0ms duplicate=0

  Total fired:
    [gs ] corrupt=0 drop=2 delay=0 duplicate=1
    [sat] corrupt=5 drop=0 delay=3 duplicate=0
```

#### `clear`
Cancels all pending faults on both links immediately. Faults that have already fired are not affected (the total fired counts remain accurate).

```
uhf-fault> clear
  [CLI] All pending faults cleared.
```

#### `help`
Reprints the command reference.

#### `quit` / `exit`
Shuts down the simulator cleanly.

---

### Examples

**Simulate a brief blackout window (satellite receives nothing for 5 commands):**
```
uhf-fault> drop sat 5
```

**Simulate a degraded RF link returning garbled telemetry to GS:**
```
uhf-fault> corrupt gs 10
```

**Test timeout handling — introduce a 2-second spike on both legs:**
```
uhf-fault> delay both 1 2000
```

**Simulate a multipath echo causing the satellite to receive a duplicate command:**
```
uhf-fault> duplicate sat 1
```

**Chain faults — corrupt one packet then drop the next:**
```
uhf-fault> corrupt sat 1
uhf-fault> drop sat 1
```
> Note: fault counters are independent, so both are armed simultaneously. The first packet will be corrupted; the second will be dropped.

**Check what's pending mid-test:**
```
uhf-fault> status
```

**Abort a test scenario cleanly:**
```
uhf-fault> clear
```

---

## Fault Types Explained

| Fault | What it does | What it tests |
|-------|-------------|---------------|
| **corrupt** | Flips 1–8 random bits in the packet payload | Checksum / CRC validation, malformed-packet handling, error detection |
| **drop** | Discards the packet entirely, no indication to either side | Retry logic, timeout handling, sequence number recovery, watchdog behaviour |
| **delay** | Holds the packet for N milliseconds before forwarding | Timeout thresholds, ordering sensitivity, queue depth under load |
| **duplicate** | Sends the packet twice back-to-back | Idempotency of command handlers, deduplication logic, sequence tracking |

Faults are applied **only to outgoing packets** (the moment data is about to leave the simulator toward a client). Incoming packets are always received and queued faithfully — this mirrors how a real radio impairment would manifest.

Fault counters are **independent per type**. You can have `corrupt=3` and `drop=1` armed on `sat` at the same time; the drop check runs first, and if a packet is dropped, corruption is skipped for that packet.

---

## Testing Scenarios

### Does the FSW retry after a dropped command?
```
uhf-fault> drop sat 1
# Send a command from GS — satellite should not receive it
# Observe whether FSW retransmits or GS times out and retries
```

### Does the FSW validate packet integrity?
```
uhf-fault> corrupt sat 5
# Send several commands — FSW should detect and reject malformed packets
# Check whether FSW logs errors or enters a fault state
```

### Does the GS handle a delayed telemetry response without crashing?
```
uhf-fault> delay gs 1 3000
# Send a command that expects a telemetry reply within 2s
# GS should time out gracefully, not hang
```

### Does the FSW handle duplicate commands safely (idempotency)?
```
uhf-fault> duplicate sat 3
# Send 3 commands — FSW will receive each one twice
# Verify commands are not executed twice (e.g. no double-fire of actuators)
```

### Simulate acquisition-of-signal / loss-of-signal boundary:
```
uhf-fault> drop both 10    # LOS window
# ... wait ...
uhf-fault> clear           # AOS restored
```
