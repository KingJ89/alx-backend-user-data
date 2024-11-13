#!/usr/bin/env python3
"""A module for encrypting passwords."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password using bcrypt with a randomly generated salt."""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if a hashed password matches the given plain-text password."""
    password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)
