"""Database Models Definition.

This module defines the SQLAlchemy ORM models representing the application's
database tables and data structures, specifically the Book entity.
"""

from db import Base  # Base class that connects models to SQLAlchemy's declarative system
from sqlalchemy import Column, Integer, String  # Column types and definitions for mapping database schema


class Book(Base):
    """SQLAlchemy model representing the 'Books' database table.

    Maps book attributes to table columns to enable ORM-based database operations.
    """

    __tablename__ = "Books"  # Specifies the exact table name in the relational database

    id= Column(Integer, primary_key=True, index=True)  # Primary key identifier with an index for faster lookups
    title= Column(String, index=True)  # Book title stored as string, indexed for efficient search queries
    description= Column(String, index=True)  # Book summary/details, indexed for search filtering
    author= Column(String, index=True)  # Author name, indexed for author-based queries
    year= Column(Integer)  # Publication year stored as an integer for chronological filtering/sorting
