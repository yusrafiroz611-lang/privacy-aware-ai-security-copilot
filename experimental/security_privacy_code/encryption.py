"""Authenticated encryption helpers for sensitive strings.

Generate a key once and store it in a secret manager/environment variable.
Do not commit real encryption keys to GitHub or include them in the ZIP.
"""
import os
from cryptography.fernet import Fernet, InvalidToken


def generate_key() -> bytes:
    """Generate a Fernet key. Save it securely outside source control."""
    return Fernet.generate_key()


def encrypt_text(plaintext: str, key: bytes | str | None = None) -> tuple[str, str]:
    """Encrypt text and return (ciphertext, key_used).

    If key is omitted, a new key is generated and returned as a URL-safe string.
    For a real application, pass a securely stored key instead.
    """
    if not isinstance(plaintext, str):
        raise TypeError("plaintext must be a string")
    if key is None:
        key_bytes = generate_key()
    else:
        key_bytes = key.encode("utf-8") if isinstance(key, str) else key
    token = Fernet(key_bytes).encrypt(plaintext.encode("utf-8")).decode("utf-8")
    return token, key_bytes.decode("utf-8")


def decrypt_text(ciphertext: str, key: bytes | str) -> str:
    """Decrypt text; raises InvalidToken if the key/token is invalid."""
    key_bytes = key.encode("utf-8") if isinstance(key, str) else key
    try:
        return Fernet(key_bytes).decrypt(ciphertext.encode("utf-8")).decode("utf-8")
    except InvalidToken:
        raise
