#!/bin/bash

# Script to build and install NadirCare APK on a physical device

echo "📱 NadirCare - Build and Install APK"
echo "======================================="
echo ""

# Check if device is connected
echo "🔍 Checking for connected devices..."
DEVICES=$(adb devices | grep -v "List" | grep "device$" | wc -l | tr -d ' ')

if [ "$DEVICES" -eq 0 ]; then
    echo "❌ No Android device detected!"
    echo ""
    echo "Please:"
    echo "  1. Connect your Android device via USB"
    echo "  2. Enable USB Debugging (Settings → Developer Options)"
    echo "  3. Accept 'Allow USB debugging' prompt on device"
    echo ""
    echo "Check with: adb devices"
    exit 1
fi

echo "✅ Found $DEVICES connected device(s)"
adb devices
echo ""

# Get IP address for physical device
echo "🌐 Finding your computer's IP address..."
IP=$(ipconfig getifaddr en0 2>/dev/null || ifconfig | grep "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}')

if [ -z "$IP" ]; then
    echo "⚠️  Could not automatically detect IP address"
    echo "   Please update RetrofitClient.kt manually with your IP"
    echo "   Find IP with: ipconfig getifaddr en0"
    IP="192.168.x.x"
else
    echo "✅ Found IP: $IP"
    echo ""
    echo "⚠️  IMPORTANT: Update RetrofitClient.kt before building!"
    echo "   Change BASE_URL to: http://$IP:8000/"
    echo ""
    read -p "   Have you updated RetrofitClient.kt? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "   Please update app/src/main/kotlin/com/nadircare/app/RetrofitClient.kt"
        echo "   Change line 13 to: private const val BASE_URL = \"http://$IP:8000/\""
        exit 1
    fi
fi

# Build APK
echo ""
echo "🔨 Building Debug APK..."
cd "$(dirname "$0")"
./gradlew clean assembleDebug

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

APK_PATH="app/build/outputs/apk/debug/app-debug.apk"

if [ ! -f "$APK_PATH" ]; then
    echo "❌ APK not found at: $APK_PATH"
    exit 1
fi

echo "✅ APK built successfully!"
echo "   Location: $APK_PATH"
echo ""

# Install APK
echo "📲 Installing APK on device..."
adb install -r "$APK_PATH"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Installation successful!"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Start backend server: ./start_backend.sh"
    echo "   2. Open NadirCare app on your device"
    echo "   3. Ensure device and computer are on same Wi-Fi"
    echo "   4. Test file upload!"
    echo ""
    echo "🌐 Backend URL should be: http://$IP:8000"
else
    echo "❌ Installation failed!"
    echo ""
    echo "Try manually:"
    echo "   adb install $APK_PATH"
    exit 1
fi

