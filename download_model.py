#!/usr/bin/env python3
"""
Download RVC models from various sources and organize them for use with the RVC server.

Usage:
    python3 download_model.py <url> <voice_name>
    python3 download_model.py https://weights.gg/models/example.zip MyVoice

Supports:
- Direct .zip downloads (e.g., from weights.gg)
- Direct .pth model file downloads
- Automatic extraction and file organization
"""

import sys
import os
import argparse
import urllib.request
import urllib.parse
import zipfile
import shutil
from pathlib import Path


def download_file(url: str, dest_path: Path, show_progress: bool = True):
    """Download a file from URL to destination path with optional progress."""
    print(f"Downloading from: {url}")
    print(f"Saving to: {dest_path}")
    
    def progress_hook(block_num, block_size, total_size):
        if not show_progress or total_size <= 0:
            return
        downloaded = block_num * block_size
        percent = min(100, downloaded * 100 / total_size)
        bar_length = 50
        filled = int(bar_length * downloaded / total_size)
        bar = '=' * filled + '-' * (bar_length - filled)
        print(f'\r[{bar}] {percent:.1f}%', end='', flush=True)
    
    try:
        urllib.request.urlretrieve(url, dest_path, progress_hook if show_progress else None)
        if show_progress:
            print()  # New line after progress bar
        print(f"✓ Downloaded successfully")
        return True
    except Exception as e:
        print(f"\n✗ Download failed: {e}")
        return False


def extract_zip(zip_path: Path, extract_to: Path):
    """Extract zip file to destination directory."""
    print(f"Extracting {zip_path.name}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✓ Extracted to {extract_to}")
        return True
    except Exception as e:
        print(f"✗ Extraction failed: {e}")
        return False


def organize_model_files(model_dir: Path):
    """
    Organize model files to follow the expected naming convention:
    - model.pth (main model file)
    - added.index (optional index file)
    """
    print(f"Organizing model files in {model_dir}...")
    
    # Find all .pth files
    pth_files = list(model_dir.rglob("*.pth"))
    if not pth_files:
        print("⚠ Warning: No .pth files found")
        return False
    
    # If there's a subdirectory with model files, move them up
    for pth_file in pth_files:
        if pth_file.parent != model_dir:
            new_path = model_dir / pth_file.name
            print(f"Moving {pth_file.name} to root of model directory")
            shutil.move(str(pth_file), str(new_path))
            pth_file = new_path
    
    # Refresh the list after moving
    pth_files = list(model_dir.glob("*.pth"))
    
    # Rename the first/main .pth file to model.pth if it's not already named that
    if pth_files:
        main_pth = pth_files[0]
        if main_pth.name != "model.pth":
            print(f"Renaming {main_pth.name} → model.pth")
            main_pth.rename(model_dir / "model.pth")
    
    # Find and rename index files
    index_files = list(model_dir.rglob("*.index"))
    for idx_file in index_files:
        if idx_file.parent != model_dir:
            new_path = model_dir / idx_file.name
            print(f"Moving {idx_file.name} to root of model directory")
            shutil.move(str(idx_file), str(new_path))
            idx_file = new_path
    
    # Refresh and rename
    index_files = list(model_dir.glob("*.index"))
    if index_files:
        main_index = index_files[0]
        if main_index.name != "added.index":
            print(f"Renaming {main_index.name} → added.index")
            main_index.rename(model_dir / "added.index")
    
    # Clean up any subdirectories that are now empty or contain only non-essential files
    for item in model_dir.iterdir():
        if item.is_dir():
            try:
                if not any(item.iterdir()):  # Empty directory
                    item.rmdir()
                    print(f"Removed empty directory: {item.name}")
            except OSError:
                pass  # Directory not empty or can't be removed
    
    # Summary
    final_files = list(model_dir.glob("*"))
    print(f"\n✓ Model organization complete")
    print(f"Files in {model_dir.name}:")
    for f in sorted(final_files):
        if f.is_file():
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"  - {f.name} ({size_mb:.1f} MB)")
    
    return True


def download_and_setup_model(url: str, voice_name: str, models_base_dir: Path):
    """Main function to download and setup a model."""
    print(f"\n{'='*60}")
    print(f"Setting up RVC model: {voice_name}")
    print(f"{'='*60}\n")
    
    # Create models directory and voice subdirectory
    model_dir = models_base_dir / voice_name
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # Parse URL to determine file type
    parsed_url = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    if not filename:
        print("✗ Error: Could not determine filename from URL")
        return False
    
    # Download to temporary location
    if filename.endswith('.zip'):
        temp_file = model_dir / f"temp_{filename}"
        if not download_file(url, temp_file):
            return False
        
        if not extract_zip(temp_file, model_dir):
            return False
        
        # Clean up zip file
        temp_file.unlink()
        print(f"Cleaned up temporary zip file")
    
    elif filename.endswith('.pth'):
        # Direct model file download
        dest_file = model_dir / filename
        if not download_file(url, dest_file):
            return False
    
    else:
        print(f"⚠ Warning: Unknown file type for {filename}")
        print(f"Attempting to download anyway...")
        dest_file = model_dir / filename
        if not download_file(url, dest_file):
            return False
    
    # Organize the model files
    if not organize_model_files(model_dir):
        print("⚠ Warning: Model organization encountered issues")
    
    print(f"\n{'='*60}")
    print(f"✓ Model '{voice_name}' is ready!")
    print(f"{'='*60}")
    print(f"\nTo use this model:")
    print(f"1. Start the RVC server (if not already running):")
    print(f"   cd server")
    print(f"   docker compose up -d")
    print(f"2. In your Ableton device, set:")
    print(f"   - Backend: Local")
    print(f"   - Server: http://127.0.0.1:8000")
    print(f"   - rvc_model: {voice_name}")
    print()
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Download and setup RVC models for the Ableton M4L RVC server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 download_model.py https://example.com/model.zip MyVoice
  python3 download_model.py https://weights.gg/models/voice.zip CoolVoice
  python3 download_model.py https://example.com/model.pth DirectModel
  
  # Specify custom models directory
  python3 download_model.py https://example.com/model.zip MyVoice --models-dir ./custom_models
        """
    )
    
    parser.add_argument('url', help='URL to download the model from (zip or pth file)')
    parser.add_argument('voice_name', help='Name for the voice model (used as directory name)')
    parser.add_argument('--models-dir', type=str, default='./server/models',
                        help='Base directory for models (default: ./server/models)')
    
    args = parser.parse_args()
    
    # Convert to Path object
    models_base_dir = Path(args.models_dir).resolve()
    
    # Validate models directory exists or can be created
    try:
        models_base_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"✗ Error: Could not create models directory: {e}")
        return 1
    
    # Validate voice name (alphanumeric, underscore, hyphen)
    if not all(c.isalnum() or c in ('_', '-') for c in args.voice_name):
        print(f"✗ Error: Voice name should contain only letters, numbers, underscore, or hyphen")
        return 1
    
    # Run the download and setup
    success = download_and_setup_model(args.url, args.voice_name, models_base_dir)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
