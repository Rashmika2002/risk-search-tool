@echo off
REM ============================================================================
REM Risk Search Tool - One-Click Launcher
REM Double-click this file to start the application
REM ============================================================================

title Risk Search Tool - Starting...

REM Change to script directory
cd /d "%~dp0"

REM Clear screen
cls

echo.
echo ================================================================================
echo                          RISK SEARCH TOOL v2.0
echo ================================================================================
echo.
echo Starting application... Please wait.
echo.

REM ============================================================================
REM Check if Python is installed
REM ============================================================================

python --version >nul 2>&1
if errorlevel 1 (
    cls
    echo.
    echo ================================================================================
    echo                              ERROR: PYTHON NOT FOUND
    echo ================================================================================
    echo.
    echo Python is not installed or not in PATH.
    echo.
    echo PLEASE INSTALL PYTHON:
    echo 1. Go to: https://www.python.org/downloads/
    echo 2. Download Python 3.8 or higher
    echo 3. During installation: CHECK "Add Python to PATH"
    echo 4. Restart your computer
    echo 5. Run this file again
    echo.
    echo ================================================================================
    pause
    exit /b 1
)

REM ============================================================================
REM Check/Create Virtual Environment
REM ============================================================================

if not exist "venv" (
    echo.
    echo [1/3] First-time setup: Creating virtual environment...
    echo.
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo ❌ Failed to create virtual environment
        echo.
        echo Try running as Administrator:
        echo 1. Right-click this file
        echo 2. Select "Run as administrator"
        echo.
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
)

REM ============================================================================
REM Activate Virtual Environment
REM ============================================================================

echo.
echo [2/3] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment activated

REM ============================================================================
REM Install/Update Dependencies
REM ============================================================================

if not exist "venv\.installed" (
    echo.
    echo [3/3] Installing dependencies (first-time only, may take 1-2 minutes)...
    echo.
    pip install -r requirements.txt --quiet --upgrade
    if errorlevel 1 (
        echo.
        echo ❌ Failed to install dependencies
        echo.
        echo Try:
        echo 1. Run as Administrator
        echo 2. Check internet connection
        echo 3. Or manually run: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
    REM Mark as installed
    echo installed > venv\.installed
    echo ✅ Dependencies installed
) else (
    echo.
    echo [3/3] Checking for dependency updates...
    pip install -r requirements.txt --quiet --upgrade >nul 2>&1
    echo ✅ Dependencies up to date
)

REM ============================================================================
REM Start the Application
REM ============================================================================

cls
echo.
echo ================================================================================
echo                          RISK SEARCH TOOL v2.0
echo ================================================================================
echo.
echo 🚀 Starting application...
echo.
echo ⏳ Browser will open automatically in a few seconds...
echo.
echo 📍 URL: http://localhost:5000
echo.
echo ================================================================================
echo.
echo 💡 TIPS:
echo    - Keep this window open while using the app
echo    - Browser opens automatically
echo    - To stop: Close this window or press Ctrl+C
echo.
echo ================================================================================
echo.

REM Start Flask app
python app.py

REM ============================================================================
REM Handle Exit
REM ============================================================================

echo.
echo.
echo ================================================================================
echo                          APPLICATION STOPPED
echo ================================================================================
echo.
echo The Risk Search Tool has been closed.
echo.
echo To start again: Double-click this file
echo.
pause