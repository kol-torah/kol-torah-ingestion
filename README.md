# Kol Torah Ingestion

A comprehensive system for ingesting, managing, and administering Torah lessons stored in a PostgreSQL database.

## Project Overview

This repository contains three main components:

1. **Database Package** - A Python package with SQLAlchemy models and migrations for the Kol Torah database
2. **Ingestion Pipelines** - Python-based data ingestion pipelines for processing Torah lessons from various sources
3. **Admin Interface** - A web-based administrative interface for managing database records

## Directory Structure

```
kol-torah-ingestion/
├── packages/
│   └── kol-torah-db/          # Database package with SQLAlchemy models
│       ├── .venv/             # Python virtual environment (ignored)
│       ├── kol_torah_db/      # Main package code
│       │   ├── models/        # SQLAlchemy models
│       │   └── migrations/    # Database migrations (Alembic)
│       ├── pyproject.toml     # Poetry configuration and dependencies
│       └── poetry.lock        # Locked dependencies
│
├── ingestion/                 # Ingestion pipelines
│   ├── .venv/                 # Python virtual environment (ignored)
│   ├── pipelines/             # Individual pipeline modules
│   ├── config/                # Configuration files
│   ├── pyproject.toml         # Poetry configuration and dependencies
│   └── poetry.lock            # Locked dependencies
│
├── admin/                     # Admin interface
│   ├── backend/               # Python backend (FastAPI/Flask)
│   │   ├── .venv/             # Python virtual environment (ignored)
│   │   ├── api/               # API endpoints
│   │   ├── pyproject.toml     # Poetry configuration and dependencies
│   │   └── poetry.lock        # Locked dependencies
│   │
│   └── frontend/              # React frontend
│       ├── node_modules/      # Node modules (ignored)
│       ├── src/               # React source code
│       ├── public/            # Static assets
│       └── package.json       # Node dependencies
│
├── .gitignore                 # Git ignore rules
├── LICENSE                    # Project license
└── README.md                  # This file
```

## Components

### 1. Kol Torah DB Package (`packages/kol-torah-db`)

A Python package that provides:
- SQLAlchemy ORM models for all database entities
- Alembic migrations for database schema management
- Database connection utilities
- Shared database logic used across all components

**Setup:**
```bash
cd packages/kol-torah-db
poetry install
poetry shell
```

### 2. Ingestion Pipelines (`ingestion`)

Python-based data ingestion pipelines for processing and importing Torah lessons from various sources into the PostgreSQL database.

**Features:**
- Multiple source adapters
- Data validation and transformation
- Batch processing capabilities
- Error handling and logging

**Setup:**
```bash
cd ingestion
poetry install
poetry shell
```

### 3. Admin Interface (`admin`)

A modern web-based interface for managing database records.

#### Backend (`admin/backend`)

Python-based REST API providing endpoints for CRUD operations on database entities.

**Setup:**
```bash
cd admin/backend
poetry install
poetry shell
```

#### Frontend (`admin/frontend`)

React-based single-page application for the administrative interface.

**Setup:**
```bash
cd admin/frontend
pnpm install
pnpm dev
```

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Poetry (Python dependency management)
- PostgreSQL 12 or higher
- Node.js 18 or higher (for admin frontend)
- pnpm (for admin frontend)

### Database Setup

1. Create a PostgreSQL database
2. Configure database connection in each component
3. Run migrations from the `kol-torah-db` package

### Development Workflow

1. Set up the database package first
2. Run migrations to create database schema
3. Set up ingestion pipelines and test with sample data
4. Launch admin backend and frontend for management

## Environment Variables

Each component requires specific environment variables. Create `.env` files in each component directory:

- `packages/kol-torah-db/.env` - Database connection strings
- `ingestion/.env` - Pipeline configuration and database connection
- `admin/backend/.env` - API configuration and database connection
- `admin/frontend/.env` - API endpoint URLs

## Contributing

Please follow Python PEP 8 style guidelines for Python code and use appropriate linting tools for JavaScript/React code.

## License

See LICENSE file for details.
