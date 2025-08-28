#!/bin/bash

echo "🎵 Starting Audio Analysis Backend..."
echo "📁 Current directory: $(pwd)"
echo "🐍 Checking Python environment..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🚀 Starting Flask backend server..."
echo "🌐 Backend will be available at http://localhost:5000"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

# Start the Flask server
python app.py
