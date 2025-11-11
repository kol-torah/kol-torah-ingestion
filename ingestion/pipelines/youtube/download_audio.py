"""Download YouTube video audio and upload to S3."""

import os
import logging
import tempfile
from pathlib import Path
from typing import Optional, List
from datetime import date
import boto3
from botocore.exceptions import ClientError
import yt_dlp

import config
from kol_torah_db.models import YoutubeVideo, Series, Rabbi
from pipelines.utils import get_db_session

logger = logging.getLogger(__name__)


class YouTubeAudioDownloader:
    """Downloads YouTube video audio and uploads to S3."""
    
    def __init__(
        self, 
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_region: Optional[str] = None,
        s3_bucket: Optional[str] = None
    ):
        """Initialize S3 client and configuration.
        
        Args:
            aws_access_key_id: AWS access key (uses config if not provided)
            aws_secret_access_key: AWS secret key (uses config if not provided)
            aws_region: AWS region (uses config if not provided)
            s3_bucket: S3 bucket name (uses config if not provided)
        """
        self.aws_access_key_id = aws_access_key_id or config.get_aws_access_key_id()
        self.aws_secret_access_key = aws_secret_access_key or config.get_aws_secret_access_key()
        self.aws_region = aws_region or config.AWS_REGION
        self.s3_bucket = s3_bucket or config.S3_BUCKET_NAME
        
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region
        )
    
    def _generate_s3_path(
        self, 
        rabbi_slug: str, 
        series_slug: str, 
        publish_date: date, 
        video_id: str
    ) -> str:
        """Generate S3 path for a video's audio file.
        
        Args:
            rabbi_slug: Rabbi slug
            series_slug: Series slug
            publish_date: Video publish date
            video_id: YouTube video ID
            
        Returns:
            S3 path in format: {rabbi-slug}/{series-slug}/{publish-date}-{video-id}.mp3
        """
        date_str = publish_date.strftime("%Y-%m-%d")
        return f"{rabbi_slug}/{series_slug}/{date_str}-{video_id}.mp3"
    
    def _check_s3_exists(self, s3_path: str) -> bool:
        """Check if a file exists in S3.
        
        Args:
            s3_path: Path in S3 bucket
            
        Returns:
            True if file exists, False otherwise
        """
        try:
            self.s3_client.head_object(Bucket=self.s3_bucket, Key=s3_path)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise
    
    def _download_audio(self, video_id: str, output_path: Path) -> None:
        """Download audio from YouTube video.
        
        Args:
            video_id: YouTube video ID
            output_path: Local path to save audio file
        """
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': str(output_path.with_suffix('')),  # yt-dlp adds .mp3
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [self._progress_hook],
        }
        
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        logger.info(f"Downloading audio from {video_url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    
    def _progress_hook(self, d):
        """Progress hook for yt-dlp."""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                print(f"\rDownloading: {percent:.1f}%", end='', flush=True)
            elif '_percent_str' in d:
                print(f"\rDownloading: {d['_percent_str']}", end='', flush=True)
        elif d['status'] == 'finished':
            print("\rDownload complete, converting to MP3...", flush=True)
    
    def _upload_to_s3(self, local_path: Path, s3_path: str) -> None:
        """Upload file to S3 with progress indication.
        
        Args:
            local_path: Local file path
            s3_path: S3 destination path
        """
        file_size = local_path.stat().st_size
        logger.info(f"Uploading to s3://{self.s3_bucket}/{s3_path} ({file_size / (1024*1024):.2f} MB)")
        
        # Upload with progress callback
        self.s3_client.upload_file(
            str(local_path),
            self.s3_bucket,
            s3_path,
            Callback=lambda bytes_transferred: print(
                f"\rUploading to S3: {(bytes_transferred / file_size) * 100:.1f}%",
                end='',
                flush=True
            )
        )
        print()  # New line after upload completes
        logger.info(f"Successfully uploaded to S3")
    
    def process_video(self, video: YoutubeVideo, rabbi_slug: str, series_slug: str) -> bool:
        """Download audio and upload to S3 for a single video.
        
        Args:
            video: YoutubeVideo database object
            rabbi_slug: Rabbi slug for S3 path
            series_slug: Series slug for S3 path
            
        Returns:
            True if processed successfully, False if skipped or failed
        """
        # Check if already uploaded
        if video.bucket and video.path:
            logger.info(f"Video {video.video_id} already uploaded to S3, skipping")
            return False
        
        # Generate S3 path
        s3_path = self._generate_s3_path(rabbi_slug, series_slug, video.publish_date, video.video_id)
        
        # Double-check S3 in case DB is out of sync
        if self._check_s3_exists(s3_path):
            logger.warning(f"File exists in S3 but not in DB, updating DB record")
            with get_db_session() as session:
                db_video = session.query(YoutubeVideo).filter(YoutubeVideo.id == video.id).first()
                if db_video:
                    db_video.bucket = self.s3_bucket
                    db_video.path = s3_path
            return False
        
        # Download and upload
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir) / f"{video.video_id}.mp3"
            
            try:
                # Download audio
                logger.info(f"Processing video: {video.title} ({video.video_id})")
                self._download_audio(video.video_id, temp_path)
                
                # Upload to S3
                self._upload_to_s3(temp_path, s3_path)
                
                # Update database
                with get_db_session() as session:
                    db_video = session.query(YoutubeVideo).filter(YoutubeVideo.id == video.id).first()
                    if db_video:
                        db_video.bucket = self.s3_bucket
                        db_video.path = s3_path
                        logger.info(f"Updated database record for video {video.video_id}")
                
                return True
                
            except Exception as e:
                logger.error(f"Error processing video {video.video_id}: {e}")
                raise
    
    def process_all_videos(self, limit: Optional[int] = None) -> dict:
        """Process all unprocessed videos across all series.
        
        Args:
            limit: Maximum number of videos to process (None for all)
            
        Returns:
            Dictionary with processing statistics
        """
        logger.info("Starting audio download for all unprocessed videos")
        
        # Get all unprocessed videos with their series information
        with get_db_session() as session:
            query = session.query(
                YoutubeVideo, 
                Series, 
                Rabbi
            ).join(
                Series, YoutubeVideo.series_id == Series.id
            ).join(
                Rabbi, Series.rabbi_id == Rabbi.id
            ).filter(
                YoutubeVideo.bucket.is_(None),
                YoutubeVideo.path.is_(None)
            ).order_by(
                Rabbi.slug, 
                Series.slug, 
                YoutubeVideo.publish_date
            )
            
            if limit:
                query = query.limit(limit)
            
            results = query.all()
            
            # Detach from session to use in processing
            video_data = [
                (
                    v.id, 
                    v.video_id, 
                    v.title, 
                    v.publish_date,
                    s.slug,  # series_slug
                    r.slug   # rabbi_slug
                ) 
                for v, s, r in results
            ]
        
        total = len(video_data)
        logger.info(f"Found {total} unprocessed videos across all series")
        
        if total == 0:
            return {"total": 0, "processed": 0, "skipped": 0, "failed": 0}
        
        processed = 0
        skipped = 0
        failed = 0
        
        for idx, (vid_id, video_id, title, publish_date, series_slug, rabbi_slug) in enumerate(video_data, 1):
            logger.info(f"\n[{idx}/{total}] Processing video {video_id} ({rabbi_slug}/{series_slug})")
            
            try:
                # Open fresh connection for each video to avoid Neon timeout
                with get_db_session() as session:
                    video = session.query(YoutubeVideo).filter(YoutubeVideo.id == vid_id).first()
                    if not video:
                        logger.error(f"Video {video_id} not found in database")
                        failed += 1
                        continue
                    
                    result = self.process_video(video, rabbi_slug, series_slug)
                    if result:
                        processed += 1
                    else:
                        skipped += 1
            except Exception as e:
                logger.error(f"Failed to process video {video_id}: {e}")
                failed += 1
        
        stats = {
            "total": total,
            "processed": processed,
            "skipped": skipped,
            "failed": failed
        }
        
        logger.info(f"\nProcessing complete: {stats}")
        return stats
