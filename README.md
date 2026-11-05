# IEC-FastAPI-Book-Store-App

A modular, production-grade RESTful API for a Book Store Application built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL** for the **IEC Agentic AI Bootcamp**.

---

## Architecture & Features

This project follows a **Layered Architecture (Separation of Concerns)** to ensure clean, testable, and maintainable code:

- **FastAPI**: High-performance asynchronous web framework with automatic OpenAPI documentation.
- **Service Layer**: Business logic and database operations are encapsulated in `services.py`, keeping API routes in `main.py` lean.
- **SQLAlchemy 2.0 ORM**: Type-safe relational database modeling with declarative Base mapping.
- **PostgreSQL (`psycopg[binary]`)**: High-performance database driver utilizing Psycopg 3.
- **Pydantic v2**: Strict request payload validation and ORM serialization.
- **Automated Lifecycle**: Database tables are automatically verified and created on server startup via FastAPI's `lifespan` handler.

---

## Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Python 3.12+** | Runtime environment |
| **FastAPI** | REST API framework |
| **Uvicorn** | ASGI server |
| **SQLAlchemy** | ORM & database toolkit |
| **PostgreSQL** | Relational database |
| **Psycopg 3 (`psycopg[binary]`)** | PostgreSQL database adapter |
| **Pydantic v2** | Data validation & serialization |
| **python-dotenv** | Environment configuration management |

---

## Project Structure

```text
IEC-FastAPI-Book-Store-App/
├── .env.example       # Template for environment variables
├── .gitignore          # Git exclusion rules
├── db.py               # Database engine, session factory, and table creation
├── main.py             # FastAPI app, lifespan setup, and API route controllers
├── models.py           # SQLAlchemy ORM database models (Book entity)
├── schemas.py          # Pydantic schemas for data validation and serialization
├── services.py         # Business logic and database CRUD operations
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

---

## Getting Started

### 1. Prerequisites
- **Python 3.12+**
- **PostgreSQL** installed and running locally or hosted in the cloud.

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/IEC-FastAPI-Book-Store-App.git
cd IEC-FastAPI-Book-Store-App
```

### 3. Create and Activate a Virtual Environment

**Using standard `venv`:**
```powershell
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
```

**Using `uv` (faster):**
```powershell
uv venv
.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```powershell
# Using pip:
python -m pip install -r requirements.txt

# Or using uv:
uv pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root based on `.env.example`:

```bash
cp .env.example .env
```

Update `SQLALCHEMY_DATABASE_URL` with your PostgreSQL credentials:
```env
SQLALCHEMY_DATABASE_URL=postgresql+psycopg://<username>:<password>@localhost:5432/<database_name>
```

---

## Running the Application

Start the local development server with auto-reload:

```powershell
uvicorn main:app --reload
```

The application will start at:
- **API Base URL**: `http://127.0.0.1:8000`
- **Interactive Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc Documentation**: `http://127.0.0.1:8000/redoc`

---

## API Endpoints

| HTTP Method | Endpoint | Status Code | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/books/` | `200 OK` | Retrieve all books |
| `GET` | `/books/{id}` | `200 OK` | Retrieve a specific book by ID |
| `POST` | `/books/` | `201 Created` | Create a new book record |
| `PUT` | `/books/{book_id}` | `200 OK` | Update an existing book by ID |
| `DELETE` | `/books/{book_id}` | `200 OK` | Delete a book by ID |

### Example Payloads

#### Create Book (`POST /books/`)
```json
{
  "title": "Clean Architecture",
  "description": "A Craftsman's Guide to Software Structure and Design",
  "author": "Robert C. Martin",
  "year": 2017
}
```

#### Successful Response (`200 OK` / `201 Created`)
```json
{
  "id": 1,
  "title": "Clean Architecture",
  "description": "A Craftsman's Guide to Software Structure and Design",
  "author": "Robert C. Martin",
  "year": 2017
}
```

---

## License & Attribution

Developed as part of the **IEC Agentic AI Bootcamp**. Distributed under the MIT License.
