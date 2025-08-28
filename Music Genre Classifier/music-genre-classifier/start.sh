#!/bin/bash

echo "🎵 Starting Music Genre Classifier..."
echo "📁 Current directory: $(pwd)"
echo "🔧 Installing dependencies..."

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

echo "🚀 Starting development server..."
echo "🌐 Open http://localhost:3000 in your browser"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

npm run dev
