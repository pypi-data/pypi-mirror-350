# backup/photo_backup.py
# CLI entry point for Photonic: safe, structured photo backup with skip-dupe default

import argparse
import sys
from pathlib import Path
from backup.lib.file_utils import is_hidden_or_system_file, get_file_type
from backup.lib.metadata_utils import extract_camera_model, extract_date_taken, ensure_exiftool
from backup.lib.path_utils import get_target_path
import shutil
import os


def build_target_index(target_dir: Path) -> set[str]:
    filenames = set()
    for root, _, files in os.walk(target_dir):
        for f in files:
            filenames.add(f)
    return filenames


def build_source_index(source_dir: Path) -> list[dict]:
    records = []
    for root, _, files in os.walk(source_dir):
        for f in files:
            src = Path(root) / f
            if is_hidden_or_system_file(src) or src.is_dir():
                continue
            records.append({
                "path": src,
                "name": src.name,
                "suffix": src.suffix.lower(),
            })
    return records


def plan_actions(source_files: list[dict], existing_filenames: set[str], skip_dupe: bool) -> list[dict]:
    actions = []
    for f in source_files:
        if not get_file_type(f["suffix"]):
            continue
        if skip_dupe and f["name"] in existing_filenames:
            actions.append({"action": "skip", **f})
        else:
            actions.append({"action": "copy", **f})
    return actions


def execute_actions(actions: list[dict], target_root: Path, skip_dupe: bool):
    for a in actions:
        if a["action"] != "copy":
            continue

        src_path = a["path"]
        print(f"Copying {src_path} -> ", end="", flush=True)
        try:
            file_type = get_file_type(src_path.suffix)
            year, date_str = extract_date_taken(src_path)
            camera = extract_camera_model(src_path)
            target_dir = target_root / year / date_str / camera / file_type
            target_dir.mkdir(parents=True, exist_ok=True)
            base_target_path = target_dir / src_path.name
            final_target_path = get_target_path(base_target_path, skip_dupe)
            if final_target_path is None:
                print("⏩ skipped (dupe)")
                continue
            shutil.copy2(src_path, final_target_path)
            print(f"{final_target_path} ✅ success")
        except Exception as e:
            print(f"❌ error: {e}")


def str_to_bool(v: str) -> bool:
    return v.lower() in ("true", "yes", "1")


def main():
    parser = argparse.ArgumentParser(
        description="PhotonKit – safely organize and manage your camera photos."
    )
    parser.add_argument(
        "--source", required=True,
        help="Path to the source folder or volume (e.g., SD card)"
    )
    parser.add_argument(
        "--target", required=True,
        help="Path to the backup folder or volume (e.g., external drive)"
    )
    parser.add_argument(
        "--skip-dupe", default="true",
        help=(
            "(default) true, skip files that already exist in target. "
            "false allows duplicates (IMG_1234-1.jpg, etc)."
        )
    )

    # Show help if no arguments are passed
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)

    args = parser.parse_args()
    skip_dupe = str_to_bool(args.skip_dupe)

    source = Path(args.source).expanduser().resolve()
    target = Path(args.target).expanduser().resolve()
    if not source.exists():
        print(f"❌ Source does not exist: {source}")
        return
    target.mkdir(parents=True, exist_ok=True)

    try:
        ensure_exiftool()
        print("📥 Indexing source...")
        source_files = build_source_index(source)
        print("📤 Indexing target...")
        target_filenames = build_target_index(target)
        print("📦 Planning...")
        actions = plan_actions(source_files, target_filenames, skip_dupe)

        total = len(actions)
        to_copy = sum(1 for a in actions if a["action"] == "copy")
        skipped = total - to_copy

        print(f"\n📊 Plan: {total} files")
        print(f"  ➤ To copy : {to_copy}")
        print(f"  ➤ Skipped : {skipped}\n")

        execute_actions(actions, target, skip_dupe)

    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user. Exiting cleanly.")


if __name__ == "__main__":
    main()
