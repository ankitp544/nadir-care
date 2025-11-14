#!/bin/bash

# Complete setup and test script for NadirCare

echo "🚀 NadirCare - Setup and Test Script"
echo "========================================"
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "app" ]; then
    echo "❌ Error: Please run this script from the NadirCare    project root"
    exit 1
fi
# Activate virtual environment
source venv/bin/activate

# Check for Tesseract
echo ""
echo "🔍 Checking for Tesseract OCR..."
if command -v tesseract &> /dev/null; then
    echo "   ✅ Tesseract found: $(tesseract --version | head -1)"
else
    echo "   ⚠️  Tesseract not found!"
    echo "   Install with: brew install tesseract"
    echo ""
fi

# Check for Anthropic API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "   ⚠️  ANTHROPIC_API_KEY not set (optional - app will work with mock data)"
    echo "   Set with: export ANTHROPIC_API_KEY=your_key_here"
else
    echo "   ✅ ANTHROPIC_API_KEY is set"
fi

cd ..

# Step 2: Instructions for Android Studio
echo ""
echo "📱 Step 2: Android Studio Setup"
echo "   ============================="
echo ""
echo "   1. Open Android Studio"
echo "   2. File > Open"
echo "   3. Select: $(pwd)"
echo "   4. Wait for Gradle sync"
echo ""

# Step 3: Start backend option
echo "🖥️  Step 3: Starting Backend Server"
echo "   ================================"
echo ""
read -p "   Start the backend server now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "   Starting server on http://0.0.0.0:8000"
    echo "   Access from emulator at: http://10.0.2.2:8000"
    echo "   Press CTRL+C to stop"
    echo ""
    cd backend
    source venv/bin/activate
    python main.py
else
    echo ""
    echo "   ℹ️  To start the backend later, run:"
    echo "      ./start_backend.sh"
    echo ""
    echo "   Or manually:"
    echo "      cd backend"
    echo "      source venv/bin/activate"
    echo "      python main.py"
    echo ""
fi

