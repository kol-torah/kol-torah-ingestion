# Kol Torah DB

SQLAlchemy models and database migrations for the Kol Torah project.

## Installation

```bash
poetry install
```

## Configuration

Copy `.env.example` to `.env` and configure your database connection:

```bash
cp .env.example .env
```

Edit `.env` and set your database connection string.

## Usage

```python
from kol_torah_db.database import SessionLocal, Base
from kol_torah_db.models import YourModel
```

## Migrations

### Create a new migration

```bash
# Activate the virtual environment
.\env\Scripts\Activate.ps1

# Create a new migration (auto-generate from models)
alembic revision --autogenerate -m "description of changes"
```

### Run migrations

```bash
# Activate the virtual environment
.\env\Scripts\Activate.ps1

# Upgrade to latest version
alembic upgrade head

# Downgrade one version
alembic downgrade -1

# Show current version
alembic current

# Show migration history
alembic history
```
