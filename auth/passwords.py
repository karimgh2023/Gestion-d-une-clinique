"""
Hachage des mots de passe avec PBKDF2-HMAC-SHA256 (bibliothèque standard).
Ne jamais stocker le mot de passe en clair en base.
"""

from __future__ import annotations

import hashlib
import secrets

PBKDF2_ITERATIONS = 150_000


def hash_password(plain: str) -> tuple[str, str]:
    """Retourne (sel_hex, hash_hex) pour stockage MySQL."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        plain.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return salt.hex(), digest.hex()


def verify_password(plain: str, salt_hex: str, stored_hash_hex: str) -> bool:
    try:
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(stored_hash_hex)
    except ValueError:
        return False
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        plain.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return digest == expected
