# Media Sorter

A Python application to automatically organize and rename folders and loose files for:
- Movies
- TV Series
- Books
- Audiobooks
- Video Games
- Software
- Courses

Includes:
- Metadata scraping from IMDb and Google Books
- Dry-run mode
- Undo functionality
- Simple GUI built with Tkinter


## Requirements

- Python 3.8+
- pip install -r requirements.txt


## Usage

### CLI Mode

```bash
python main.py
```

### GUI Mode

```bash
python main.py
```
Use the GUI to:
- Select the folder to organize
- Enable or disable dry-run mode
- Sort your content
- Undo the last sort if needed

## Features
- Rename folders like Some.Movie.2012.1080p → Some Movie (2012)
- Automatically categorize files into:
    - movies/
    - series/
    - books/
    - audiobooks/
    - videogames/
    - software/
    - courses/
- Google Books and IMDb integration
- Collision-safe file/folder naming
- Logging + one-click undo
- Loose file handling (e.g., .mkv, .mp4 directly in unsorted root)