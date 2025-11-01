"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


# ==================== Rabbi Schemas ====================

class RabbiBase(BaseModel):
    """Base schema for Rabbi with common fields."""
    name_hebrew: str = Field(..., min_length=1, max_length=255)
    name_english: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    website_url: Optional[str] = Field(None, max_length=500)


class RabbiCreate(RabbiBase):
    """Schema for creating a new Rabbi."""
    pass


class RabbiUpdate(BaseModel):
    """Schema for updating a Rabbi (all fields optional)."""
    name_hebrew: Optional[str] = Field(None, min_length=1, max_length=255)
    name_english: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    website_url: Optional[str] = Field(None, max_length=500)


class RabbiResponse(RabbiBase):
    """Schema for Rabbi responses."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ==================== Series Schemas ====================

class SeriesBase(BaseModel):
    """Base schema for Series with common fields."""
    rabbi_id: int
    name_hebrew: str = Field(..., min_length=1, max_length=255)
    name_english: str = Field(..., min_length=1, max_length=255)
    description_hebrew: Optional[str] = None
    description_english: Optional[str] = None
    website_url: Optional[str] = Field(None, max_length=500)
    type: str = Field(..., min_length=1, max_length=100)


class SeriesCreate(SeriesBase):
    """Schema for creating a new Series."""
    pass


class SeriesUpdate(BaseModel):
    """Schema for updating a Series (all fields optional)."""
    rabbi_id: Optional[int] = None
    name_hebrew: Optional[str] = Field(None, min_length=1, max_length=255)
    name_english: Optional[str] = Field(None, min_length=1, max_length=255)
    description_hebrew: Optional[str] = None
    description_english: Optional[str] = None
    website_url: Optional[str] = Field(None, max_length=500)
    type: Optional[str] = Field(None, min_length=1, max_length=100)


class SeriesResponse(SeriesBase):
    """Schema for Series responses."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
