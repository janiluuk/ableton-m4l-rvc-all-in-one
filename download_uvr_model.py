#!/usr/bin/env python3
"""
Download UVR/Demucs models for audio source separation.

Usage:
    python3 download_uvr_model.py <model_name>
    python3 download_uvr_model.py htdemucs

Demucs models are normally auto-downloaded on first use, but this script
allows pre-downloading for offline use or faster container startup.

Supported models:
- htdemucs (default, 4-stem: vocals, drums, bass, other)
- htdemucs_ft (fine-tuned version)
- htdemucs_6s (6-stem separation)
- htdemucs_mmi (special version)
- mdx, mdx_extra, mdx_q, mdx_extra_q (MDX models)
"""

import sys
import os
import argparse
import urllib.request
import urllib.error
from pathlib import Path


# Demucs model URLs on GitHub releases
DEMUCS_MODELS = {
    'htdemucs': 'https://dl.fbaipublicfiles.com/demucs/hybrid_transformer/04573f0d-f3cf25b2.th',
    'htdemucs_ft': 'https://dl.fbaipublicfiles.com/demucs/hybrid_transformer/955717e8-8726e21a.th',
    'htdemucs_6s': 'https://dl.fbaipublicfiles.com/demucs/hybrid_transformer/5c90dfd2-34c22ccb.th',
    'htdemucs_mmi': 'https://dl.fbaipublicfiles.com/demucs/hybrid_transformer/75fc33f5-1941ce65.th',
    'mdx': 'https://dl.fbaipublicfiles.com/demucs/mdx_final/83fc094f-4a16d450.th',
    'mdx_extra': 'https://dl.fbaipublicfiles.com/demucs/mdx_final/e51eebcc-c1b80bdd.th',
    'mdx_q': 'https://dl.fbaipublicfiles.com/demucs/mdx_final/6b9c2ca1-3fd82607.th',
    'mdx_extra_q': 'https://dl.fbaipublicfiles.com/demucs/mdx_final/b72baf4e-8778635e.th',
}

# Maximum file size to download (2GB for large models)
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024


def get_cache_dir():
    """Get the Demucs model cache directory."""
    # Check for custom cache directory
    if 'DEMUCS_CACHE_DIR' in os.environ:
        cache_dir = Path(os.environ['DEMUCS_CACHE_DIR'])
    else:
        # Default Torch hub cache location
        cache_dir = Path.home() / '.cache' / 'torch' / 'hub' / 'checkpoints'
    
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def download_model(model_name: str, url: str, dest_path: Path):
    """Download a Demucs model file with progress indicator."""
    print(f"Downloading {model_name} model...")
    print(f"From: {url}")
    print(f"To: {dest_path}")
    
    def progress_hook(block_num, block_size, total_size):
        if total_size <= 0:
            downloaded = block_num * block_size
            print(f'\rDownloaded: {downloaded / (1024*1024):.1f} MB', end='', flush=True)
            return
        
        downloaded = block_num * block_size
        
        # Check file size limit
        if downloaded > MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024*1024):.1f}GB")
        
        percent = min(100, downloaded * 100 / total_size)
        bar_length = 50
        filled = int(bar_length * downloaded / total_size)
        bar = '=' * filled + '-' * (bar_length - filled)
        size_mb = total_size / (1024 * 1024)
        downloaded_mb = downloaded / (1024 * 1024)
        print(f'\r[{bar}] {percent:.1f}% ({downloaded_mb:.1f}/{size_mb:.1f} MB)', end='', flush=True)
    
    try:
        urllib.request.urlretrieve(url, dest_path, progress_hook)
        print()  # New line after progress bar
        print(f"✓ Downloaded successfully")
        return True
    except urllib.error.URLError as e:
        print(f"\n✗ Download failed (URL error): {e}")
        return False
    except urllib.error.HTTPError as e:
        print(f"\n✗ Download failed (HTTP {e.code}): {e.reason}")
        return False
    except ValueError as e:
        print(f"\n✗ Download failed: {e}")
        return False
    except OSError as e:
        print(f"\n✗ Download failed (I/O error): {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Download UVR/Demucs models for audio source separation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available models:
  htdemucs       - Default 4-stem model (vocals, drums, bass, other) [recommended]
  htdemucs_ft    - Fine-tuned version
  htdemucs_6s    - 6-stem separation model
  htdemucs_mmi   - Special version
  mdx            - MDX model
  mdx_extra      - MDX with extra quality
  mdx_q          - MDX quantized
  mdx_extra_q    - MDX extra quantized

Examples:
  python3 download_uvr_model.py htdemucs
  python3 download_uvr_model.py htdemucs_ft
  
  # Use custom cache directory
  DEMUCS_CACHE_DIR=/custom/path python3 download_uvr_model.py htdemucs

Note: Demucs normally auto-downloads models on first use. This script is
useful for pre-downloading models for offline use or faster startup.
        """
    )
    
    parser.add_argument('model', 
                        nargs='?',
                        choices=list(DEMUCS_MODELS.keys()),
                        help='Name of the Demucs model to download')
    parser.add_argument('--cache-dir', type=str,
                        help='Custom cache directory (default: ~/.cache/torch/hub/checkpoints)')
    parser.add_argument('--list', action='store_true',
                        help='List all available models')
    
    args = parser.parse_args()
    
    if args.list:
        print("Available Demucs models:")
        for model in DEMUCS_MODELS.keys():
            print(f"  - {model}")
        return 0
    
    if not args.model:
        parser.error("the following arguments are required: model")
    
    # Get cache directory
    if args.cache_dir:
        cache_dir = Path(args.cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)
    else:
        cache_dir = get_cache_dir()
    
    model_name = args.model
    model_url = DEMUCS_MODELS[model_name]
    
    # Extract filename from URL
    filename = model_url.split('/')[-1]
    dest_path = cache_dir / filename
    
    print(f"\n{'='*60}")
    print(f"Downloading Demucs model: {model_name}")
    print(f"{'='*60}\n")
    
    # Check if already exists
    if dest_path.exists():
        size_mb = dest_path.stat().st_size / (1024 * 1024)
        print(f"Model already exists: {dest_path}")
        print(f"Size: {size_mb:.1f} MB")
        
        response = input("\nOverwrite existing model? [y/N]: ").strip().lower()
        if response != 'y':
            print("Download cancelled.")
            return 0
    
    # Download the model
    success = download_model(model_name, model_url, dest_path)
    
    if success:
        size_mb = dest_path.stat().st_size / (1024 * 1024)
        print(f"\n{'='*60}")
        print(f"✓ Model '{model_name}' is ready!")
        print(f"{'='*60}")
        print(f"Location: {dest_path}")
        print(f"Size: {size_mb:.1f} MB")
        print(f"\nTo use this model in the RVC server:")
        print(f"  1. Set DEMUCS_MODEL={model_name} in docker-compose.yml")
        print(f"  2. Or specify 'uvr_model: {model_name}' in the device")
        print()
        return 0
    else:
        print(f"\n✗ Failed to download model '{model_name}'")
        return 1


if __name__ == "__main__":
    sys.exit(main())
