#!/bin/bash
# ==========================================================
#  Plex Playlist Sync — One-click installer for macOS
#  Double-click this file to set everything up.
#  (First time: right-click -> Open -> Open, to get past the
#   macOS security warning about unidentified developers.)
# ==========================================================

cd "$(dirname "$0")" || exit 1

echo "=========================================="
echo "  Installing Plex Playlist Sync..."
echo "=========================================="

# Pick a Python 3 command
if command -v python3 >/dev/null 2>&1; then
    PY=python3
elif command -v python >/dev/null 2>&1; then
    PY=python
else
    echo "❌ Python 3 is not installed."
    echo "   Install it from https://www.python.org/downloads/ and run this again."
    read -r -p "Press Enter to close..."
    exit 1
fi

echo "Creating a private virtual environment..."
$PY -m venv venv || { echo "❌ Could not create venv."; read -r -p "Press Enter to close..."; exit 1; }

# shellcheck disable=SC1091
source venv/bin/activate

echo "Installing required packages (this can take a minute)..."
python -m pip install --upgrade pip >/dev/null
pip install -r requirements.txt || { echo "❌ Package install failed."; read -r -p "Press Enter to close..."; exit 1; }

if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo "📝 A config file named '.env' was created for you."
    echo "   Open it in a text editor and add your Plex server URLs and tokens."
fi

echo ""
echo "✅ Install complete!"
echo "   Next: edit the '.env' file, then double-click 'start-mac.command' to run."
read -r -p "Press Enter to close..."
