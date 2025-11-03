# 🚀 Quick Deploy to Physical Device

Fastest way to build and install on your Android device.

## ⚡ Quick Steps

### 1. Enable Developer Mode
- **Settings** → **About Phone** → Tap **Build Number** 7 times
- **Settings** → **Developer Options** → Enable **USB Debugging**

### 2. Connect Device
- Connect via USB cable
- Accept "Allow USB debugging" prompt on device

### 3. Update Backend URL

Your computer's IP: **192.168.29.100**

Open: `app/src/main/kotlin/com/nadircare/app/RetrofitClient.kt`

Change line 13:
```kotlin
// FROM:
private const val BASE_URL = "http://10.0.2.2:8000/"

// TO:
private const val BASE_URL = "http://192.168.29.100:8000/"
```

**Note**: Your IP may change. Check with:
```bash
ipconfig getifaddr en0
```

### 4. Build & Install (Choose One Method)

#### Method A: Automated Script (Easiest)
```bash
./build_and_install.sh
```

#### Method B: Android Studio
1. Select your device from device dropdown
2. Click **Run** button ▶️

#### Method C: Command Line
```bash
# Build APK
./gradlew assembleDebug

# Install APK
adb install app/build/outputs/apk/debug/app-debug.apk
```

### 5. Start Backend Server
```bash
./start_backend.sh
```

**Important**: Both device and computer must be on **same Wi-Fi network**!

---

## 🔍 Verify Connection

**From device browser:**
- Open Chrome
- Navigate to: `http://192.168.29.100:8000/`
- Should see: `{"message":"NadirCare API is running"}`

---

## 📱 Test App

1. Open **NadirCare** app on device
2. Tap "Select Medical Report"
3. Choose file (image/PDF)
4. Tap "Upload Report"
5. View recommendation!

---

## ⚠️ Troubleshooting

### Device Not Detected
```bash
adb devices
```

If empty:
- Enable USB Debugging
- Accept prompt on device
- Try different USB port/cable

### Can't Connect to Backend
- ✅ Check backend is running
- ✅ Verify IP in RetrofitClient.kt
- ✅ Same Wi-Fi network
- ✅ Test in browser: `http://YOUR_IP:8000/`

### Build Errors
```bash
./gradlew clean
./gradlew assembleDebug
```

---

**That's it!** 🎉

For detailed instructions, see **DEPLOY_TO_DEVICE.md**

