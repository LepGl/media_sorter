import re
from pathlib import Path
from config import VIDEO_EXTENSIONS

def guess_category_from_name(name: str):
    lowered = name.lower()

    # Keywords in folder name
    if any(keyword in lowered for keyword in ["epub", "pdf", "book", "edition"]):
        return "books"
    if any(keyword in lowered for keyword in ["audiobook", "m4b", "audible", "narrated"]):
        return "audiobooks"
    if any(keyword in lowered for keyword in ["fitgirl", "gog", "codex", "repack"]):
        return "videogames"
    if any(keyword in lowered for keyword in ["s0", "e0", "season", "episode"]):
        return "series"
    if any(keyword in lowered for keyword in ["course", "tutorial", "lesson"]):
        return "courses"
    if any(keyword in lowered for keyword in ["pro", "setup", "x64", "software", "installer"]):
        return "software"
    if any(keyword in lowered for keyword in ["bluray", "webdl", "hdrip", "x265", "x264", "1080p", "720p"]):
        return "movies"

    return None  # fallback if name doesn't suggest anything

def guess_category_from_contents(folder: Path):
    if not folder.is_dir():
        return None

    extensions = set()
    for file in folder.rglob("*"):
        if file.is_file():
            extensions.add(file.suffix.lower())

    # Extension-based logic
    if any(ext in extensions for ext in [".epub", ".pdf"]):
        return "books"
    if any(ext in extensions for ext in [".m4b", ".mp3", ".flac"]):
        return "audiobooks"
    if any(ext in extensions for ext in VIDEO_EXTENSIONS):
        return "movies"
    if any(ext in extensions for ext in [".exe", ".dmg", ".msi", ".pkg"]):
        return "software"

    return None

def parse_name_year_fallback(name: str):
    name = Path(name).stem
    name = re.sub(r"[\\[\\]{}()_]", "", name)
    name = re.sub(r"[.\\-]", " ", name)
    name = re.sub(r"\\s+", " ", name)
    name = name.strip()
    return name
