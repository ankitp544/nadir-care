# 🏥 NadirCare - Start Here

Your project is ready to test! Follow these simple steps:

## ✅ What's Already Done

- ✅ Android app code (MainActivity, API layer, UI)
- ✅ Backend server (FastAPI)
- ✅ Backend dependencies installed
- ✅ Tesseract OCR installed
- ✅ Testing scripts created

## 🚀 Quick Test (3 Steps)

### Step 1: Start Backend Server

Open Terminal and run:
```bash
cd /Users/ankit/AndroidStudioProjects/NadirCare
./start_backend.sh
```

**Keep this terminal open!** You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Open in Android Studio

1. **Open Android Studio**
2. **File > Open**
3. Navigate to: `/Users/ankit/AndroidStudioProjects/NadirCare`
4. Click **OK**
5. Wait for Gradle sync (this may take a few minutes the first time)

### Step 3: Run on Emulator

1. **Create/Start Emulator:**
   - Click **Device Manager** (phone icon)
   - Click **Create Device** (if needed)
   - Select a device (e.g., Pixel 5)
   - Choose system image (API 33 or 34)
   - Click ▶️ **Play** to start emulator

2. **Run the App:**
   - Select your running emulator from dropdown
   - Click **Run** button (green play icon) or press `Shift + F10`
   - Wait for build and installation

3. **Test:**
   - Tap "Select Medical Report"
   - Choose a test image or PDF
   - Tap "Upload Report"
   - See the recommendation!

## 📚 Detailed Guides

- **QUICK_START.md** - Step-by-step testing guide
- **TESTING_GUIDE.md** - Comprehensive testing instructions
- **README.md** - Project overview

## 🛠️ Helper Scripts

- **`./start_backend.sh`** - Start backend server
- **`./setup_and_test.sh`** - Complete setup and test
- **`test_backend.py`** - Test backend API directly

## 🔍 Troubleshooting

### Backend won't start?
```bash
cd backend
source venv/bin/activate
python main.py
```

### App won't build?
- In Android Studio: **File > Sync Project with Gradle Files**
- **Build > Clean Project**
- **Build > Rebuild Project**

### Connection error?
- Verify backend is running: `curl http://localhost:8000/`
- Check RetrofitClient.kt uses: `http://10.0.2.2:8000/`

### Need help?
Check **TESTING_GUIDE.md** for detailed troubleshooting.

## 📝 Current Status

- **Backend URL**: `http://10.0.2.2:8000` (for emulator)
- **Backend Port**: `8000`
- **Min SDK**: Android 24 (Nougat)
- **Target SDK**: Android 34

---

**Ready to test?** Follow Step 1-3 above! 🚀

