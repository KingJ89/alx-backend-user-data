#!/usr/bin/env python3
"""Database module to manage User operations."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """Class to interact with the database."""

    def __init__(self) -> None:
        """
        Initializes the database connection and sets up the schema.

        - Creates an SQLite database `a.db`.
        - Drops existing tables and recreates them to ensure a clean slate.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)  # Clear existing tables
        Base.metadata.create_all(self._engine)  # Recreate tables
        self.__session = None  # Lazy-initialized session object

    @property
    def _session(self) -> Session:
        """
        Provides a memoized session object to interact with the database.

        Returns:
            Session: SQLAlchemy session for database operations.
        """
        if self.__session is None:
            session_factory = sessionmaker(bind=self._engine)
            self.__session = session_factory()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The hashed password for the user.

        Returns:
            User: The newly created `User` object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds the first user that matches the given filter criteria.

        Args:
            **kwargs: Arbitrary keyword arguments to filter users.

        Returns:
            User: The user object matching the filters.

        Raises:
            NoResultFound: If no user matches the criteria.
            InvalidRequestError: If the query is malformed.
        """
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound as e:
            raise NoResultFound(f"No user found with criteria: {kwargs}") from e
        except InvalidRequestError as e:
            raise InvalidRequestError("Invalid filter arguments.") from e

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments for fields to update.

        Raises:
            ValueError: If an attribute in `kwargs` is invalid or does not exist.
        """
        user = self.find_user_by(id=user_id)
        for attribute, value in kwargs.items():
            if hasattr(user, attribute):
                setattr(user, attribute, value)
            else:
                raise ValueError(f"Invalid attribute: {attribute}")
        self._session.commit()
