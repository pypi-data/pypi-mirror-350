# backup/lib/file_utils.py
# File classification and filtering helpers, now includes HEIC files

from pathlib import Path

FILE_TYPES = {
    "jpg": [".jpg", ".jpeg", ".heic"],  # 📌 added .heic as part of jpg family
    "raw": [".cr2", ".cr3", ".nef", ".arw"],
    "video": [".mov", ".mp4", ".avi"],
}

def get_file_type(extension: str) -> str | None:
    ext = extension.lower()
    for category, exts in FILE_TYPES.items():
        if ext in exts:
            return category
    return None

def is_hidden_or_system_file(path: Path) -> bool:
    return path.name.startswith('.') or path.name.startswith('._')
