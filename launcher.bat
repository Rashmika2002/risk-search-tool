@echo off
title Risk Search Tool Launcher
color 0A

echo.
echo ====================================================
echo       RISK SEARCH TOOL - LAUNCHER
echo ====================================================
echo.

REM Check if Python is installed
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)
echo       Python is installed

REM Check if in correct directory
echo.
echo [2/4] Checking application files...
if not exist "app.py" (
    echo [ERROR] app.py not found!
    echo Please make sure you are running this from the application folder
    pause
    exit /b 1
)
echo       Application files found

REM Install/update dependencies
echo.
echo [3/4] Installing dependencies...
pip install -r requirements.txt --quiet --disable-pip-version-check
if errorlevel 1 (
    echo [WARNING] Some dependencies may not have installed correctly
    echo The application may still work. If you encounter errors, run:
    echo pip install -r requirements.txt
    echo.
)
echo       Dependencies ready

REM Run application
echo.
echo [4/4] Starting application...
echo.
echo ====================================================
echo.
echo The application will open in your browser shortly
echo.
echo To stop: Press Ctrl+C or close this window
echo.
echo ====================================================
echo.

python app.py

REM If app exits, pause so user can see error message
echo.
echo.
echo ====================================================
echo Application has stopped
echo ====================================================
pause
