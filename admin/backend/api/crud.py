"""CRUD operations for database models."""

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from kol_torah_db.models import Rabbi, Series
from . import schemas


# ==================== Rabbi CRUD ====================

def get_rabbis(db: Session, skip: int = 0, limit: int = 100) -> List[Rabbi]:
    """Get a list of rabbis."""
    return db.query(Rabbi).offset(skip).limit(limit).all()


def get_rabbi(db: Session, rabbi_id: int) -> Optional[Rabbi]:
    """Get a single rabbi by ID."""
    return db.query(Rabbi).filter(Rabbi.id == rabbi_id).first()


def get_rabbi_by_slug(db: Session, slug: str) -> Optional[Rabbi]:
    """Get a single rabbi by slug."""
    return db.query(Rabbi).filter(Rabbi.slug == slug).first()


def create_rabbi(db: Session, rabbi: schemas.RabbiCreate) -> Rabbi:
    """Create a new rabbi."""
    db_rabbi = Rabbi(**rabbi.model_dump())
    db.add(db_rabbi)
    db.commit()
    db.refresh(db_rabbi)
    return db_rabbi


def update_rabbi(db: Session, rabbi_id: int, rabbi: schemas.RabbiUpdate) -> Optional[Rabbi]:
    """Update a rabbi."""
    db_rabbi = get_rabbi(db, rabbi_id)
    if not db_rabbi:
        return None
    
    # Update only provided fields
    update_data = rabbi.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_rabbi, field, value)
    
    # Manually set updated_at
    db_rabbi.updated_at = func.now()
    
    db.commit()
    db.refresh(db_rabbi)
    return db_rabbi


def delete_rabbi(db: Session, rabbi_id: int) -> bool:
    """Delete a rabbi and all associated series."""
    db_rabbi = get_rabbi(db, rabbi_id)
    if not db_rabbi:
        return False
    
    # Delete associated series first
    db.query(Series).filter(Series.rabbi_id == rabbi_id).delete()
    
    # Delete the rabbi
    db.delete(db_rabbi)
    db.commit()
    return True


# ==================== Series CRUD ====================

def get_all_series(db: Session, skip: int = 0, limit: int = 100) -> List[Series]:
    """Get a list of all series."""
    return db.query(Series).offset(skip).limit(limit).all()


def get_series_by_rabbi(db: Session, rabbi_id: int) -> List[Series]:
    """Get all series for a specific rabbi."""
    return db.query(Series).filter(Series.rabbi_id == rabbi_id).all()


def get_series(db: Session, series_id: int) -> Optional[Series]:
    """Get a single series by ID."""
    return db.query(Series).filter(Series.id == series_id).first()


def create_series(db: Session, series: schemas.SeriesCreate) -> Series:
    """Create a new series."""
    db_series = Series(**series.model_dump())
    db.add(db_series)
    db.commit()
    db.refresh(db_series)
    return db_series


def update_series(db: Session, series_id: int, series: schemas.SeriesUpdate) -> Optional[Series]:
    """Update a series."""
    db_series = get_series(db, series_id)
    if not db_series:
        return None
    
    # Update only provided fields
    update_data = series.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_series, field, value)
    
    # Manually set updated_at
    db_series.updated_at = func.now()
    
    db.commit()
    db.refresh(db_series)
    return db_series


def delete_series(db: Session, series_id: int) -> bool:
    """Delete a series."""
    db_series = get_series(db, series_id)
    if not db_series:
        return False
    
    db.delete(db_series)
    db.commit()
    return True
