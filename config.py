from pathlib import Path

# Set the path to your unsorted folder here
UNSORTED_FOLDER = Path("E:/media")

# Output folder structure (relative to the unsorted folder)
CATEGORIES = {
    "movies": "movies",
    "series": "series",
    "books": "books",
    "audiobooks": "audiobooks",
    "videogames": "videogames",
    "software": "software",
    "courses": "courses"
}

# Supported video file extensions
VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv"]

# Dry-run mode: If True, no actual file/folder changes will be made
DRY_RUN = True
