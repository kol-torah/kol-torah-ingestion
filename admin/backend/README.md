# Kol Torah Admin Backend

FastAPI backend for the Kol Torah admin interface.

## Setup

1. **Install dependencies:**
   ```bash
   poetry install
   ```

2. **Configure database:**
   - Copy `.env.example` to `.env` (or create `.env`)
   - Update `DATABASE_URL` with your database credentials
   - The backend uses the `webapp` role with read/write access to the `main` schema

3. **Activate virtual environment:**
   ```bash
   poetry shell
   ```

## Running the Server

### Development Mode (with auto-reload):
```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive API docs (Swagger): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc

## API Endpoints

### Rabbis
- `GET /rabbis/` - List all rabbis
- `GET /rabbis/{rabbi_id}` - Get a specific rabbi
- `POST /rabbis/` - Create a new rabbi
- `PUT /rabbis/{rabbi_id}` - Update a rabbi
- `DELETE /rabbis/{rabbi_id}` - Delete a rabbi (and all associated series)

### Series
- `GET /series/` - List all series
- `GET /series/by-rabbi/{rabbi_id}` - Get all series for a specific rabbi
- `GET /series/{series_id}` - Get a specific series
- `POST /series/` - Create a new series
- `PUT /series/{series_id}` - Update a series
- `DELETE /series/{series_id}` - Delete a series

## Project Structure

```
admin/backend/
├── api/
│   ├── __init__.py
│   ├── main.py          # FastAPI app and configuration
│   ├── database.py      # Database connection and session
│   ├── schemas.py       # Pydantic models for request/response
│   ├── crud.py          # Database operations
│   └── routers/
│       ├── __init__.py
│       ├── rabbis.py    # Rabbi endpoints
│       └── series.py    # Series endpoints
├── .env                 # Environment variables (not in git)
├── pyproject.toml       # Dependencies
├── run.py              # Development server startup
└── README.md
```

## Development

The backend uses:
- **FastAPI** for the web framework
- **SQLAlchemy** for ORM
- **Pydantic** for data validation
- **kol-torah-db** package for database models

The backend connects to the database using credentials from the `.env` file, which should use the `webapp` role for appropriate permissions.
