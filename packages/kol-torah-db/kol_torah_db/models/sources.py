"""SQLAlchemy models for the sources schema."""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from kol_torah_db.database import Base


class YoutubePlaylist(Base):
    """YouTube Playlist model - tracks YouTube playlists for ingestion."""
    
    __tablename__ = "youtube_playlists"
    __table_args__ = {"schema": "sources"}
    
    id = Column(Integer, primary_key=True, index=True)
    playlist_id = Column(String(255), nullable=False, unique=True, index=True)
    series_id = Column(Integer, ForeignKey("main.series.id"), nullable=False, index=True)
    filter_regex = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    series = relationship("Series", foreign_keys=[series_id])
    videos = relationship("YoutubeVideo", back_populates="playlist")
    
    def __repr__(self):
        return f"<YoutubePlaylist(id={self.id}, playlist_id='{self.playlist_id}', series_id={self.series_id})>"


class YoutubeVideo(Base):
    """YouTube Video model - tracks individual YouTube videos."""
    
    __tablename__ = "youtube_videos"
    __table_args__ = {"schema": "sources"}
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String(255), nullable=False, unique=True, index=True)
    playlist_id = Column(Integer, ForeignKey("sources.youtube_playlists.id"), nullable=False, index=True)
    series_id = Column(Integer, ForeignKey("main.series.id"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    publish_date = Column(Date, nullable=False)
    bucket = Column(String(255), nullable=True)
    path = Column(String(1000), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    playlist = relationship("YoutubePlaylist", back_populates="videos")
    series = relationship("Series", foreign_keys=[series_id])
    
    def __repr__(self):
        return f"<YoutubeVideo(id={self.id}, video_id='{self.video_id}', title='{self.title}')>"
