@echo off
REM ==========================================================
REM   Plex Playlist Sync - Launcher for Windows
REM   Double-click to start the app, then open the link below
REM   in your web browser. Close this window to stop the app.
REM ==========================================================

cd /d "%~dp0"

if not exist "venv" (
    echo [ERROR] It looks like the app isn't installed yet.
    echo Double-click "install-windows.bat" first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo ==========================================
echo   Starting Plex Playlist Sync
echo   Open this in your browser:
echo      http://localhost:8511
echo   (Close this window to stop the app.)
echo ==========================================
python app.py
pause
