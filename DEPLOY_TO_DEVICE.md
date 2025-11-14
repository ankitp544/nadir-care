# 📱 Deploying to Physical Android Device

This guide explains how to build and install the NadirCare app on a physical Android device.

## Prerequisites

- Physical Android device (Android 7.0+ / API 24+)
- USB cable to connect device to computer
- Android Studio installed
- Backend server running (or accessible on network)

---

## Step 1: Enable Developer Options on Your Device

1. **Open Settings** on your Android device
2. **About Phone** → Find **Build Number**
3. **Tap Build Number 7 times** until you see "You are now a developer!"
4. Go back to **Settings** → You'll now see **Developer Options**

---

## Step 2: Enable USB Debugging

1. Open **Developer Options** (Settings → Developer Options)
2. Enable **USB Debugging**
3. If prompted, tap **Allow** to trust your computer
4. **Optional**: Enable **Install via USB** (if available)

---

## Step 3: Connect Device to Computer

1. **Connect your device** to your computer via USB cable
2. On your device, you may see a prompt: **"Allow USB debugging?"**
   - Check **"Always allow from this computer"**
   - Tap **OK**
3. **Verify connection** in Android Studio:
   - Open Android Studio
   - Look at the device dropdown (top toolbar)
   - Your device should appear in the list

**Troubleshooting Connection:**
- Try different USB ports (prefer USB 3.0)
- Try different USB cables
- Some devices require **File Transfer mode** (not Charging only)
- Install device USB drivers if needed (check device manufacturer website)

---

## Step 4: Update Backend URL for Physical Device

**Important**: Physical devices can't use `10.0.2.2`. You need your computer's IP address.

### Find Your Computer's IP Address

**macOS:**
```bash
ipconfig getifaddr en0
# Or:
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**Linux:**
```bash
hostname -I
# Or:
ip addr show | grep "inet "
```

**Windows:**
```cmd
ipconfig
# Look for IPv4 Address under your network adapter
```

You'll get something like: `192.168.1.100` or `192.168.0.50`

### Update RetrofitClient

1. Open: `app/src/main/kotlin/com/nadircare/app/RetrofitClient.kt`
2. Update the `BASE_URL`:

```kotlin
private const val BASE_URL = "http://192.168.1.100:8000/"  // Replace with YOUR IP
```

3. **Save the file**

**Important**: 
- Both your device and computer must be on the **same Wi-Fi network**
- If IP changes, update the URL
- Ensure firewall allows port 8000

---

## Step 5: Build APK

### Option A: Build Debug APK (Recommended for Testing)

**In Android Studio:**

1. **Build** → **Build Bundle(s) / APK(s)** → **Build APK(s)**
2. Wait for build to complete
3. You'll see a notification: **"APK(s) generated successfully"**
4. Click **locate** in the notification, or navigate to:
   ```
   app/build/outputs/apk/debug/app-debug.apk
   ```

**Or via Command Line:**
```bash
cd /Users/ankit/AndroidStudioProjects/NadirCare
./gradlew assembleDebug
```

APK will be at: `app/build/outputs/apk/debug/app-debug.apk`

### Option B: Build Release APK (For Distribution)

**For Release APK, you need a signing key first:**

1. **Build** → **Generate Signed Bundle / APK**
2. Select **APK** → **Next**
3. Create a new keystore (if you don't have one):
   - Click **Create new...**
   - Choose location and password
   - Fill in key information
   - Click **OK**
4. Select your keystore → Enter passwords
5. Click **Next** → **Finish**
6. APK will be at: `app/release/app-release.apk`

---

## Step 6: Install APK on Device

### Method 1: Via Android Studio (Easiest)

1. Make sure device is connected and recognized
2. Select your device from device dropdown (top toolbar)
3. Click **Run** button ▶️ (green play icon)
4. Android Studio will build and install automatically

### Method 2: Install via ADB (Command Line)

```bash
# Find APK path
cd /Users/ankit/AndroidStudioProjects/NadirCare

