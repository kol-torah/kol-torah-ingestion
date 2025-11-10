# Kol Torah Ingestion Pipelines

Python-based data ingestion pipelines for processing Torah lessons from various sources.

## Overview

This project contains CLI-driven ingestion pipelines for:
- **YouTube Videos**: Fetch video metadata from YouTube channels/playlists
- **Audio Processing**: Download and upload audio to S3 (coming soon)
- **Transcription**: Transcribe Hebrew audio using RunPods (coming soon)

## Installation

1. Install dependencies:
```bash
poetry install
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your credentials:
# - DATABASE_URL: PostgreSQL connection string
# - YOUTUBE_API_KEY: YouTube Data API v3 key
# - AWS credentials and S3 bucket (for audio processing)
```

## Usage

### CLI Commands

The ingestion system is controlled via `cli.py`:

```bash
# Activate virtual environment
.\env\Scripts\Activate.ps1

# Run CLI (shows all available commands)
python cli.py --help

# YouTube commands
python cli.py youtube --help
```

### Fetch YouTube Videos

**From a playlist:**
```bash
python cli.py youtube fetch-playlist \
  --playlist-id PLxxxxxxxxxxxxxx \
  --series-id 1
```

**From a channel (all uploads):**
```bash
python cli.py youtube fetch-channel \
  --channel-id UCxxxxxxxxxxxxxx \
  --series-id 1
```

**Limit results:**
```bash
python cli.py youtube fetch-playlist \
  --playlist-id PLxxxxxxxxxxxxxx \
  --series-id 1 \
  --max-results 50
```

### How It Works

1. **fetch-playlist/fetch-channel**: Fetches video metadata from YouTube API
2. Videos are stored in `sources.youtube_videos` table
3. Duplicate videos (by video_id) are automatically skipped
4. Links videos to the specified series

## Project Structure

```
ingestion/
├── cli.py                    # Main CLI entry point
├── pipelines/
│   ├── utils.py             # Shared utilities (DB connections)
│   └── youtube/
│       ├── __init__.py
│       └── fetch_videos.py  # YouTube video fetching logic
├── .env.example             # Environment template
└── pyproject.toml          # Dependencies
```

## Development

The project uses:
- **Click**: CLI framework
- **SQLAlchemy**: Database ORM (via kol-torah-db package)
- **google-api-python-client**: YouTube Data API
- **boto3**: AWS S3 (for audio storage)
- **python-dotenv**: Environment configuration

## Next Steps

Additional pipeline stages to be implemented:
- Audio download from YouTube videos
- S3 upload for audio files
- Transcription using RunPods
- Post-processing and content extraction

