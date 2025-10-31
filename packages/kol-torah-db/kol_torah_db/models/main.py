"""SQLAlchemy models for the main schema."""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from kol_torah_db.database import Base


class Rabbi(Base):
    """Rabbi model - contains information about rabbis giving lessons."""
    
    __tablename__ = "rabbis"
    __table_args__ = {"schema": "main"}
    
    id = Column(Integer, primary_key=True, index=True)
    name_hebrew = Column(String(255), nullable=False, index=True)
    name_english = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    website_url = Column(String(500), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    series = relationship("Series", back_populates="rabbi")
    
    def __repr__(self):
        return f"<Rabbi(id={self.id}, name_english='{self.name_english}', slug='{self.slug}')>"


class Series(Base):
    """Series model - describes a series of lessons by a rabbi."""
    
    __tablename__ = "series"
    __table_args__ = {"schema": "main"}
    
    id = Column(Integer, primary_key=True, index=True)
    rabbi_id = Column(Integer, ForeignKey("main.rabbis.id"), nullable=False, index=True)
    name_hebrew = Column(String(255), nullable=False)
    name_english = Column(String(255), nullable=False)
    description_hebrew = Column(Text, nullable=True)
    description_english = Column(Text, nullable=True)
    website_url = Column(String(500), nullable=True)
    type = Column(String(100), nullable=False, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    rabbi = relationship("Rabbi", back_populates="series")
    
    def __repr__(self):
        return f"<Series(id={self.id}, name_english='{self.name_english}', type='{self.type}')>"
