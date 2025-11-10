"""Fetch YouTube videos for specific series and store them in the database."""

import os
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from isodate import parse_duration

from kol_torah_db.models import YoutubeVideo, Series
from pipelines.utils import get_db_session

logger = logging.getLogger(__name__)


class YouTubeVideoFetcher:
    """Fetches videos from YouTube API and stores them in database."""
    
    # Series-specific channel configurations
    BUTBUL_HALACHA_YOMIT_CHANNEL_ID = "UCS9moGQA0U4MqWzT98mIlGw"
    BUTBUL_HALACHA_YOMIT_PLAYLIST_KEYWORD = "הלכה יומית"
    
    HALICHOT_OLAM_PLAYLIST_ID = "PLPPy6SF11zD8YIS1hqdscDdDPjWcICPPc"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize YouTube API client.
        
        Args:
            api_key: YouTube Data API key. If not provided, will use YOUTUBE_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YouTube API key is required. Set YOUTUBE_API_KEY environment variable.")
        
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
    
    def _get_channel_playlists(self, channel_id: str) -> List[Dict[str, Any]]:
        """Get all playlists for a channel.
        
        Args:
            channel_id: YouTube channel ID
            
        Returns:
            List of playlist metadata dictionaries
        """
        playlists = []
        next_page_token = None
        
        try:
            while True:
                request = self.youtube.playlists().list(
                    part="snippet",
                    channelId=channel_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()
                
                for item in response.get("items", []):
                    playlists.append({
                        "id": item["id"],
                        "title": item["snippet"]["title"],
                        "description": item["snippet"].get("description", "")
                    })
                
                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break
            
            logger.info(f"Found {len(playlists)} playlists in channel {channel_id}")
            return playlists
            
        except HttpError as e:
            logger.error(f"YouTube API error fetching playlists: {e}")
            raise
    
    def _get_playlist_videos(self, playlist_id: str) -> List[str]:
        """Get all video IDs from a playlist.
        
        Args:
            playlist_id: YouTube playlist ID
            
        Returns:
            List of video IDs
        """
        video_ids = []
        next_page_token = None
        
        try:
            while True:
                request = self.youtube.playlistItems().list(
                    part="contentDetails",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()
                
                for item in response.get("items", []):
                    video_id = item["contentDetails"]["videoId"]
                    video_ids.append(video_id)
                
                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break
            
            logger.info(f"Found {len(video_ids)} videos in playlist {playlist_id}")
            return video_ids
            
        except HttpError as e:
            logger.error(f"YouTube API error fetching playlist videos: {e}")
            raise
    
    def _get_video_details(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        """Get detailed information for a list of videos.
        
        Args:
            video_ids: List of YouTube video IDs
            
        Returns:
            List of video metadata dictionaries
        """
        videos = []
        
        # YouTube API allows max 50 IDs per request
        for i in range(0, len(video_ids), 50):
            batch_ids = video_ids[i:i+50]
            
            try:
                request = self.youtube.videos().list(
                    part="snippet,contentDetails",
                    id=",".join(batch_ids)
                )
                response = request.execute()
                
                for item in response.get("items", []):
                    snippet = item["snippet"]
                    content_details = item["contentDetails"]
                    
                    # Parse duration
                    duration = parse_duration(content_details["duration"])
                    duration_minutes = duration.total_seconds() / 60
                    
                    videos.append({
                        "video_id": item["id"],
                        "title": snippet["title"],
                        "description": snippet.get("description", ""),
                        "publish_date": datetime.strptime(
                            snippet["publishedAt"],
                            "%Y-%m-%dT%H:%M:%SZ"
                        ).date(),
                        "duration_minutes": duration_minutes
                    })
                
            except HttpError as e:
                logger.error(f"YouTube API error fetching video details: {e}")
                raise
        
        return videos
    
    def _filter_existing_videos(self, video_ids: List[str]) -> List[str]:
        """Filter out video IDs that already exist in the database.
        
        Args:
            video_ids: List of YouTube video IDs
            
        Returns:
            List of video IDs not in database
        """
        with get_db_session() as session:
            existing_video_ids = set(
                row[0] for row in session.query(YoutubeVideo.video_id)
                .filter(YoutubeVideo.video_id.in_(video_ids))
                .all()
            )
            
            new_video_ids = [vid for vid in video_ids if vid not in existing_video_ids]
            
            logger.info(f"Filtered: {len(video_ids)} total, {len(existing_video_ids)} existing, {len(new_video_ids)} new")
            return new_video_ids
    
    def fetch_butbul_halacha_yomit(self, series_id: int, max_duration_minutes: float = 10.0) -> int:
        """Fetch videos for Butbul Halacha Yomit series.
        
        Args:
            series_id: Database ID for the Butbul Halacha Yomit series
            max_duration_minutes: Maximum video duration in minutes (default: 10)
            
        Returns:
            Number of new videos added to database
        """
        logger.info("Starting fetch for Butbul Halacha Yomit series")
        
        # Get all playlists from the channel
        all_playlists = self._get_channel_playlists(self.BUTBUL_HALACHA_YOMIT_CHANNEL_ID)
        
        # Filter playlists by keyword
        matching_playlists = [
            p for p in all_playlists 
            if self.BUTBUL_HALACHA_YOMIT_PLAYLIST_KEYWORD in p["title"]
        ]
        
        logger.info(f"Found {len(matching_playlists)} playlists matching '{self.BUTBUL_HALACHA_YOMIT_PLAYLIST_KEYWORD}'")
        
        # Collect all video IDs from matching playlists
        all_video_ids = []
        for playlist in matching_playlists:
            logger.info(f"Processing playlist: {playlist['title']}")
            video_ids = self._get_playlist_videos(playlist["id"])
            all_video_ids.extend(video_ids)
        
        # Remove duplicates
        all_video_ids = list(set(all_video_ids))
        logger.info(f"Total unique videos found: {len(all_video_ids)}")
        
        # Filter out videos already in database
        new_video_ids = self._filter_existing_videos(all_video_ids)
        
        if not new_video_ids:
            logger.info("No new videos to add")
            return 0
        
        # Get detailed information for new videos
        video_details = self._get_video_details(new_video_ids)
        
        # Filter by duration and save to database
        added_count = 0
        skipped_duration_count = 0
        
        with get_db_session() as session:
            # Verify series exists
            series = session.query(Series).filter(Series.id == series_id).first()
            if not series:
                raise ValueError(f"Series with id {series_id} not found")
            
            for video in video_details:
                if video["duration_minutes"] > max_duration_minutes:
                    logger.debug(
                        f"Skipping video {video['video_id']} - duration {video['duration_minutes']:.1f} min exceeds {max_duration_minutes} min"
                    )
                    skipped_duration_count += 1
                    continue
                
                new_video = YoutubeVideo(
                    video_id=video["video_id"],
                    series_id=series_id,
                    title=video["title"],
                    description=video["description"],
                    publish_date=video["publish_date"]
                )
                session.add(new_video)
                added_count += 1
                logger.info(
                    f"Added video: {video['video_id']} - {video['title']} ({video['duration_minutes']:.1f} min)"
                )
        
        logger.info(
            f"Processing complete: {added_count} videos added, "
            f"{skipped_duration_count} skipped (too long)"
        )
        return added_count
    
    def fetch_halichot_olam(self, series_id: int) -> int:
        """Fetch videos for Halichot Olam series.
        
        Args:
            series_id: Database ID for the Halichot Olam series
            
        Returns:
            Number of new videos added to database
        """
        logger.info("Starting fetch for Halichot Olam series")
        
        # Get all video IDs from the playlist
        all_video_ids = self._get_playlist_videos(self.HALICHOT_OLAM_PLAYLIST_ID)
        
        logger.info(f"Total videos found in playlist: {len(all_video_ids)}")
        
        # Filter out videos already in database
        new_video_ids = self._filter_existing_videos(all_video_ids)
        
        if not new_video_ids:
            logger.info("No new videos to add")
            return 0
        
        # Get detailed information for new videos
        video_details = self._get_video_details(new_video_ids)
        
        # Save to database (no duration filter for Halichot Olam)
        added_count = 0
        
        with get_db_session() as session:
            # Verify series exists
            series = session.query(Series).filter(Series.id == series_id).first()
            if not series:
                raise ValueError(f"Series with id {series_id} not found")
            
            for video in video_details:
                new_video = YoutubeVideo(
                    video_id=video["video_id"],
                    series_id=series_id,
                    title=video["title"],
                    description=video["description"],
                    publish_date=video["publish_date"]
                )
                session.add(new_video)
                added_count += 1
                logger.info(
                    f"Added video: {video['video_id']} - {video['title']} ({video['duration_minutes']:.1f} min)"
                )
        
        logger.info(f"Processing complete: {added_count} videos added")
        return added_count
