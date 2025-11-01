"""API router for Rabbi endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/rabbis", tags=["rabbis"])


@router.get("/", response_model=List[schemas.RabbiResponse])
def list_rabbis(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get a list of all rabbis."""
    rabbis = crud.get_rabbis(db, skip=skip, limit=limit)
    return rabbis


@router.get("/{rabbi_id}", response_model=schemas.RabbiResponse)
def get_rabbi(rabbi_id: int, db: Session = Depends(get_db)):
    """Get a specific rabbi by ID."""
    rabbi = crud.get_rabbi(db, rabbi_id)
    if not rabbi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rabbi with id {rabbi_id} not found"
        )
    return rabbi


@router.post("/", response_model=schemas.RabbiResponse, status_code=status.HTTP_201_CREATED)
def create_rabbi(rabbi: schemas.RabbiCreate, db: Session = Depends(get_db)):
    """Create a new rabbi."""
    # Check if slug already exists
    existing_rabbi = crud.get_rabbi_by_slug(db, rabbi.slug)
    if existing_rabbi:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rabbi with slug '{rabbi.slug}' already exists"
        )
    
    return crud.create_rabbi(db, rabbi)


@router.put("/{rabbi_id}", response_model=schemas.RabbiResponse)
def update_rabbi(rabbi_id: int, rabbi: schemas.RabbiUpdate, db: Session = Depends(get_db)):
    """Update a rabbi."""
    # If slug is being updated, check it doesn't conflict with another rabbi
    if rabbi.slug:
        existing_rabbi = crud.get_rabbi_by_slug(db, rabbi.slug)
        if existing_rabbi and existing_rabbi.id != rabbi_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Rabbi with slug '{rabbi.slug}' already exists"
            )
    
    updated_rabbi = crud.update_rabbi(db, rabbi_id, rabbi)
    if not updated_rabbi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rabbi with id {rabbi_id} not found"
        )
    return updated_rabbi


@router.delete("/{rabbi_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rabbi(rabbi_id: int, db: Session = Depends(get_db)):
    """Delete a rabbi and all associated series."""
    success = crud.delete_rabbi(db, rabbi_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rabbi with id {rabbi_id} not found"
        )
    return None
