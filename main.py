"""FastAPI Application and API Route Definitions for Book Store.

This module initializes the FastAPI application instance, configures dependency injection
for database sessions, and exposes RESTful HTTP endpoints for Book CRUD operations.
Run with: uvicorn main:app --reload
"""

from contextlib import asynccontextmanager  # Manages asynchronous application lifecycle context
from typing import List  # Provides type hints for endpoint response lists
from fastapi import FastAPI, Depends, HTTPException, status  # Core FastAPI framework utilities and HTTP status codes
from sqlalchemy.orm import Session  # Database session type for dependency injection
import schemas  # Pydantic schemas for request validation and response serialization
import services  # Business logic and database service operations for Book entities
from db import get_db, create_table  # Dependency generator for DB sessions and table creation helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown lifecycle events.

    Ensures all database tables defined in ORM models are created before handling requests.

    Inputs:
        app (FastAPI): The running FastAPI application instance.

    Outputs:
        AsyncGenerator: Yields control back to the ASGI server.
    """
    create_table()  # Ensures tables exist in PostgreSQL upon application startup
    yield


app = FastAPI(lifespan=lifespan)  # Initializes the core FastAPI application instance with lifespan handler


@app.get("/books/", response_model=List[schemas.Book])
async def get_all_books(db: Session = Depends(get_db)) -> List[schemas.Book]:
    """Retrieve all book records from the database.

    Fetches the complete catalog of books using the service layer.

    Inputs:
        db (Session): Database session injected via FastAPI dependency.

    Outputs:
        List[schemas.Book]: A list of books serialized according to the Pydantic Book schema.
    """
    return services.get_books(db)  # Calls service layer to query all book records


@app.get("/books/{id}", response_model=schemas.Book)
async def get_book_by_id(id: int, db: Session = Depends(get_db)) -> schemas.Book:
    """Retrieve a single book by its unique primary key ID.

    Queries the book through the service layer and raises an HTTP 404 error if not found.

    Inputs:
        id (int): Primary key ID of the book provided in the URL path.
        db (Session): Database session injected via FastAPI dependency.

    Outputs:
        schemas.Book: The matching book record serialized according to the schema.
    """
    book_queryset = services.get_book(db, id)  # Queries the database for the book with the specified ID
    if book_queryset:  # Verifies the record was found in the database
        return book_queryset  # Returns the found book instance to be serialized by FastAPI

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Book ID Provided pr Book ID does not exist")  # Returns 404 when book is missing


@app.post("/books/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
async def create_new_book(book: schemas.BookCreate, db: Session = Depends(get_db)) -> schemas.Book:
    """Create a new book record in the database.

    Validates request payload via BookCreate schema and persists the record via the service layer.

    Inputs:
        book (schemas.BookCreate): Validated request payload containing new book details.
        db (Session): Database session injected via FastAPI dependency.

    Outputs:
        schemas.Book: Newly created book record with generated ID.
    """
    return services.create_book(db, book)  # Delegates creation and persistence to the service layer


@app.put("/books/{book_id}", response_model=schemas.Book)
async def update_book(book: schemas.BookCreate, book_id: int, db: Session = Depends(get_db)) -> schemas.Book:
    """Update an existing book record by its primary key ID.

    Accepts updated fields, validates them, and applies changes via the service layer.
    Raises an HTTP 404 error if the target book does not exist.

    Inputs:
        book (schemas.BookCreate): Validated payload containing updated book attributes.
        book_id (int): Primary key ID of the book to update, extracted from the path parameter.
        db (Session): Database session injected via FastAPI dependency.

    Outputs:
        schemas.Book: The updated book record serialized according to the schema.
    """
    db_update = services.update_book(db, book, book_id)  # Executes update logic in the service layer
    if not db_update:  # Checks if the book was found and successfully updated
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")  # Returns 404 if record does not exist

    return db_update  # Returns the updated record


@app.delete("/books/{book_id}", response_model=schemas.Book)
async def delete_book(book_id: int, db: Session = Depends(get_db)) -> schemas.Book:
    """Delete a book record from the database by its primary key ID.

    Removes the specified book via the service layer and raises an HTTP 404 if not found.

    Inputs:
        book_id (int): Primary key ID of the book to delete, extracted from the path parameter.
        db (Session): Database session injected via FastAPI dependency.

    Outputs:
        schemas.Book: The deleted book record confirming removal.
    """
    delete_entry = services.delete_book(db, book_id)  # Executes deletion in the service layer
    if delete_entry:  # Verifies the record existed and was successfully deleted
        return delete_entry  # Returns the deleted book record

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Not Found")  # Returns 404 if book was not found
