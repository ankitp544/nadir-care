# Testing Guide for NadirCare

This guide will help you test the Android app in an emulator.

## Prerequisites

1. **Android Studio** installed with:
   - Android SDK (API 24+)
   - Android Emulator configured
   - At least one AVD (Android Virtual Device) created

2. **Python 3** installed (you have it at: `/Library/Frameworks/Python.framework/Versions/3.12/bin/python3`)

3. **Tesseract OCR** installed:
   ```bash
   brew install tesseract  # macOS
   ```

## Step 1: Set Up Backend Dependencies

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Set Anthropic API key for GenAI features:
   ```bash
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

## Step 2: Start the Backend Server

Run the FastAPI server:
```bash
python main.py
```

You should see output like:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Keep this terminal window open!** The backend must be running for the app to work.

Test the backend:
```bash
curl http://localhost:8000/
```

You should see: `{"message":"NadirCare API is running"}`

## Step 3: Open Project in Android Studio

1. Open Android Studio
2. Select "Open an Existing Project"
3. Navigate to `/Users/ankit/AndroidStudioProjects/NadirCare`
4. Click "OK"
5. Wait for Gradle sync to complete

## Step 4: Create/Start an Android Emulator

1. In Android Studio, click the **Device Manager** icon (phone/tablet icon in toolbar)
2. If you don't have an AVD:
   - Click "Create Device"
   - Select a device (e.g., Pixel 5)
   - Select a system image (API 33 or 34 recommended)
   - Click "Finish"
3. Start the emulator by clicking the **Play** button next to your AVD

Wait for the emulator to fully boot.

## Step 5: Configure Backend URL

The app is already configured to use `http://10.0.2.2:8000` which is the Android emulator's way of accessing `localhost:8000` on your computer.

**Verify in**: `app/src/main/kotlin/com/nadircare/app/RetrofitClient.kt`
- Should have: `private const val BASE_URL = "http://10.0.2.2:8000/"`

## Step 6: Build and Run the App

1. In Android Studio, select your running emulator from the device dropdown
2. Click the **Run** button (green play icon) or press `Shift + F10`
3. Wait for the app to build and install

If you encounter build errors:
- Click "Sync Project with Gradle Files" (elephant icon with sync arrows)
- Check that all dependencies are downloaded
- Try "Build > Clean Project" then "Build > Rebuild Project"

## Step 7: Test the App

1. **App Launch**: The app should open showing the NadirCare interface
2. **Select File**: Click "Select Medical Report" button
   - Choose a test image (JPG/PNG) or PDF from your device
   - You can use any medical report image for testing
3. **Upload**: Click "Upload Report" button
4. **Wait for Processing**: You'll see "Analyzing your report..." with a progress indicator
5. **View Results**: The app should display:
   - Recommendation type (ADMISSION, DOCTOR_VISIT, or HOME_MEDICATION)
   - Reasoning
   - Suggested actions

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Missing dependencies:**
```bash
pip install -r requirements.txt
```

**Tesseract not found:**
```bash
# Check installation
which tesseract
# If not found, install: brew install tesseract
```

### Android App Issues

**Build errors:**
- Sync Gradle: File > Sync Project with Gradle Files
- Clean build: Build > Clean Project
- Invalidate caches: File > Invalidate Caches > Invalidate and Restart

**App crashes on upload:**
- Check Logcat in Android Studio for error messages
- Verify backend is running: `curl http://localhost:8000/`
- Check network permissions in AndroidManifest.xml

**Connection refused:**
- Verify backend URL in `RetrofitClient.kt` is `http://10.0.2.2:8000`
- Check backend is running on port 8000
- Try accessing from emulator browser: `http://10.0.2.2:8000/`

**File picker not working:**
- Grant storage permissions if prompted
- On Android 13+, the app uses scoped storage (should work automatically)

## Quick Test Script

You can also test the backend directly with a sample file:

```bash
# Test backend with a sample image
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/test/image.jpg"
```

## Notes

- The backend must be running before testing the app
- Use `10.0.2.2` for emulator, your computer's IP for physical devices
- GenAI features require Anthropic API key (optional - app will work without it using mock data)
- For production, update CORS settings in `backend/main.py`

