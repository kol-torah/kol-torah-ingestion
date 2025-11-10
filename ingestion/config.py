"""Configuration management for Kol Torah ingestion pipelines.

This module centralizes all configuration, separating:
- Secrets (from .env file): API keys, credentials
- Non-secret config: Log levels, batch sizes, bucket names, etc.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

__all__ = [
    # Secret getters
    "get_database_url",
    "get_youtube_api_key",
    "get_aws_access_key_id",
    "get_aws_secret_access_key",
    # Non-secret configuration
    "AWS_REGION",
    "S3_BUCKET_NAME",
    "LOG_LEVEL",
    "BATCH_SIZE",
]


# ============================================================================
# SECRETS (from .env file)
# ============================================================================

def get_database_url() -> str:
    """Get database connection URL."""
    url = os.getenv("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL environment variable is required")
    return url


def get_youtube_api_key() -> str:
    """Get YouTube Data API key."""
    key = os.getenv("YOUTUBE_API_KEY")
    if not key:
        raise ValueError("YOUTUBE_API_KEY environment variable is required")
    return key


def get_aws_access_key_id() -> str:
    """Get AWS access key ID."""
    key = os.getenv("AWS_ACCESS_KEY_ID")
    if not key:
        raise ValueError("AWS_ACCESS_KEY_ID environment variable is required")
    return key


def get_aws_secret_access_key() -> str:
    """Get AWS secret access key."""
    key = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not key:
        raise ValueError("AWS_SECRET_ACCESS_KEY environment variable is required")
    return key


# ============================================================================
# NON-SECRET CONFIGURATION
# ============================================================================

# AWS Configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "kol-torah-media")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Pipeline Configuration
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "100"))
