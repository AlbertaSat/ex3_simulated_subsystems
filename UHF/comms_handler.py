"""Communications handler for encrypted uplink frames.

Parses the sequential AES-GCM nonce, decrypts authenticated ciphertext,
and ignores frames that reuse a previous nonce (replay protection).
Downlink traffic is not handled here and remains plaintext.

Copyright 2026 [Samuel Olabode]. Licensed under the Apache License, Version 2.0
"""

from __future__ import annotations

from uplink_crypto import UplinkCryptoError, UplinkDecryptor


class CommsHandler:
    """Receive-side handler for encrypted operator uplink messages."""

    def __init__(self, decryptor: UplinkDecryptor | None = None):
        """Create a comms handler.

        Args:
            decryptor: Optional decryptor instance. A default decryptor
                loaded from the key store is created when omitted.
        """
        self._decryptor = decryptor if decryptor is not None else UplinkDecryptor()
        self._accepted = 0
        self._ignored = 0

    @property
    def accepted_count(self) -> int:
        """Number of uplink frames successfully decrypted."""
        return self._accepted

    @property
    def ignored_count(self) -> int:
        """Number of uplink frames dropped (replay, auth failure, etc.)."""
        return self._ignored

    @property
    def last_nonce(self) -> int:
        """Most recently accepted nonce counter."""
        return self._decryptor.last_nonce

    def handle_uplink(self, frame: bytes) -> bytes | None:
        """Decrypt an encrypted uplink frame, or ignore it.

        Args:
            frame: Encrypted uplink bytes from the operator / ground station.

        Returns:
            bytes | None: Decrypted plaintext on success, or None when the
                frame is ignored (previous nonce, auth failure, malformed).
        """
        try:
            plaintext = self._decryptor.decrypt(frame)
        except UplinkCryptoError as exc:
            self._ignored += 1
            print(f"[CommsHandler] ignoring uplink frame: {exc}")
            return None

        self._accepted += 1
        print(
            f"[CommsHandler] decrypted uplink nonce="
            f"{self._decryptor.last_nonce} "
            f"({len(plaintext)} plaintext bytes)"
        )
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
