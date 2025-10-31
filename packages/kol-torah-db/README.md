# Kol Torah DB

SQLAlchemy models and database migrations for the Kol Torah project.

## Installation

```bash
poetry install
```

## Usage

```python
from kol_torah_db.models import YourModel
```

## Migrations

Run migrations using Alembic:

```bash
poetry run alembic upgrade head
```
