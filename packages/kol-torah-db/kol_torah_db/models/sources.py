"""SQLAlchemy models for the sources schema."""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from kol_torah_db.database import Base


class YoutubeVideo(Base):
    """YouTube Video model - tracks individual YouTube videos."""
    
    __tablename__ = "youtube_videos"
    __table_args__ = {"schema": "sources"}
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String(255), nullable=False, unique=True, index=True)
    series_id = Column(Integer, ForeignKey("main.series.id"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    publish_date = Column(Date, nullable=False)
    url = Column(String(500), nullable=False)
    duration = Column(Integer, nullable=False)
    bucket = Column(String(255), nullable=True)
    path = Column(String(1000), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    series = relationship("Series", foreign_keys=[series_id])
    
    def __repr__(self):
        return f"<YoutubeVideo(id={self.id}, video_id='{self.video_id}', title='{self.title}')>"
