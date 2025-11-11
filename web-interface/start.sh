#!/bin/bash

# WhatsApp MCP Web Interface Startup Script

echo "================================================"
echo "WhatsApp MCP - Web Interface"
echo "================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "Error: This script must be run from the web-interface directory"
    echo "Please run: cd web-interface && ./start.sh"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.6 or higher"
    exit 1
fi

# Check if virtual environment exists, if not create one
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check if WhatsApp bridge is running
echo ""
echo "Checking if WhatsApp bridge is running..."
if curl -s http://localhost:8080 > /dev/null 2>&1; then
    echo "✓ WhatsApp bridge is running on port 8080"
else
    echo "⚠ Warning: WhatsApp bridge may not be running on port 8080"
    echo "  Make sure to start it with: cd ../whatsapp-bridge && go run main.go"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "================================================"
echo "Starting WhatsApp MCP Web Interface..."
echo "================================================"
echo ""
echo "Access the web interface at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask app
python app.py
