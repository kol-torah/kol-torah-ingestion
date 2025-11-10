"""CLI entry point for Kol Torah ingestion pipelines."""

import click
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(
    level=getattr(logging, log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@click.group()
def cli():
    """Kol Torah Ingestion Pipelines - CLI tool for managing data ingestion."""
    pass


@cli.group()
def youtube():
    """YouTube-related ingestion commands."""
    pass


@youtube.command("fetch-playlist")
@click.option("--playlist-id", required=True, help="YouTube playlist ID")
@click.option("--series-id", required=True, type=int, help="Database series ID")
@click.option("--max-results", type=int, default=None, help="Maximum number of videos to fetch")
def fetch_playlist(playlist_id: str, series_id: int, max_results: int):
    """Fetch videos from a YouTube playlist and store in database."""
    from pipelines.youtube.fetch_videos import fetch_and_store_playlist
    
    click.echo(f"Fetching videos from playlist: {playlist_id}")
    click.echo(f"Target series ID: {series_id}")
    
    try:
        added_count = fetch_and_store_playlist(playlist_id, series_id, max_results)
        click.echo(f"✓ Successfully added {added_count} new videos")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@youtube.command("fetch-channel")
@click.option("--channel-id", required=True, help="YouTube channel ID")
@click.option("--series-id", required=True, type=int, help="Database series ID")
@click.option("--max-results", type=int, default=None, help="Maximum number of videos to fetch")
def fetch_channel(channel_id: str, series_id: int, max_results: int):
    """Fetch videos from a YouTube channel and store in database."""
    from pipelines.youtube.fetch_videos import fetch_and_store_channel
    
    click.echo(f"Fetching videos from channel: {channel_id}")
    click.echo(f"Target series ID: {series_id}")
    
    try:
        added_count = fetch_and_store_channel(channel_id, series_id, max_results)
        click.echo(f"✓ Successfully added {added_count} new videos")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@youtube.command("fetch-butbul-daily-halacha")
@click.option("--rabbi-slug", default="butbul", help="Rabbi slug (default: butbul)")
@click.option("--series-slug", default="daily-halacha", help="Series slug (default: daily-halacha)")
@click.option("--max-duration", type=float, default=10.0, help="Maximum video duration in minutes (default: 10)")
def fetch_butbul_daily_halacha(rabbi_slug: str, series_slug: str, max_duration: float):
    """Fetch videos for Butbul Daily Halacha series."""
    from pipelines.youtube.fetch_youtube_videos import YouTubeVideoFetcher
    from pipelines.utils import get_db_session
    from kol_torah_db.models import Rabbi, Series
    
    click.echo(f"Looking up series: rabbi='{rabbi_slug}', series='{series_slug}'")
    
    # Look up series ID from database
    try:
        with get_db_session() as session:
            series = session.query(Series).join(Rabbi).filter(
                Rabbi.slug == rabbi_slug,
                Series.slug == series_slug
            ).first()
            
            if not series:
                click.echo(f"✗ Error: Series not found for rabbi '{rabbi_slug}' and series '{series_slug}'", err=True)
                raise click.Abort()
            
            # Extract values while session is active
            series_id: int = series.id  # type: ignore
            series_name: str = series.name_english  # type: ignore
            
        click.echo(f"Found series: {series_name} (ID: {series_id})")
    except Exception as e:
        click.echo(f"✗ Database error: {e}", err=True)
        raise click.Abort()
    
    click.echo(f"Fetching Butbul Daily Halacha videos (max duration: {max_duration} min)")
    
    try:
        fetcher = YouTubeVideoFetcher()
        added_count = fetcher.fetch_butbul_halacha_yomit(series_id, max_duration)
        click.echo(f"✓ Successfully added {added_count} new videos")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


@youtube.command("fetch-halichot-olam")
@click.option("--rabbi-slug", default="butbul", help="Rabbi slug (default: butbul)")
@click.option("--series-slug", default="halichot-olam", help="Series slug (default: halichot-olam)")
def fetch_halichot_olam(rabbi_slug: str, series_slug: str):
    """Fetch videos for Halichot Olam series."""
    from pipelines.youtube.fetch_youtube_videos import YouTubeVideoFetcher
    from pipelines.utils import get_db_session
    from kol_torah_db.models import Rabbi, Series
    
    click.echo(f"Looking up series: rabbi='{rabbi_slug}', series='{series_slug}'")
    
    # Look up series ID from database
    try:
        with get_db_session() as session:
            series = session.query(Series).join(Rabbi).filter(
                Rabbi.slug == rabbi_slug,
                Series.slug == series_slug
            ).first()
            
            if not series:
                click.echo(f"✗ Error: Series not found for rabbi '{rabbi_slug}' and series '{series_slug}'", err=True)
                raise click.Abort()
            
            # Extract values while session is active
            series_id: int = series.id  # type: ignore
            series_name: str = series.name_english  # type: ignore
            
        click.echo(f"Found series: {series_name} (ID: {series_id})")
    except Exception as e:
        click.echo(f"✗ Database error: {e}", err=True)
        raise click.Abort()
    
    click.echo(f"Fetching Halichot Olam videos")
    
    try:
        fetcher = YouTubeVideoFetcher()
        added_count = fetcher.fetch_halichot_olam(series_id)
        click.echo(f"✓ Successfully added {added_count} new videos")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    cli()
