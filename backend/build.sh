#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

echo "Verifying system dependencies..."
which tesseract || echo "WARNING: tesseract not found in PATH"
which pdftotext || echo "WARNING: pdftotext (poppler) not found in PATH"

echo "Testing tesseract..."
tesseract --version || echo "WARNING: tesseract test failed"

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Build complete!"

