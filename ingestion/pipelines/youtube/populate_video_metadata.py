"""One-time script to populate URL and duration for existing YouTube videos."""

import logging
from typing import List, Dict, Any
import yt_dlp

from kol_torah_db.models import YoutubeVideo
from pipelines.utils import get_db_session

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VideoMetadataPopulator:
    """Populates URL and duration metadata for YouTube videos."""
    
    def __init__(self):
        """Initialize the populator."""
        self.ydl_opts: Dict[str, Any] = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'skip_download': True,
        }
    
    def _fetch_video_metadata(self, video_id: str) -> Dict[str, Any]:
        """Fetch metadata for a single video from YouTube.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Dictionary with 'url' and 'duration' keys
        """
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:  # type: ignore
                info = ydl.extract_info(video_url, download=False)
                
                return {
                    'url': info.get('webpage_url', video_url),
                    'duration': info.get('duration', None)  # Duration in seconds
                }
        except Exception as e:
            logger.error(f"Failed to fetch metadata for video {video_id}: {e}")
            # Return defaults if fetch fails
            return {
                'url': video_url,
                'duration': None
            }
    
    def populate_video(self, video_id: int, youtube_video_id: str) -> bool:
        """Populate URL and duration for a single video.
        
        Args:
            video_id: Database ID of the video
            youtube_video_id: YouTube video ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Fetching metadata for video {youtube_video_id}")
            metadata = self._fetch_video_metadata(youtube_video_id)
            
            # Update database
            with get_db_session() as session:
                video = session.query(YoutubeVideo).filter(YoutubeVideo.id == video_id).first()
                if video:
                    video.url = metadata['url']
                    video.duration = metadata['duration']
                    
                    duration_str = f"{metadata['duration']}s" if metadata['duration'] else "unknown"
                    logger.info(f"Updated video {youtube_video_id}: URL={metadata['url']}, Duration={duration_str}")
                    return True
                else:
                    logger.error(f"Video {video_id} not found in database")
                    return False
                    
        except Exception as e:
            logger.error(f"Error processing video {youtube_video_id}: {e}")
            return False
    
    def populate_all_videos(self) -> Dict[str, int]:
        """Populate URL and duration for all videos missing this data.
        
        Returns:
            Dictionary with processing statistics
        """
        logger.info("Starting metadata population for all videos")
        
        # Get all videos that need metadata
        with get_db_session() as session:
            videos = session.query(YoutubeVideo).filter(
                (YoutubeVideo.url.is_(None)) | (YoutubeVideo.duration.is_(None))
            ).all()
            
            # Detach from session - convert to plain values
            video_data = [(v.id, v.video_id, v.title) for v in videos]  # type: ignore
        
        total = len(video_data)
        logger.info(f"Found {total} videos needing metadata")
        
        if total == 0:
            return {"total": 0, "successful": 0, "failed": 0}
        
        successful = 0
        failed = 0
        
        for idx, (vid_id, youtube_video_id, title) in enumerate(video_data, 1):
            logger.info(f"\n[{idx}/{total}] Processing: {title} ({youtube_video_id})")
            
            if self.populate_video(vid_id, youtube_video_id):  # type: ignore
                successful += 1
            else:
                failed += 1
        
        stats = {
            "total": total,
            "successful": successful,
            "failed": failed
        }
        
        logger.info(f"\nProcessing complete: {stats}")
        return stats


def main():
    """Main entry point for the script."""
    populator = VideoMetadataPopulator()
    stats = populator.populate_all_videos()
    
    logger.info("\n" + "="*50)
    logger.info("SUMMARY")
    logger.info("="*50)
    logger.info(f"Total videos processed: {stats['total']}")
    logger.info(f"Successful: {stats['successful']}")
    logger.info(f"Failed: {stats['failed']}")
    logger.info("="*50)


if __name__ == "__main__":
    main()
