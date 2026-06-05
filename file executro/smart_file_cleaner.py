#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, timedelta
from zipfile import ZipFile, ZIP_DEFLATED
import argparse
import hashlib
import shutil
import os

try:
    import send2trash
except ImportError:
    send2trash = None


# =========================================================
#   DATE HELPERS
# =========================================================

def get_created_time(path: Path) -> float:
    """
    macOS: st_birthtime = created time
    Windows: st_ctime = created time
    Linux: fallback to modified time
    """
    stat = path.stat()

    if hasattr(stat, "st_birthtime"):
        return stat.st_birthtime

    if os.name == "nt":
        return stat.st_ctime

    return stat.st_mtime


def get_modified_time(path: Path) -> float:
    return path.stat().st_mtime


def format_date(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")


def get_group_name(path: Path, mode: str) -> str:
    created = datetime.fromtimestamp(get_created_time(path))

    if mode == "year":
        return created.strftime("%Y")

    if mode == "month":
        return created.strftime("%Y-%m")

    if mode == "day":
        return created.strftime("%Y-%m-%d")

    raise ValueError("Mode must be: year, month, or day")


# =========================================================
#   SIZE HELPERS
# =========================================================

def bytes_to_mb(size: int) -> float:
    return size / (1024 * 1024)


def bytes_to_gb(size: int) -> float:
    return size / (1024 * 1024 * 1024)


def human_size(size: int) -> str:
    if size >= 1024 * 1024 * 1024:
        return f"{bytes_to_gb(size):.2f} GB"
    return f"{bytes_to_mb(size):.2f} MB"


# =========================================================
#   SCANNER
# =========================================================

def scan_files(source: Path, output: Path | None = None) -> list[Path]:
    files = []

    for item in source.rglob("*"):
        if not item.is_file():
            continue

        # Skip hidden files
        if item.name.startswith("."):
            continue

        # Skip output folder
        if output:
            try:
                item.relative_to(output)
                continue
            except ValueError:
                pass

        files.append(item)

    return files


# =========================================================
#   REPORT
# =========================================================

def generate_report(files: list[Path]) -> None:
    if not files:
        print("No files found.")
        return

    total_size = sum(file.stat().st_size for file in files)

    extensions = {}

    categories = {
        "images": [".jpg", ".jpeg", ".png", ".webp", ".gif", ".heic"],
        "videos": [".mp4", ".mov", ".avi", ".mkv", ".webm"],
        "documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".pages"],
        "spreadsheets": [".xls", ".xlsx", ".csv", ".numbers"],
        "archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "installers": [".dmg", ".pkg", ".exe", ".msi"],
        "code": [".py", ".js", ".html", ".css", ".json", ".ts", ".jsx", ".tsx"],
    }

    category_totals = {key: 0 for key in categories}

    for file in files:
        ext = file.suffix.lower() or "[no extension]"
        size = file.stat().st_size

        extensions[ext] = extensions.get(ext, 0) + size

        for category, exts in categories.items():
            if ext in exts:
                category_totals[category] += size

    print("\n========== FILE REPORT ==========")
    print(f"Total files: {len(files)}")
    print(f"Total size: {human_size(total_size)}")

    print("\n--- Size by category ---")
    for category, size in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        if size > 0:
            print(f"{category:15} {human_size(size)}")

    print("\n--- Top extensions by size ---")
    for ext, size in sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"{ext:15} {human_size(size)}")


# =========================================================
#   LARGE FILES
# =========================================================

def find_large_files(files: list[Path], min_mb: int, source: Path) -> None:
    min_bytes = min_mb * 1024 * 1024

    large_files = [
        file for file in files
        if file.stat().st_size >= min_bytes
    ]

    large_files.sort(key=lambda file: file.stat().st_size, reverse=True)

    print(f"\n========== LARGE FILES OVER {min_mb} MB ==========")

    if not large_files:
        print("No large files found.")
        return

    for file in large_files:
        size = human_size(file.stat().st_size)
        created = format_date(get_created_time(file))
        print(f"{size:12} {created}  {file.relative_to(source)}")


# =========================================================
#   OLD FILES
# =========================================================

def find_old_files(files: list[Path], days: int, source: Path) -> None:
    cutoff = datetime.now() - timedelta(days=days)

    old_files = []

    for file in files:
        created = datetime.fromtimestamp(get_created_time(file))
        if created < cutoff:
            old_files.append(file)

    old_files.sort(key=lambda file: get_created_time(file))

    print(f"\n========== OLD FILES OLDER THAN {days} DAYS ==========")

    if not old_files:
        print("No old files found.")
        return

    total_size = sum(file.stat().st_size for file in old_files)

    print(f"Old files found: {len(old_files)}")
    print(f"Total old file size: {human_size(total_size)}\n")

    for file in old_files[:100]:
        size = human_size(file.stat().st_size)
        created = format_date(get_created_time(file))
        print(f"{size:12} {created}  {file.relative_to(source)}")

    if len(old_files) > 100:
        print(f"\nShowing first 100 only. {len(old_files) - 100} more old files found.")


