#!/bin/bash
#
# Convenience wrapper for download_uvr_model.py
# 
# Usage:
#   ./download_uvr_model.sh <model_name>
#   ./download_uvr_model.sh htdemucs
#   ./download_uvr_model.sh --list
#

set -e

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required but not installed"
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Run the Python script
python3 "${SCRIPT_DIR}/download_uvr_model.py" "$@"
