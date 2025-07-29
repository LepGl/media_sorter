import re

def guess_category_from_name(name):
    name_lower = name.lower()

    if any(x in name_lower for x in ["s0", "season", "ep", "complete", "episode"]):
        return "series"
    elif any(x in name_lower for x in ["audiobook", "audio book", "audible"]):
        return "audiobooks"
    elif any(x in name_lower for x in ["book", ".epub", ".pdf", "volume", "edition"]):
        return "books"
    elif any(x in name_lower for x in ["course", "tutorial", "udemy", "guide"]):
        return "courses"
    elif any(x in name_lower for x in ["setup", "installer", "crack", "license", "pro", "win64"]):
        return "software"
    elif any(x in name_lower for x in ["game", "fitgirl", "codex", "gog", "repack"]):
        return "videogames"
    elif re.search(r"\b\d{4}\b", name_lower):
        return "movies"

    return None

def parse_name_year_fallback(name):
    # Remove brackets and extra tags
    cleaned = re.sub(r"[\[\(].*?[\]\)]", "", name)
    cleaned = re.sub(r"[\._\-]+", " ", cleaned).strip()

    # Extract year
    match = re.search(r"(.*?)(\b19\d{2}|\b20\d{2})", cleaned)
    if match:
        title = match.group(1).strip()
        year = match.group(2)
        return f"{title} ({year})"
    else:
        return cleaned
