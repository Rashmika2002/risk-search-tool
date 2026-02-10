#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "===================================================="
echo "       RISK SEARCH TOOL - LAUNCHER"
echo "===================================================="
echo ""

# Check if Python is installed
echo "[1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python 3 is not installed!${NC}"
    echo ""
    echo "Please install Python 3.8 or higher from:"
    echo "https://www.python.org/downloads/"
    echo ""
    exit 1
fi
echo -e "${GREEN}      Python is installed${NC}"

# Check if in correct directory
echo ""
echo "[2/4] Checking application files..."
if [ ! -f "app.py" ]; then
    echo -e "${RED}[ERROR] app.py not found!${NC}"
    echo "Please make sure you are running this from the application folder"
    exit 1
fi
echo -e "${GREEN}      Application files found${NC}"

# Install/update dependencies
echo ""
echo "[3/4] Installing dependencies..."
pip3 install -r requirements.txt --quiet --disable-pip-version-check 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[WARNING] Some dependencies may not have installed correctly${NC}"
    echo "The application may still work. If you encounter errors, run:"
    echo "pip3 install -r requirements.txt"
    echo ""
fi
echo -e "${GREEN}      Dependencies ready${NC}"

# Run application
echo ""
echo "[4/4] Starting application..."
echo ""
echo "===================================================="
echo ""
echo "The application will open in your browser shortly"
echo ""
echo "To stop: Press Ctrl+C"
echo ""
echo "===================================================="
echo ""

python3 app.py

# If app exits, show message
echo ""
echo ""
echo "===================================================="
echo "Application has stopped"
echo "===================================================="
