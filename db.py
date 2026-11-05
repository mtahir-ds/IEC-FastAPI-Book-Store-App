"""Database Configuration and Connection Setup.

This module initializes the database connection engine, session management,
declarative base class, and utility functions for session lifecycle management
and table creation in PostgreSQL using SQLAlchemy.
"""

from sqlalchemy import create_engine  # Creates the database engine to establish and manage connections to the database
from sqlalchemy.orm import sessionmaker, declarative_base  # sessionmaker manages DB sessions/transactions; declarative_base provides a base class for ORM models

from dotenv import load_dotenv  # Loads environment variables from a .env file to keep secrets out of source code

import os  # Provides access to environment variables to securely read configuration

load_dotenv()  # Reads the .env file and loads variables into the environment so they are accessible to the app

SQLALCHEMY_DATABASE_URL = os.getenv(key="SQLALCHEMY_DATABASE_URL")  # Retrieves the DB connection URL from the environment to avoid hardcoding credentials

engine = create_engine(SQLALCHEMY_DATABASE_URL)  # Initializes the connection pool and dialect to communicate with the database

SessionLocal = sessionmaker(
    autocommit=False,  # Prevents automatic commits so transactions remain explicit and atomic
    autoflush=False,  # Prevents premature flushing of queries before committing or explicitly flushing
    bind=engine,  # Associates the session factory with our configured database engine
)

Base = declarative_base()  # Base class for all ORM models to inherit from and register their schema metadata


def get_db():
    """Create and yield a database session per request.

    Acts as a FastAPI dependency to provide an isolated database session and
    guarantees session cleanup upon completion to avoid connection leaks.

    Inputs:
        None

    Outputs:
        Generator: Yields an active SQLAlchemy Session instance.
    """
    db = SessionLocal()  # Instantiates a new database session for the request

    try:
        yield db  # Provides the session to the calling endpoint/context
    except Exception as e:
        print(f"Exception: {e}")
        raise  # Re-raises the exception so FastAPI can manage the HTTP error response cycle
    finally:
        db.close()  # Ensures the session is closed when the request lifecycle ends


def create_table():
    """Create all database tables defined in the ORM models.

    Emits DDL statements to create any missing tables bound to the declarative Base metadata.

    Inputs:
        None

    Outputs:
        None
    """
    import models  # Imports ORM models to register mapped tables with Base.metadata before creation
    Base.metadata.create_all(
        bind=engine
    )  # Generates and executes CREATE TABLE SQL statements for all registered models


if __name__ == "__main__":
    create_table()
    print("Tables created")
