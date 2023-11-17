#!/usr/bin/env python3
"""module for authentication"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash password to bytes"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
