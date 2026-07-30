"""AES-256-GCM helpers for encrypted uplink frames.

Mirrors the aes-gcm / Aes256Gcm approach planned for flight software:
sequential nonces act as a message counter, and GCM authenticates the
ciphertext so tampered frames fail decryption.

Wire format:  nonce (12 bytes, big-endian counter) || ciphertext||tag

Copyright 2026 [Samuel Olabode]. Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from key_store import KEY_SIZE, NONCE_SIZE, load_aes_key


class UplinkCryptoError(Exception):
    """Raised when an uplink frame cannot be encrypted or decrypted."""


class UplinkEncryptor:
    """Encrypt operator uplink messages with sequential AES-GCM nonces."""

    def __init__(self, key: bytes | None = None, start_counter: int = 1):
        """Create an encryptor.

        Args:
            key: Optional 32-byte AES key. Loads from key store when omitted.
            start_counter: First nonce counter value to use (default 1).
        """
        if start_counter < 1:
            raise ValueError("start_counter must be >= 1")
        self._key = key if key is not None else load_aes_key()
        if len(self._key) != KEY_SIZE:
            raise ValueError(f"AES-256 key must be {KEY_SIZE} bytes")
        self._aesgcm = AESGCM(self._key)
        self._counter = start_counter

    @property
    def next_counter(self) -> int:
        """Return the counter that will be used for the next encrypt call."""
        return self._counter

    def encrypt(self, plaintext: bytes) -> bytes:
        """Encrypt plaintext and return nonce || ciphertext||tag.

        Args:
            plaintext: Raw operator message bytes.

        Returns:
            bytes: Encrypted uplink frame including the sequential nonce.
        """
        if not isinstance(plaintext, (bytes, bytearray)):
            raise TypeError("plaintext must be bytes")
        nonce = self._counter.to_bytes(NONCE_SIZE, "big")
        ciphertext = self._aesgcm.encrypt(nonce, bytes(plaintext), None)
        self._counter += 1
        return nonce + ciphertext


class UplinkDecryptor:
    """Decrypt uplink frames and enforce monotonic nonce counters."""

    def __init__(self, key: bytes | None = None):
        """Create a decryptor.

        Args:
            key: Optional 32-byte AES key. Loads from key store when omitted.
        """
        self._key = key if key is not None else load_aes_key()
        if len(self._key) != KEY_SIZE:
            raise ValueError(f"AES-256 key must be {KEY_SIZE} bytes")
        self._aesgcm = AESGCM(self._key)
        self._last_nonce = 0

    @property
    def last_nonce(self) -> int:
        """Return the most recently accepted nonce counter."""
        return self._last_nonce

    def decrypt(self, frame: bytes) -> bytes:
        """Parse the nonce, reject replays, and decrypt the ciphertext.

        Args:
            frame: Encrypted uplink frame (nonce || ciphertext||tag).

        Returns:
            bytes: Decrypted plaintext.

        Raises:
            UplinkCryptoError: If the frame is truncated, replayed, or
                fails authentication.
        """
        if not isinstance(frame, (bytes, bytearray)):
            raise TypeError("frame must be bytes")
        if len(frame) <= NONCE_SIZE:
            raise UplinkCryptoError("uplink frame too short")

        nonce = bytes(frame[:NONCE_SIZE])
        ciphertext = bytes(frame[NONCE_SIZE:])
        counter = int.from_bytes(nonce, "big")

        if counter <= self._last_nonce:
            raise UplinkCryptoError(
                f"rejected replayed or stale nonce {counter} "
                f"(last accepted {self._last_nonce})"
            )

        try:
            plaintext = self._aesgcm.decrypt(nonce, ciphertext, None)
        except InvalidTag as exc:
            raise UplinkCryptoError(
                "AES-GCM authentication failed for uplink frame"
            ) from exc

        self._last_nonce = counter
        return plaintext


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
