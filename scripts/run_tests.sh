#!/usr/bin/env bash
#
# run_tests.sh - Execute the unit test suite for the pigen project on Linux.
# If the required packages are missing the installation script is invoked.
#
# Usage: ./scripts/run_tests.sh

set -e

# Ensure dependencies are installed
missing=false
if [ ! -d "venv" ]; then
    echo "[pigen] Virtual environment not found. Running installer..."
    ./scripts/install_linux.sh
fi

source venv/bin/activate

for pkg in $(cut -d'=' -f1 requirements.txt); do
    pip show "$pkg" >/dev/null 2>&1 || missing=true
done

if [ "$missing" = true ]; then
    echo "[pigen] Installing missing packages..."
    pip install -r requirements.txt
else
    echo "[pigen] All requirements already satisfied."
fi

echo "[pigen] Running unit tests..."
python -m unittest discover -v -s tests
