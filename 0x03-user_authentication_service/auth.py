#!/usr/bin/env python3
"""Authentication module providing user management and password handling."""

from uuid import uuid4
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The plaintext password to hash.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generate a unique UUID string.

    Returns:
        str: A new UUID string.
    """
    return str(uuid4())


class Auth:
    """Class for managing authentication and user operations."""

    def __init__(self) -> None:
        """
        Initialize an instance of the `Auth` class.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user in the database.

        Args:
            email (str): Email address of the user.
            password (str): Plaintext password for the user.

        Returns:
            User: The created `User` object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate user login credentials.

        Args:
            email (str): The user's email.
            password (str): The plaintext password to verify.

        Returns:
            bool: `True` if credentials are valid, `False` otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> Union[None, str]:
        """
        Create a new session for a user and store the session ID.

        Args:
            email (str): The user's email address.

        Returns:
            Union[None, str]: The session ID if the user is found, otherwise `None`.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[None, User]:
        """
        Retrieve a user using their session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            Union[None, User]: The user associated with the session ID, or `None`.
        """
        if session_id is None:
            return None

        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Invalidate a user's session by clearing the session ID.

        Args:
            user_id (int): The user's ID.

        Returns:
            None
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a password reset token for a user.

        Args:
            email (str): The user's email address.

        Returns:
            str: The generated reset token.

        Raises:
            ValueError: If no user with the given email is found.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError("User not found")

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update a user's password using a valid reset token.

        Args:
            reset_token (str): The password reset token.
            password (str): The new plaintext password.

        Returns:
            None

        Raises:
            ValueError: If the reset token is invalid or not found.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")

        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)
