#!/usr/bin/env bash
#
# install_linux.sh - Set up Python virtual environment and install dependencies
# for the pigen project on Linux.
#
# This script creates a virtual environment in the "venv" directory and
# installs all packages listed in requirements.txt.
#
# Usage: ./scripts/install_linux.sh

set -e

echo "[pigen] Creating Python virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "[pigen] Virtual environment created."
else
    echo "[pigen] Virtual environment already exists."
fi

# Activate the environment
source venv/bin/activate

echo "[pigen] Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "[pigen] Environment setup complete."
