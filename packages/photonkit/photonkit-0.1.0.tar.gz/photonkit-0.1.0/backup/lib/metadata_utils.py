# backup/lib/metadata_utils.py
# Metadata utilities: camera model, timestamp, exiftool

import subprocess
import datetime
import re
from pathlib import Path

EXIFTOOL_TIMEOUT = 5
MAX_CAMERA_NAME_LEN = 32

def normalize_camera_name(name: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()
    return name[:MAX_CAMERA_NAME_LEN] if name else "camera-default"

def extract_camera_model(path: Path) -> str:
    try:
        result = subprocess.run(
            ["exiftool", "-Model", str(path)],
            capture_output=True, text=True, timeout=EXIFTOOL_TIMEOUT
        )
        for line in result.stdout.splitlines():
            if "Model" in line:
                _, value = line.split(":", 1)
                return normalize_camera_name(value.strip())
    except Exception:
        pass
    return "camera-default"

def extract_date_taken(path: Path) -> tuple[str, str]:
    try:
        timestamp = path.stat().st_mtime
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y"), dt.strftime("%Y-%m-%d")
    except Exception:
        return "unknown", "unknown-date"

def ensure_exiftool():
    try:
        subprocess.run(["exiftool", "-ver"], capture_output=True, check=True)
    except Exception:
        raise EnvironmentError("ExifTool not found. Install via `brew install exiftool`.")