# =========================================================
#   DUPLICATE FILES
# =========================================================

def file_hash(path: Path, chunk_size: int = 1024 * 1024) -> str:
    hash_obj = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hash_obj.update(chunk)

    return hash_obj.hexdigest()


def find_duplicates(files: list[Path], source: Path) -> None:
    print("\n========== DUPLICATE FILES ==========")
    print("Step 1: Grouping by file size...")

    size_map = {}

    for file in files:
        size = file.stat().st_size

        if size == 0:
            continue

        size_map.setdefault(size, []).append(file)

    possible_duplicates = [
        group for group in size_map.values()
        if len(group) > 1
    ]

    if not possible_duplicates:
        print("No duplicates found by size.")
        return

    print("Step 2: Hashing possible duplicates...")

    hash_map = {}

    for group in possible_duplicates:
        for file in group:
            try:
                hashed = file_hash(file)
                hash_map.setdefault(hashed, []).append(file)
            except PermissionError:
                print(f"Permission denied: {file}")
            except FileNotFoundError:
                continue

    duplicate_groups = [
        group for group in hash_map.values()
        if len(group) > 1
    ]

    if not duplicate_groups:
        print("No real duplicates found.")
        return

    wasted_space = 0

    for group in duplicate_groups:
        group.sort(key=lambda file: get_created_time(file))

        original = group[0]
        duplicates = group[1:]

        duplicate_size = sum(file.stat().st_size for file in duplicates)
        wasted_space += duplicate_size

        print("\nDuplicate group:")
        print(f"KEEP:   {original.relative_to(source)}")

        for duplicate in duplicates:
            print(f"REMOVE: {duplicate.relative_to(source)}")

    print(f"\nDuplicate groups found: {len(duplicate_groups)}")
    print(f"Possible space to recover: {human_size(wasted_space)}")
    print("\nThis command only reports duplicates. It does not delete anything.")


# =========================================================
#   ZIP BY DATE
# =========================================================

def zip_by_date(
    files: list[Path],
    source: Path,
    output: Path,
    mode: str,
    dry_run: bool,
    move_originals: bool,
    include_zips: bool
) -> None:
    selected_files = []

    for file in files:
        if not include_zips and file.suffix.lower() == ".zip":
            continue

        selected_files.append(file)

    grouped = {}

    for file in selected_files:
        group_name = get_group_name(file, mode)
        grouped.setdefault(group_name, []).append(file)

    print("\n========== ZIP BY DATE ==========")
    print(f"Groups found: {len(grouped)}")
    print(f"Mode: {mode}")
    print(f"Dry run: {dry_run}")

    for group_name in sorted(grouped.keys()):
        group_files = grouped[group_name]
        zip_path = output / f"{group_name}.zip"

        total_size = sum(file.stat().st_size for file in group_files)

        print(f"\nArchive: {zip_path.name}")
        print(f"Files: {len(group_files)}")
        print(f"Original size: {human_size(total_size)}")

        if dry_run:
            for file in group_files[:10]:
                print(f"  - {file.relative_to(source)}")

            if len(group_files) > 10:
                print(f"  ... and {len(group_files) - 10} more files")

            continue

        output.mkdir(parents=True, exist_ok=True)

        with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zipf:
            for file in group_files:
                arcname = file.relative_to(source)
                zipf.write(file, arcname)

        compressed_size = zip_path.stat().st_size
        print(f"Compressed size: {human_size(compressed_size)}")

        if move_originals:
            moved_folder = output / "_originals_moved" / group_name
            move_files(group_files, source, moved_folder)
            print(f"Moved originals to: {moved_folder}")


# =========================================================
#   DELETE BY YEAR
# =========================================================

