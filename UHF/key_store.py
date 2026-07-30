"""Load the AES-256-GCM key used for encrypted uplink.

The key is expected from a secure location. For development a placeholder
file under UHF/keys/ is used. Production deployments should set
UHF_AES256_KEY to a 64-character hex string (32 raw bytes).

Copyright 2026 [Samuel Olabode]. Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

import os
from pathlib import Path

KEY_SIZE = 32
NONCE_SIZE = 12
TAG_SIZE = 16

# Overhead of nonce + GCM authentication tag on every encrypted uplink frame.
ENCRYPTED_FRAME_OVERHEAD = NONCE_SIZE + TAG_SIZE

_KEYS_DIR = Path(__file__).resolve().parent / "keys"
_DEV_KEY_PATH = _KEYS_DIR / "dev_aes256.key"
_ENV_VAR = "UHF_AES256_KEY"


def _parse_hex_key(hex_key: str) -> bytes:
    """Parse a hex-encoded AES-256 key and validate its length."""
    cleaned = "".join(
        line.split("#", 1)[0].strip()
        for line in hex_key.splitlines()
    )
    cleaned = cleaned.replace(" ", "").replace("\n", "")
    try:
        key = bytes.fromhex(cleaned)
    except ValueError as exc:
        raise ValueError("AES key must be valid hexadecimal") from exc
    if len(key) != KEY_SIZE:
        raise ValueError(
            f"AES-256 key must be {KEY_SIZE} bytes, got {len(key)}"
        )
    return key


def load_aes_key(key_path: Path | None = None) -> bytes:
    """Load the AES-256 key from the environment or a key file.

    Precedence:
      1. UHF_AES256_KEY environment variable (hex)
      2. key_path argument, or the development placeholder file

    Args:
        key_path: Optional path to a hex-encoded key file.

    Returns:
        bytes: A 32-byte AES-256 key.
    """
    env_key = os.environ.get(_ENV_VAR)
    if env_key:
        return _parse_hex_key(env_key)

    path = key_path if key_path is not None else _DEV_KEY_PATH
    if not path.is_file():
        raise FileNotFoundError(
            f"AES key file not found at {path}. "
            f"Set {_ENV_VAR} or provide a development key file."
        )
    return _parse_hex_key(path.read_text(encoding="utf-8"))


# pylint: disable=duplicate-code
# no error
__author__ = "Samuel Olabode"
__copyright__ = """
    Copyright (C) 2026, [Samuel Olabode]
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."""
