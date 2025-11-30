#!/bin/bash

# Helper script to push an image file from Mac to Android emulator
# Usage: ./push_image_to_emulator.sh ~/Desktop/image.jpg

# Add Android SDK platform-tools to PATH if needed
if [ -d "$HOME/Library/Android/sdk/platform-tools" ]; then
    export PATH="$HOME/Library/Android/sdk/platform-tools:$PATH"
fi

# Check if file path is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_image_file>"
    echo "Example: $0 ~/Desktop/test_image.jpg"
    exit 1
fi

IMAGE_PATH="$1"

# Check if file exists
if [ ! -f "$IMAGE_PATH" ]; then
    echo "Error: File not found: $IMAGE_PATH"
    exit 1
fi

# Get filename
FILENAME=$(basename "$IMAGE_PATH")

# Push to Downloads folder (accessible by file picker)
echo "Pushing $FILENAME to emulator..."
adb push "$IMAGE_PATH" "/sdcard/Download/$FILENAME"

if [ $? -eq 0 ]; then
    echo "✅ Successfully copied $FILENAME to emulator Downloads folder"
    echo "You can now access it from the file picker in the NadirCare app"
else
    echo "❌ Failed to copy file. Make sure emulator is running."
    exit 1
fi

