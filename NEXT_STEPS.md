# 🎉 Build Successful! Next Steps

Your Android app is built successfully. Now let's test it end-to-end!

## ✅ Step-by-Step Testing

### Step 1: Start the Backend Server

Open a terminal and run:

```bash
cd /Users/ankit/AndroidStudioProjects/NadirCare
./start_backend.sh
```

Or manually:
```bash
cd backend
source venv/bin/activate
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**⚠️ Keep this terminal open!** The backend must be running while testing.

**Quick test**: In another terminal, verify the backend is working:
```bash
curl http://localhost:8000/
```
Should return: `{"message":"NadirCare API is running"}`

---

### Step 2: Create/Start Android Emulator

1. **In Android Studio**:
   - Click **Device Manager** icon (📱 phone icon in toolbar)
   
2. **Create AVD (if you don't have one)**:
   - Click **Create Device**
   - Select a device (e.g., **Pixel 5** or **Pixel 7**)
   - Click **Next**
   - Select a **System Image**:
     - **API Level 33** (Android 13) or **34** (Android 14) recommended
     - Download if needed (click **Download** link)
   - Click **Next** → **Finish**

3. **Start the Emulator**:
   - Click the **▶️ Play** button next to your AVD
   - Wait for the emulator to fully boot (this may take 1-2 minutes)

---

### Step 3: Configure Backend URL (If Using Physical Device)

**For Emulator**: Already configured! The app uses `http://10.0.2.2:8000` which maps to your computer's `localhost:8000`.

**For Physical Device**: 
1. Find your computer's IP address:
   ```bash
   # macOS/Linux:
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # Or:
   ipconfig getifaddr en0  # macOS
   ```
   
2. Update `app/src/main/kotlin/com/nadircare/app/RetrofitClient.kt`:
   ```kotlin
   private const val BASE_URL = "http://YOUR_IP:8000/"
   ```
   Replace `YOUR_IP` with your computer's IP (e.g., `192.168.1.100`)

---

### Step 4: Run the App

1. **In Android Studio**:
   - Select your running emulator/device from the device dropdown (top toolbar)
   - Click **Run** button (▶️ green play icon) or press `Shift + F10`
   - Wait for the app to install and launch

2. **App should open** showing:
   - "NadirCare" title
   - "Select Medical Report" button
   - "Upload Report" button (initially disabled)

---

### Step 5: Test the Complete Flow

1. **Select a File**:
   - Tap "Select Medical Report" button
   - Choose an image (JPG/PNG) or PDF from the file picker
   - You can use any medical report image for testing, or create a test image
   - File name should appear below the button

2. **Upload the Report**:
   - Tap "Upload Report" button (should be enabled now)
   - You'll see "Analyzing your report..." with a progress indicator
   - Wait for processing (may take 10-30 seconds depending on file size)

3. **View Results**:
   - The app displays:
     - **Recommendation Type**: ADMISSION / DOCTOR_VISIT / HOME_MEDICATION
     - **Reasoning**: Explanation of the recommendation
     - **Suggested Actions**: List of next steps

---

## 🧪 Test Scenarios

### Test 1: Successful Upload
- ✅ Select file → Upload → See recommendation

### Test 2: No File Selected
- ✅ Try to upload without selecting a file → Should show error

### Test 3: Backend Not Running
- Stop backend → Try upload → Should show connection error

### Test 4: Different File Types
- Try JPG image
- Try PNG image  
- Try PDF file

---

## 🔍 Debugging Tips

### Check Logcat
- **View > Tool Windows > Logcat** in Android Studio
- Filter by: `com.nadircare.app`
- Look for network errors or API responses

### Backend Logs
- Check the terminal running the backend
- You'll see processing logs:
  ```
  Processing file: test.jpg (image/jpeg)
  Extracting text from image: test.jpg
  Extracted text length: 1234 characters
  Parsing with GenAI...
  ```

### Network Issues?
- **Emulator**: Ensure backend URL is `http://10.0.2.2:8000`
- **Physical Device**: Ensure device and computer are on same WiFi network
- **Firewall**: May need to allow port 8000

---

## ✅ Success Checklist

- [ ] Backend server running on port 8000
- [ ] Emulator/device started and running
- [ ] App installed and launched successfully
- [ ] Can select files (image/PDF)
- [ ] Can upload files
- [ ] Receive recommendations
- [ ] Results display correctly

---

## 🚀 What's Working

✅ Android app UI complete
✅ File picker functional
✅ File upload to backend
✅ Backend processing (OCR + GenAI parsing)
✅ Recommendation engine
✅ Results display

## 📝 Next Improvements (Optional)

- Add error handling for network timeouts
- Add image preview before upload
- Cache results locally
- Add user authentication (if needed)
- Improve GenAI prompts for better parsing
- Add more sophisticated recommendation logic

---

## 🆘 Need Help?

If something doesn't work:
1. Check **TESTING_GUIDE.md** for detailed troubleshooting
2. Verify backend is running: `curl http://localhost:8000/`
3. Check Logcat for error messages
4. Verify network permissions in AndroidManifest.xml

**Ready to test?** Start with Step 1 above! 🎯

