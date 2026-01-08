#!/bin/bash
#
# Convenience wrapper for download_model.py
# 
# Usage:
#   ./download_model.sh <url> <voice_name>
#   ./download_model.sh https://weights.gg/models/example.zip MyVoice
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
python3 "${SCRIPT_DIR}/download_model.py" "$@"