# Install via ADB
adb install app/build/outputs/apk/debug/app-debug.apk

# Or if you have the full path:
adb install /Users/ankit/AndroidStudioProjects/NadirCare/app/build/outputs/apk/debug/app-debug.apk
```

### Method 3: Install via File Transfer

1. **Copy APK** to your device:
   - Transfer `app-debug.apk` to your device via USB or cloud storage
   - Or email it to yourself

2. **On your device:**
   - Open **Files** app or download location
   - Tap the APK file
   - You may see **"Install blocked"** → Tap **Settings** → Enable **"Install unknown apps"**
   - Tap **Install** → **Done**

**Note**: Some devices require enabling "Install unknown apps" for the specific app you're using (Files, Chrome, Gmail, etc.)

---

## Step 7: Verify Installation

1. Find **NadirCare** app icon on your device
2. Tap to open
3. Verify it connects to backend:
   - Select a file
   - Try uploading
   - Check backend logs to see requests

---

## Step 8: Start Backend Server

**Before testing, ensure backend is running:**

```bash
cd /Users/ankit/AndroidStudioProjects/NadirCare/backend
source venv/bin/activate
python main.py
```

**Important**: 
- Backend must be accessible on your network
- Check firewall allows connections on port 8000
- Test from device browser: `http://YOUR_IP:8000/`

---

## Troubleshooting

### Device Not Detected

**Check ADB connection:**
```bash
adb devices
```

**If device shows as "unauthorized":**
- On device: Revoke USB debugging authorizations
- Disconnect and reconnect USB
- Accept "Allow USB debugging" prompt

**If device not listed:**
- Install device-specific USB drivers
- Try different USB port/cable
- Enable "Developer Options" → "USB Debugging"

### App Won't Connect to Backend

**Check:**
1. ✅ Backend is running: `curl http://localhost:8000/`
2. ✅ Correct IP address in `RetrofitClient.kt`
3. ✅ Device and computer on same Wi-Fi
4. ✅ Firewall allows port 8000

**Test connection from device:**
- Open Chrome on device
- Navigate to: `http://YOUR_IP:8000/`
- Should see: `{"message":"NadirCare API is running"}`

### "Install Blocked" Error

**Enable Unknown Sources:**
- Settings → Security → Enable **"Unknown Sources"** (Android 7 and below)
- Settings → Apps → Special Access → **"Install unknown apps"** (Android 8+)
- Enable for the app you're using (Files, Chrome, etc.)

### Build Errors

**Clean and rebuild:**
```bash
./gradlew clean
./gradlew assembleDebug
```

**In Android Studio:**
- Build → Clean Project
- Build → Rebuild Project

---

## Quick Reference

### Build Debug APK
```bash
./gradlew assembleDebug
```

### Install APK via ADB
```bash
adb install app/build/outputs/apk/debug/app-debug.apk
```

### Check Connected Devices
```bash
adb devices
```

### Find Your IP Address
```bash
# macOS
ipconfig getifaddr en0

# Linux
hostname -I
```

### Uninstall App
```bash
adb uninstall com.nadircare.app
```

---

## Network Configuration Tips

### For Home Network
- Use your computer's local IP (192.168.x.x)
- Ensure both devices on same Wi-Fi
- Router may need to allow device-to-device communication

### For Mobile Hotspot
- Share hotspot from your computer or phone
- Connect other device to hotspot
- Use the hotspot's IP address

### For Production/Cloud
- Deploy backend to cloud (AWS, Heroku, etc.)
- Update `BASE_URL` to cloud URL
- Use HTTPS for secure connections

---

## Next Steps

After successful installation:
1. ✅ Test file upload
2. ✅ Verify recommendations display
3. ✅ Check backend logs for processing
4. ✅ Test with different file types (JPG, PNG, PDF)

---

## Notes

- **Debug APK** is for testing only (unsigned, larger size)
- **Release APK** is for distribution (smaller, signed)
- Keep backend running while testing
- Backend URL in code must match your network setup

---

**Ready to test?** Follow steps 1-8 above! 🚀

