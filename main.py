import shutil
import csv
from datetime import datetime
from pathlib import Path

from config import UNSORTED_FOLDER, CATEGORIES, VIDEO_EXTENSIONS, DRY_RUN
from utils import guess_category_from_name, parse_name_year_fallback
from metadata import get_movie_or_series_metadata, get_book_metadata

LOG_FILE = UNSORTED_FOLDER / "media_sort_log.txt"

def create_output_folders(base_path):
    for folder in CATEGORIES.values():
        path = base_path / folder
        if not path.exists():
            if not DRY_RUN:
                path.mkdir(parents=True, exist_ok=True)
            print(f"[CREATE] {path}")
        else:
            print(f"[EXISTS] {path}")

def scan_unsorted_folder(base_path):
    folders = []
    loose_files = []
    for item in base_path.iterdir():
        if item.is_dir():
            folders.append(item)
        elif item.is_file() and item.suffix.lower() in VIDEO_EXTENSIONS:
            loose_files.append(item)
    print(f"Found {len(folders)} folders and {len(loose_files)} loose media files.")
    return folders, loose_files

def wrap_loose_video_file(file_path, category_guess="movies"):
    base_name = file_path.stem
    target_folder_name = base_name.strip()
    target_folder = file_path.parent / target_folder_name
    if not target_folder.exists():
        print(f"[CREATE FOLDER] {target_folder}")
        if not DRY_RUN:
            target_folder.mkdir()
    new_file_path = target_folder / file_path.name
    print(f"[MOVE FILE] {file_path.name} → {target_folder.name}/")
    if not DRY_RUN:
        shutil.move(str(file_path), str(new_file_path))
    return target_folder, category_guess

def get_final_name_and_category(folder):
    name_guess = folder.name

    # Heuristic category guess first
    guess_category = guess_category_from_name(name_guess)

    # Books and audiobooks: try Google Books first
    if guess_category in ("books", "audiobooks"):
        book_meta = get_book_metadata(name_guess)
        if book_meta:
            return book_meta["name"], guess_category

    # Movies/series: try IMDb
    movie_meta = get_movie_or_series_metadata(name_guess)
    if movie_meta:
        return movie_meta["name"], movie_meta["category"]

    # Fallback
    fallback_name = parse_name_year_fallback(name_guess)
    print(f"[FALLBACK] {name_guess} → {fallback_name} ({guess_category})")
    return fallback_name, guess_category or "movies"

def resolve_name_conflict(target_base, name):
    target_path = target_base / name
    if not target_path.exists():
        return target_path
    i = 1
    while True:
        new_name = f"{name} [{i}]"
        target_path = target_base / new_name
        if not target_path.exists():
            return target_path
        i += 1

def log_action(original_path: Path, new_path: Path):
    with open(LOG_FILE, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), str(original_path), str(new_path)])

def undo_last_sort():
    if not LOG_FILE.exists():
        print("[UNDO] No log file found.")
        return
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if not lines:
        print("[UNDO] Log is empty.")
        return
    for line in reversed(lines):
        try:
            _, original_path, new_path = line.strip().split(",", 2)
            src = Path(new_path.strip())
            dst = Path(original_path.strip())
            if not src.exists():
                print(f"[UNDO] Skipping missing: {src}")
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            print(f"[UNDO] Moving back: {src} → {dst}")
            if not DRY_RUN:
                shutil.move(str(src), str(dst))
        except Exception as e:
            print(f"[UNDO ERROR] {line.strip()} → {e}")
    print("[UNDO] Done.")
    if not DRY_RUN:
        LOG_FILE.unlink()

def run_sort():
    print(f"[SCAN ROOT] {UNSORTED_FOLDER}")
    create_output_folders(UNSORTED_FOLDER)
    folders, loose_files = scan_unsorted_folder(UNSORTED_FOLDER)

    for file in loose_files:
        guess = guess_category_from_name(file.name)
        wrapped_folder, guess = wrap_loose_video_file(file, category_guess=guess or "movies")
        folders.append(wrapped_folder)

    for folder in folders:
        clean_name, category = get_final_name_and_category(folder)
        category_folder = CATEGORIES.get(category, "uncategorized")
        target_base = UNSORTED_FOLDER / category_folder
        final_target = resolve_name_conflict(target_base, clean_name)
        print(f"[RENAME + MOVE] {folder.name} → {final_target}")
        if not DRY_RUN:
            shutil.move(str(folder), str(final_target))
            log_action(folder, final_target)

if __name__ == "__main__":
    # === SELECT ONE MODE BELOW ===

    # To run sorting:
    run_sort()

    # To undo last run instead:
    # undo_last_sort()
