@echo off
REM ==========================================================
REM   Plex Playlist Sync - One-click installer for Windows
REM   Double-click this file to set everything up.
REM ==========================================================

cd /d "%~dp0"

echo ==========================================
echo   Installing Plex Playlist Sync...
echo ==========================================

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python is not installed or not on your PATH.
    echo Install it from https://www.python.org/downloads/
    echo IMPORTANT: tick "Add Python to PATH" in the installer, then run this again.
    echo.
    pause
    exit /b 1
)

echo Creating a private virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Could not create the virtual environment.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo Installing required packages (this can take a minute)...
python -m pip install --upgrade pip >nul
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Package install failed.
    pause
    exit /b 1
)

if not exist ".env" (
    copy ".env.example" ".env" >nul
    echo.
    echo A config file named ".env" was created for you.
    echo Open it in Notepad and add your Plex server URLs and tokens.
)

echo.
echo [DONE] Install complete!
echo Next: edit the ".env" file, then double-click "start-windows.bat" to run.
pause
