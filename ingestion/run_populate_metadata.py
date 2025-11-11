"""Run the video metadata population script."""

import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipelines.youtube.populate_video_metadata import main

if __name__ == "__main__":
    main()
