#!/usr/bin/env python3
"""SQLAlchemy ORM model definition for User."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Base class for all ORM models
Base = declarative_base()


class User(Base):
    """
    Represents the 'users' table in the database.

    Attributes:
        id (int): Primary key, auto-incremented unique identifier for each user.
        email (str): User's email address, required and must be unique.
        hashed_password (str): The hashed version of the user's password.
        session_id (str, optional): Session identifier for authentication.
        reset_token (str, optional): Token for password reset operations.
    """
    
    # Table name
    
    __tablename__ = 'users'
    
    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String(250), nullable=False, unique=True, doc="Unique email address for the user.")
    hashed_password = Column(String(250), nullable=False, doc="Password stored in hashed format.")
    session_id = Column(String(128), nullable=True, doc="Session token for tracking user sessions.")
    reset_token = Column(String(128), nullable=True, doc="Token used for resetting the user's password.")
