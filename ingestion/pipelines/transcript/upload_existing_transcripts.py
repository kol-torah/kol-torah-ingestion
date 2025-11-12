"""Upload existing transcripts from local directory to S3."""

import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import boto3
from botocore.exceptions import ClientError

import config
from kol_torah_db.models import YoutubeVideo, Series, Rabbi
from pipelines.utils import get_db_session

logger = logging.getLogger(__name__)


class TranscriptUploader:
    """Uploads existing transcript files to S3 and updates database."""
    
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
    
    def _generate_transcript_s3_path(self, audio_path: str) -> str:
        """Generate S3 path for transcript based on audio path.
        
        Args:
            audio_path: S3 path of the audio file (e.g., rabbi/series/2024-01-01-videoid.mp3)
            
        Returns:
            S3 path for transcript (e.g., rabbi/series/2024-01-01-videoid.json)
        """
        # Replace .mp3 extension with .json
        return audio_path.rsplit('.', 1)[0] + '.json'
    
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
    
    def _validate_transcript_file(self, file_path: Path) -> bool:
        """Validate that the transcript file is valid JSON.
        
        Args:
            file_path: Path to transcript file
            
        Returns:
            True if valid, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            return True
        except (json.JSONDecodeError, Exception) as e:
            logger.warning(f"Invalid transcript file {file_path}: {e}")
            return False
    
    def _upload_to_s3(self, local_path: Path, s3_path: str) -> None:
        """Upload file to S3 with progress indication.
        
        Args:
            local_path: Local file path
            s3_path: S3 destination path
        """
        file_size = local_path.stat().st_size
        logger.info(f"Uploading to s3://{self.s3_bucket}/{s3_path} ({file_size / 1024:.2f} KB)")
        
        # Upload with progress callback
        self.s3_client.upload_file(
            str(local_path),
            self.s3_bucket,
            s3_path,
            ExtraArgs={'ContentType': 'application/json'},
            Callback=lambda bytes_transferred: print(
                f"\rUploading to S3: {(bytes_transferred / file_size) * 100:.1f}%",
                end='',
                flush=True
            ) if file_size > 0 else None
        )
        print()  # New line after upload completes
        logger.info(f"Successfully uploaded to S3")
    
    def upload_from_directory(self, transcript_dir: str) -> Dict[str, int]:
        """Upload all transcripts from a directory.
        
        Args:
            transcript_dir: Directory containing transcript JSON files named <video-id>.json
            
        Returns:
            Dictionary with processing statistics
        """
        transcript_path = Path(transcript_dir)
        
        if not transcript_path.exists() or not transcript_path.is_dir():
            raise ValueError(f"Directory does not exist: {transcript_dir}")
        
        logger.info(f"Scanning directory: {transcript_dir}")
        
        # Find all JSON files
        transcript_files = list(transcript_path.glob("*.json"))
        total = len(transcript_files)
        
        logger.info(f"Found {total} transcript files")
        
        if total == 0:
            return {"total": 0, "uploaded": 0, "skipped": 0, "failed": 0}
        
        # Load all videos without transcripts from database (single query)
        logger.info("Loading videos without transcripts from database...")
        with get_db_session() as session:
            videos = session.query(YoutubeVideo).filter(
                YoutubeVideo.transcript_path.is_(None)
            ).all()
            
            # Create a mapping of video_id to (db_id, audio_path)
            video_map = {
                str(v.video_id): (int(v.id), str(v.path) if v.path else None)  # type: ignore
                for v in videos
            }
        
        logger.info(f"Found {len(video_map)} videos in database without transcripts")
        
        uploaded = 0
        skipped = 0
        failed = 0
        
        for idx, transcript_file in enumerate(transcript_files, 1):
            # Extract video ID from filename
            video_id = transcript_file.stem  # filename without extension
            
            logger.info(f"\n[{idx}/{total}] Processing transcript for video {video_id}")
            
            # Check if video exists in our map
            if video_id not in video_map:
                logger.info(f"Video {video_id} not found in database or already has transcript, skipping")
                skipped += 1
                continue
            
            video_db_id, audio_path = video_map[video_id]
            
            # Check if video has audio path
            if not audio_path:
                logger.warning(f"Video {video_id} has no audio path in database, skipping")
                skipped += 1
                continue
            
            # Validate transcript file
            if not self._validate_transcript_file(transcript_file):
                logger.error(f"Invalid transcript file for video {video_id}")
                failed += 1
                continue
            
            # Generate transcript S3 path based on audio path
            transcript_s3_path = self._generate_transcript_s3_path(audio_path)
            
            # Upload to S3
            try:
                logger.info(f"Processing transcript for video: {video_id}")
                self._upload_to_s3(transcript_file, transcript_s3_path)
                
                # Update database
                with get_db_session() as session:
                    video = session.query(YoutubeVideo).filter(
                        YoutubeVideo.id == video_db_id
                    ).first()
                    if video:
                        video.transcript_bucket = self.s3_bucket  # type: ignore
                        video.transcript_path = transcript_s3_path  # type: ignore
                        logger.info(f"Updated database record for video {video_id}")
                
                uploaded += 1
                
            except Exception as e:
                logger.error(f"Failed to upload transcript for video {video_id}: {e}")
                failed += 1
        
        stats = {
            "total": total,
            "uploaded": uploaded,
            "skipped": skipped,
            "failed": failed
        }
        
        logger.info(f"\nProcessing complete: {stats}")
        return stats


def main(transcript_dir: str):
    """Main entry point for the script.
    
    Args:
        transcript_dir: Directory containing transcript JSON files
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    uploader = TranscriptUploader()
    stats = uploader.upload_from_directory(transcript_dir)
    
    logger.info("\n" + "="*50)
    logger.info("SUMMARY")
    logger.info("="*50)
    logger.info(f"Total transcript files: {stats['total']}")
    logger.info(f"Uploaded: {stats['uploaded']}")
    logger.info(f"Skipped: {stats['skipped']}")
    logger.info(f"Failed: {stats['failed']}")
    logger.info("="*50)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python upload_existing_transcripts.py <transcript_directory>")
        sys.exit(1)
    
    main(sys.argv[1])
