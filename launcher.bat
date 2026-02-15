@echo off
REM ============================================================================
REM Risk Search Tool - One-Click Launcher
REM ============================================================================

title Risk Search Tool

REM Change to script directory
cd /d "%~dp0"

REM Clear screen
cls

echo.
echo ================================================================================
echo                          RISK SEARCH TOOL
echo ================================================================================
echo.
echo Starting application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 First-time setup: Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
    echo.
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
if not exist "venv\.installed" (
    echo 📦 Installing dependencies (this may take a minute)...
    echo.
    pip install -r requirements.txt --quiet --upgrade
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo. > venv\.installed
    echo ✅ Dependencies installed
    echo.
)

REM Update dependencies if requirements.txt changed
pip install -r requirements.txt --quiet --upgrade >nul 2>&1

REM Start the application
echo.
echo ================================================================================
echo 🚀 Launching Risk Search Tool...
echo ================================================================================
echo.
echo Browser will open automatically at http://127.0.0.1:5000
echo.
echo To stop the application, close this window or press Ctrl+C
echo.
echo ================================================================================
echo.

REM Start Python app
python app.py

REM If app exits, pause so user can see error messages
echo.
echo.
echo ================================================================================
echo Application stopped
echo ================================================================================
pause