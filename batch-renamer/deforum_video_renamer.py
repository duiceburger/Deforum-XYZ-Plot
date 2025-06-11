#!/usr/bin/env python3
"""
Deforum Video Renamer Script

This script renames video files in Deforum output folders to match their folder names.
It looks for subfolders with batch names and renames any timestamped .mp4 files
inside them to use the folder name instead.

Usage:
    python deforum_video_renamer.py [output_directory]

If no directory is specified, it will use the current directory.

Example:
    Folder: 20250610233650_New_Circle_Best_Settings_666_iter_1024x1024_strength-0.4_strength_schedule-0.4_cfg-7
    Video:  20250610233833.mp4
    Result: 20250610233650_New_Circle_Best_Settings_666_iter_1024x1024_strength-0.4_strength_schedule-0.4_cfg-7.mp4
"""

import os
import sys
import re
import shutil
from pathlib import Path

def is_timestamp_folder(folder_name):
    """
    Check if a folder name contains a timestamp pattern (YYYYMMDDHHMMSS).
    This indicates it's likely a Deforum batch output folder.
    The timestamp can be anywhere in the folder name.
    """
    timestamp_pattern = r'\d{14}'
    return re.search(timestamp_pattern, folder_name) is not None

def is_timestamp_video(filename):
    """
    Check if a filename is a timestamp-only video file (YYYYMMDDHHMMSS.mp4).
    """
    timestamp_video_pattern = r'^\d{14}\.mp4$'
    return re.match(timestamp_video_pattern, filename) is not None

def extract_timestamp_from_folder(folder_name):
    """
    Extract the timestamp from a folder name.
    Returns the timestamp string if found, None otherwise.
    """
    timestamp_pattern = r'\d{14}'
    match = re.search(timestamp_pattern, folder_name)
    return match.group(0) if match else None

def find_and_rename_videos(base_directory, dry_run=False):
    """
    Find all video files in timestamp-named subfolders and rename them to match folder names.
    
    Args:
        base_directory (str): The directory to search for Deforum output folders
        dry_run (bool): If True, only show what would be renamed without actually doing it
    """
    base_path = Path(base_directory)
    
    if not base_path.exists():
        print(f"Error: Directory '{base_directory}' does not exist.")
        return
    
    renamed_count = 0
    error_count = 0
    
    print(f"Scanning directory: {base_path.absolute()}")
    print("-" * 60)
    
    # Look through all subdirectories
    for item in base_path.iterdir():
        if not item.is_dir():
            continue
            
        folder_name = item.name
        
        # Check if this looks like a Deforum batch folder (contains timestamp)
        if not is_timestamp_folder(folder_name):
            continue
            
        # Extract the timestamp from the folder name
        folder_timestamp = extract_timestamp_from_folder(folder_name)
        if not folder_timestamp:
            continue
            
        print(f"\nChecking folder: {folder_name}")
        print(f"  Folder timestamp: {folder_timestamp}")
        
        # Look for video files in this folder
        video_files = list(item.glob("*.mp4"))
        
        if not video_files:
            print(f"  No video files found")
            continue
            
        for video_file in video_files:
            video_name = video_file.name
            
            # Check if this is a timestamp-only video file
            if not is_timestamp_video(video_name):
                print(f"  Skipping '{video_name}' (doesn't match timestamp pattern)")
                continue
                
            # Extract timestamp from video name to see if it's related to this batch
            video_timestamp = video_name.replace('.mp4', '')
            
            # Create new filename using folder name
            new_video_name = f"{folder_name}.mp4"
            new_video_path = item / new_video_name
            
            # Check if target file already exists
            if new_video_path.exists() and new_video_path != video_file:
                print(f"  ⚠️  Warning: Target file '{new_video_name}' already exists")
                continue
                
            if dry_run:
                print(f"  📹 Would rename: '{video_name}' → '{new_video_name}'")
                print(f"     Video timestamp: {video_timestamp}, Folder timestamp: {folder_timestamp}")
            else:
                try:
                    # Rename the file
                    video_file.rename(new_video_path)
                    print(f"  ✅ Renamed: '{video_name}' → '{new_video_name}'")
                    renamed_count += 1
                except Exception as e:
                    print(f"  ❌ Error renaming '{video_name}': {e}")
                    error_count += 1
    
    print("\n" + "=" * 60)
    if dry_run:
        print("DRY RUN COMPLETE - No files were actually renamed")
    else:
        print(f"COMPLETED: {renamed_count} videos renamed")
        if error_count > 0:
            print(f"ERRORS: {error_count} files could not be renamed")

def main():
    """
    Main function to handle command line arguments and run the renamer.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Rename Deforum video files to match their folder names",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python deforum_video_renamer.py
  python deforum_video_renamer.py --dry-run
  python deforum_video_renamer.py "C:/path/to/deforum/outputs"
  python deforum_video_renamer.py "D:/AI Apps/stable-diffusion-webui/outputs/txt2img-images" --dry-run
        """
    )
    
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Directory containing Deforum output folders (default: current directory)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be renamed without actually doing it'
    )
    
    args = parser.parse_args()
    
    # Convert to absolute path for clarity
    directory = os.path.abspath(args.directory)
    
    print("Deforum Video Renamer")
    print("=" * 60)
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be changed")
        print("-" * 60)
    
    find_and_rename_videos(directory, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
