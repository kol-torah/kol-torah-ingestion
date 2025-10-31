# Kol Torah Admin Backend

FastAPI-based REST API for managing Kol Torah database records.

## Installation

```bash
poetry install
```

## Configuration

Copy `.env.example` to `.env` and configure your database connection and API settings.

## Running the Server

```bash
poetry run uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`
