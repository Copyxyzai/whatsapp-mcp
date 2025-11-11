@echo off
REM WhatsApp MCP Web Interface Startup Script for Windows

echo ================================================
echo WhatsApp MCP - Web Interface
echo ================================================
echo.

REM Check if we're in the right directory
if not exist "app.py" (
    echo Error: This script must be run from the web-interface directory
    echo Please run: cd web-interface ^&^& start.bat
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Python is not installed
    echo Please install Python 3.6 or higher
    pause
    exit /b 1
)

REM Check if virtual environment exists, if not create one
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Check if WhatsApp bridge is running (simplified check for Windows)
echo.
echo ================================================
echo Starting WhatsApp MCP Web Interface...
echo ================================================
echo.
echo Make sure the WhatsApp bridge is running on port 8080
echo (In another terminal: cd ..\whatsapp-bridge ^&^& go run main.go)
echo.
echo Access the web interface at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the Flask app
python app.py

pause
