"""API router for Series endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/series", tags=["series"])


@router.get("/", response_model=List[schemas.SeriesResponse])
def list_series(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get a list of all series."""
    series = crud.get_all_series(db, skip=skip, limit=limit)
    return series


@router.get("/by-rabbi/{rabbi_id}", response_model=List[schemas.SeriesResponse])
def get_series_by_rabbi(rabbi_id: int, db: Session = Depends(get_db)):
    """Get all series for a specific rabbi."""
    # Check if rabbi exists
    rabbi = crud.get_rabbi(db, rabbi_id)
    if not rabbi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rabbi with id {rabbi_id} not found"
        )
    
    series = crud.get_series_by_rabbi(db, rabbi_id)
    return series


@router.get("/{series_id}", response_model=schemas.SeriesResponse)
def get_series(series_id: int, db: Session = Depends(get_db)):
    """Get a specific series by ID."""
    series = crud.get_series(db, series_id)
    if not series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Series with id {series_id} not found"
        )
    return series


@router.post("/", response_model=schemas.SeriesResponse, status_code=status.HTTP_201_CREATED)
def create_series(series: schemas.SeriesCreate, db: Session = Depends(get_db)):
    """Create a new series."""
    # Check if rabbi exists
    rabbi = crud.get_rabbi(db, series.rabbi_id)
    if not rabbi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rabbi with id {series.rabbi_id} not found"
        )
    
    return crud.create_series(db, series)


@router.put("/{series_id}", response_model=schemas.SeriesResponse)
def update_series(series_id: int, series: schemas.SeriesUpdate, db: Session = Depends(get_db)):
    """Update a series."""
    # If rabbi_id is being updated, check the new rabbi exists
    if series.rabbi_id:
        rabbi = crud.get_rabbi(db, series.rabbi_id)
        if not rabbi:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rabbi with id {series.rabbi_id} not found"
            )
    
    updated_series = crud.update_series(db, series_id, series)
    if not updated_series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Series with id {series_id} not found"
        )
    return updated_series


@router.delete("/{series_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_series(series_id: int, db: Session = Depends(get_db)):
    """Delete a series."""
    success = crud.delete_series(db, series_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Series with id {series_id} not found"
        )
    return None
