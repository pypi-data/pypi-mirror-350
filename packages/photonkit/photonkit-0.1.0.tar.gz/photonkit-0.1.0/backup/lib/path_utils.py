# backup/lib/path_utils.py
# Path handling utilities for deduplication and safe write

from pathlib import Path

def get_target_path(base_path: Path, skip_dupe: bool) -> Path | None:
    if not base_path.exists():
        return base_path
    if skip_dupe:
        return None
    stem = base_path.stem
    suffix = base_path.suffix
    for i in range(1, 1000):
        new_path = base_path.parent / f"{stem}-{i}{suffix}"
        if not new_path.exists():
            return new_path
    raise RuntimeError(f"Too many duplicates for: {base_path}")
