#!/bin/bash
# ==========================================================
#  Plex Playlist Sync — Launcher for macOS
#  Double-click to start the app, then open the link it prints
#  in your web browser. Close this window to stop the app.
# ==========================================================

cd "$(dirname "$0")" || exit 1

if [ ! -d "venv" ]; then
    echo "❌ It looks like the app isn't installed yet."
    echo "   Double-click 'install-mac.command' first."
    read -r -p "Press Enter to close..."
    exit 1
fi

# shellcheck disable=SC1091
source venv/bin/activate

echo "=========================================="
echo "  Starting Plex Playlist Sync"
echo "  Open this in your browser:"
echo "     http://localhost:8511"
echo "  (Press Ctrl+C or close this window to stop.)"
echo "=========================================="
python app.py
