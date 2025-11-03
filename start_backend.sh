#!/bin/bash

# Script to start the MedDiagnose backend server

echo "🚀 Starting MedDiagnose Backend Server..."
echo ""

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check for Tesseract
if ! command -v tesseract &> /dev/null; then
    echo "⚠️  Warning: Tesseract OCR not found!"
    echo "   Install with: brew install tesseract"
    echo ""
fi

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY not set"
    echo "   GenAI features will use mock data"
    echo "   Set with: export OPENAI_API_KEY=your_key_here"
    echo ""
fi

# Start server
echo "✅ Starting server on http://0.0.0.0:8000"
echo "   Access from emulator at: http://10.0.2.2:8000"
echo "   Press CTRL+C to stop"
echo ""
python main.py

