# Quick Start - Testing NadirCare in Android Emulator

Follow these steps to test the app locally. For cloud deployment, see `backend/DEPLOYMENT.md`.

## 🌐 Cloud Deployment

Want to deploy to the cloud for free? Check out:
- **[backend/DEPLOYMENT.md](backend/DEPLOYMENT.md)** - Full guide for deploying to Render (free tier)
- No server needed on your computer
- Access from anywhere
- Free SSL certificate included

---

## 🚀 Quick Steps

### 1. Install Backend Dependencies (First Time Only)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start Backend Server

**Option A: Use the helper script**
```bash
./start_backend.sh
```

**Option B: Manual start**
```bash
cd backend
source venv/bin/activate  # If using virtual environment
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**⚠️ Keep this terminal open!** The backend must run while testing.

### 3. Test Backend (Optional)

Open a new terminal and test:
```bash
curl http://localhost:8000/
```

Should return: `{"message":"NadirCare API is running"}`

### 4. Open in Android Studio

1. Open Android Studio
2. **File > Open**
3. Navigate to `/Users/ankit/AndroidStudioProjects/NadirCare`
4. Click **OK**
5. Wait for Gradle sync to complete

### 5. Create/Start Emulator

1. Click **Device Manager** icon (phone icon in toolbar)
2. Click **Create Device** (if no AVD exists)
   - Select: **Pixel 5** or any device
   - System Image: **API 33** or **34** (download if needed)
   - Click **Finish**
3. Click **Play** button ▶️ next to your AVD to start it
4. Wait for emulator to fully boot

### 6. Run the App

1. In Android Studio, select your running emulator from the device dropdown (top toolbar)
2. Click **Run** button (green play icon) or press `Shift + F10`
3. App will build, install, and launch automatically

### 7. Test the Flow

1. **Select File**: Tap "Select Medical Report" button
2. **Choose File**: Select an image (JPG/PNG) or PDF from the picker
3. **Upload**: Tap "Upload Report" button
4. **Wait**: See "Analyzing your report..." with progress
5. **View Results**: See recommendation (ADMISSION / DOCTOR_VISIT / HOME_MEDICATION)

## 🔧 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Missing Python packages:**
```bash
cd backend
pip install -r requirements.txt
```

### Android Build Issues

**Gradle sync failed:**
- Click **Sync Project with Gradle Files** (elephant icon)
- Or: **File > Sync Project with Gradle Files**

**Build errors:**
- **Build > Clean Project**
- **Build > Rebuild Project**
- **File > Invalidate Caches > Invalidate and Restart**

**App crashes:**
- Check **Logcat** in Android Studio (bottom panel)
- Verify backend is running: `curl http://localhost:8000/`
- Check network permissions in AndroidManifest.xml

**Connection refused:**
- Ensure backend URL in `app/src/main/kotlin/com/nadircare/app/RetrofitClient.kt` is `http://10.0.2.2:8000`
- Verify backend is running on port 8000
- Test from emulator browser: Open Chrome in emulator → `http://10.0.2.2:8000/`

### Test Backend API Directly

```bash
python test_backend.py
```

Or with a test file:
```bash
python test_backend.py /path/to/test/file.pdf
```

## 📝 Notes

- **Emulator uses `10.0.2.2`** to access your computer's `localhost:8000`
- **Physical devices** need your computer's IP address (update in RetrofitClient.kt)
- **GenAI features** require Anthropic API key (optional - works without it using mock data)
- Backend must be running before testing app

## ✅ Success Checklist

- [ ] Backend dependencies installed
- [ ] Tesseract OCR installed
- [ ] Backend server running on port 8000
- [ ] Android Studio project opened and synced
- [ ] Emulator created and running
- [ ] App builds and installs successfully
- [ ] App connects to backend
- [ ] File upload works
- [ ] Results display correctly

