#!/bin/bash

echo "🎵 Starting Music Genre Classifier - Full Stack Application"
echo "=================================================="
echo ""

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    pkill -f "python app.py"
    pkill -f "next dev"
    echo "✅ Servers stopped"
    exit 0
}

# Set trap to cleanup on exit
trap cleanup SIGINT SIGTERM

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Please run this script from the music-genre-classifier directory"
    exit 1
fi

echo "🔧 Setting up Python backend..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

# Navigate to backend directory
cd backend

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "🔧 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating Python virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🚀 Starting Python backend server in background..."
echo "🌐 Backend will be available at http://localhost:5000"
echo ""

# Start Python backend in background
python app.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend is running
if ! curl -s http://localhost:5000/health > /dev/null; then
    echo "❌ Backend failed to start"
    exit 1
fi

echo "✅ Backend is running successfully!"
echo ""

# Go back to main directory
cd ..

echo "🔧 Setting up Next.js frontend..."

# Install Node.js dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

echo "🚀 Starting Next.js frontend server..."
echo "🌐 Frontend will be available at http://localhost:3000"
echo ""
echo "🎯 Full application is starting up..."
echo "📱 Open http://localhost:3000 in your browser"
echo "⏹️  Press Ctrl+C to stop both servers"
echo ""

# Start Next.js frontend
npm run dev &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
