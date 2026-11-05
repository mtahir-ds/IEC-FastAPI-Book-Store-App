"""Database Services and Business Logic for Book Operations.

This module encapsulates all database CRUD (Create, Read, Update, Delete) operations
for the Book entity, separating data access logic from API route controllers.
"""

from typing import List, Optional  # Type hints for collections and optional return values
from sqlalchemy.orm import Session  # Database session type for database operations and transactions
from models import Book  # SQLAlchemy ORM model representing the 'Books' database table
from schemas import BookCreate  # Pydantic schema for validating book creation and update payloads


def create_book(db: Session, data: BookCreate) -> Book:
    """Create a new book record in the database.

    Converts the validated Pydantic schema into an ORM instance and persists
    it to the database using an explicit transaction.

    Inputs:
        db (Session): Active SQLAlchemy database session for executing transactions.
        data (BookCreate): Validated Pydantic schema containing book attributes.

    Outputs:
        Book: The newly created and committed Book ORM model instance with its generated ID.
    """
    book_instance = Book(**data.model_dump())  # Unpacks validated schema fields into the ORM model constructor

    db.add(book_instance)  # Stages the new book instance in the session for persistence
    db.commit()  # Commits the transaction to save changes permanently to the database
    db.refresh(book_instance)  # Refreshes the instance with generated database attributes (like primary key ID)

    return book_instance  # Returns the populated ORM instance to the caller


def get_books(db: Session) -> List[Book]:
    """Retrieve all book records from the database.

    Queries the books table and returns all existing entries as ORM instances.

    Inputs:
        db (Session): Active SQLAlchemy database session for executing the query.

    Outputs:
        List[Book]: A list of all Book ORM model instances found in the database.
    """
    return db.query(Book).all()  # Fetches and returns all book records from the table


def get_book(db: Session, book_id: int) -> Optional[Book]:
    """Retrieve a single book record by its primary key ID.

    Filters the books table by the provided ID and returns the first match.

    Inputs:
        db (Session): Active SQLAlchemy database session for executing the query.
        book_id (int): Primary key ID of the book to retrieve.

    Outputs:
        Optional[Book]: The matching Book ORM model instance if found, or None if not found.
    """
    return db.query(Book).filter(Book.id == book_id).first()  # Queries the database for a matching book by ID


def update_book(db: Session, book: BookCreate, book_id: int) -> Optional[Book]:
    """Update an existing book record's attributes in the database.

    Finds a book by ID, dynamically updates its fields with the provided payload,
    and commits the changes to the database.

    Inputs:
        db (Session): Active SQLAlchemy database session for executing the update.
        book (BookCreate): Validated Pydantic schema containing updated field values.
        book_id (int): Primary key ID of the book to be updated.

    Outputs:
        Optional[Book]: The updated Book ORM model instance if found and modified, or None if not found.
    """
    book_queryset = db.query(Book).filter(Book.id == book_id).first()  # Queries the existing book record by ID

    if book_queryset:  # Verifies the record exists before attempting attribute updates
        for key, value in book.model_dump().items():  # Iterates through validated field-value pairs
            setattr(book_queryset, key, value)  # Dynamically assigns new values to existing record attributes

        db.commit()  # Commits the updated attributes to the database
        db.refresh(book_queryset)  # Refreshes the ORM instance to ensure synchronization with the DB

        return book_queryset  # Returns the updated ORM model instance


def delete_book(db: Session, book_id: int) -> Optional[Book]:
    """Delete a book record from the database by its primary key ID.

    Finds a book by ID, marks it for deletion, and commits the transaction.

    Inputs:
        db (Session): Active SQLAlchemy database session for executing the deletion.
        book_id (int): Primary key ID of the book to delete.

    Outputs:
        Optional[Book]: The deleted Book ORM model instance if found and removed, or None if not found.
    """
    book_queryset = db.query(Book).filter(Book.id == book_id).first()  # Queries the target book record by ID

    if book_queryset:  # Verifies the record exists prior to deleting
        db.delete(book_queryset)  # Marks the found book record for removal from the session
        db.commit()  # Commits the deletion to permanently remove the record from the database
        return book_queryset  # Returns the deleted book instance confirming removal
