# Python Cleanup Tools

Some useful Python tools for everyone, made in Python.

This repo contains small command-line tools that help organize, analyze, and clean files from folders like `Downloads`, `Documents`, or any custom directory.

## Current Tool

### Smart File Cleaner

`smart_file_cleaner.py` is a file cleanup utility that can:

- Analyze files in a folder
- Show a file size report
- Find large files
- Find old files
- Find duplicate files
- Group files by date
- Create ZIP archives by year, month, or day
- Delete files by year safely using Trash
- Permanently delete files only when explicitly requested

The goal is to help clean messy folders like `Downloads` and `Documents` without deleting important files by accident.

## Features

### File Report

Shows total files, total size, file categories, and top file extensions by size.

```bash
python3 smart_file_cleaner.py ~/Downloads --report

# Show report
python3 smart_file_cleaner.py ~/Downloads --report

# Find large files over 100 MB
python3 smart_file_cleaner.py ~/Downloads --large-files 100

# Find files older than 180 days
python3 smart_file_cleaner.py ~/Downloads --old-files 180

# Find duplicates
python3 smart_file_cleaner.py ~/Downloads --duplicates

# Preview ZIP by month
python3 smart_file_cleaner.py ~/Downloads --zip-by-date --mode month --dry-run

# Create ZIP by month
python3 smart_file_cleaner.py ~/Downloads --zip-by-date --mode month

# Create ZIP by year
python3 smart_file_cleaner.py ~/Downloads --zip-by-date --mode year

# Create ZIP by day
python3 smart_file_cleaner.py ~/Downloads --zip-by-date --mode day

# Create ZIP by month and move originals after
python3 smart_file_cleaner.py ~/Downloads --zip-by-date --mode month --move-originals

# Preview delete files from 2023
python3 smart_file_cleaner.py ~/Downloads --delete-year 2023 --dry-run

# Move files from 2023 to Trash
python3 smart_file_cleaner.py ~/Downloads --delete-year 2023

# Permanently delete files from 2023
python3 smart_file_cleaner.py ~/Downloads --delete-year 2023 --permanent-delete