def delete_by_year(
    files: list[Path],
    source: Path,
    year: int,
    dry_run: bool,
    use_trash: bool
) -> None:
    selected_files = []

    for file in files:
        created_year = datetime.fromtimestamp(get_created_time(file)).year

        if created_year == year:
            selected_files.append(file)

    print(f"\n========== DELETE BY YEAR: {year} ==========")

    if not selected_files:
        print(f"No files found from year {year}.")
        return

    selected_files.sort(key=lambda file: get_created_time(file))

    total_size = sum(file.stat().st_size for file in selected_files)

    print(f"Files found: {len(selected_files)}")
    print(f"Total size: {human_size(total_size)}")
    print(f"Trash mode: {use_trash}")
    print(f"Dry run: {dry_run}")

    print("\nFiles selected:")

    for file in selected_files[:150]:
        size = human_size(file.stat().st_size)
        created = format_date(get_created_time(file))
        print(f"{size:12} {created}  {file.relative_to(source)}")

    if len(selected_files) > 150:
        print(f"\nShowing first 150 only. {len(selected_files) - 150} more files selected.")

    if dry_run:
        print("\nDry run only. Nothing was deleted.")
        print(f"To move these files to Trash, run again without --dry-run:")
        print(f"python3 smart_file_cleaner.py {source} --delete-year {year}")
        return

    confirm = input(f"\nType DELETE {year} to confirm: ")

    if confirm != f"DELETE {year}":
        print("Cancelled. Nothing was deleted.")
        return

    if use_trash and send2trash is None:
        print("\nSend2Trash is not installed.")
        print("Install it with:")
        print("pip3 install Send2Trash")
        print("\nCancelled. Nothing was deleted.")
        return

    deleted_count = 0
    failed_count = 0

    for file in selected_files:
        try:
            if use_trash:
                send2trash.send2trash(str(file))
            else:
                file.unlink()

            deleted_count += 1

        except Exception as error:
            failed_count += 1
            print(f"Could not delete {file}: {error}")

    if use_trash:
        print(f"\nMoved {deleted_count} files from {year} to Trash.")
    else:
        print(f"\nPermanently deleted {deleted_count} files from {year}.")

    if failed_count > 0:
        print(f"Failed to delete: {failed_count} files.")


# =========================================================
#   SAFE MOVE
# =========================================================

def move_files(files: list[Path], source: Path, destination_root: Path) -> None:
    for file in files:
        relative_path = file.relative_to(source)
        destination = destination_root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(file), str(destination))


# =========================================================
#   MAIN
# =========================================================

def main():
    parser = argparse.ArgumentParser(
        description="Smart file cleaner: reports, duplicates, large files, old files, ZIP by date, and delete by year."
    )

    parser.add_argument(
        "source",
        help="Folder to scan, example: ~/Downloads or ~/Documents"
    )

    parser.add_argument(
        "--output",
        default="organized_zips",
        help="Output folder for ZIP files. Default: organized_zips"
    )

    parser.add_argument(
        "--report",
        action="store_true",
        help="Show file summary report."
    )

    parser.add_argument(
        "--duplicates",
        action="store_true",
        help="Find duplicate files by SHA256 hash."
    )

    parser.add_argument(
        "--large-files",
        type=int,
        metavar="MB",
        help="Find files larger than this size in MB. Example: --large-files 100"
    )

    parser.add_argument(
        "--old-files",
        type=int,
        metavar="DAYS",
        help="Find files older than this many days. Example: --old-files 180"
    )

    parser.add_argument(
        "--zip-by-date",
        action="store_true",
        help="Create ZIP archives grouped by date."
    )

    parser.add_argument(
        "--mode",
        choices=["year", "month", "day"],
        default="month",
        help="ZIP grouping mode: year, month, or day. Default: month"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview ZIP or delete operation without changing anything."
    )

    parser.add_argument(
        "--move-originals",
        action="store_true",
        help="Move original files to backup folder after ZIP creation."
    )

    parser.add_argument(
        "--include-zips",
        action="store_true",
        help="Include existing ZIP files when creating new ZIP archives."
    )

    parser.add_argument(
        "--delete-year",
        type=int,
        metavar="YEAR",
        help="Delete files created in a specific year. Example: --delete-year 2023"
    )

    parser.add_argument(
        "--permanent-delete",
        action="store_true",
        help="Permanently delete files instead of moving them to Trash."
    )

    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()

    if not source.exists():
        print(f"Source folder does not exist: {source}")
        return

    if not source.is_dir():
        print(f"Source is not a folder: {source}")
        return

    print(f"Scanning: {source}")

    files = scan_files(source, output)

    if not files:
        print("No files found.")
        return

    print(f"Files found: {len(files)}")

    no_action_selected = not any([
        args.report,
        args.duplicates,
        args.large_files,
        args.old_files,
        args.zip_by_date,
        args.delete_year,
    ])

    if args.report or no_action_selected:
        generate_report(files)

    if args.large_files:
        find_large_files(files, args.large_files, source)

    if args.old_files:
        find_old_files(files, args.old_files, source)

    if args.duplicates:
        find_duplicates(files, source)

    if args.zip_by_date:
        zip_by_date(
            files=files,
            source=source,
            output=output,
            mode=args.mode,
            dry_run=args.dry_run,
            move_originals=args.move_originals,
            include_zips=args.include_zips
        )

    if args.delete_year:
        delete_by_year(
            files=files,
            source=source,
            year=args.delete_year,
            dry_run=args.dry_run,
            use_trash=not args.permanent_delete
        )

    print("\nDone.")


if __name__ == "__main__":
    main()