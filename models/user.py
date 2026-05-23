"""
models/user.py
User model helper functions for iLEARN.
"""

import hashlib


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain password against a hashed one."""
    return hash_password(plain) == hashed


def get_user_by_id(conn, user_id: int):
    """Fetch a user record by ID."""
    return conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()


def get_user_by_username(conn, username: str):
    """Fetch a user record by username."""
    return conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()


def create_user(conn, username: str, password: str, email: str = ""):
    """
    Create a new user. Returns the new user's ID, or None if the username exists.
    """
    try:
        cursor = conn.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, hash_password(password), email)
        )
        conn.commit()
        return cursor.lastrowid
    except Exception:
        return None  # Username already taken
