# NadirCare - Medical Report Analysis MVP

A simple Android app that allows patients to upload medical reports (image/PDF) and receive recommendations on next steps (hospital admission, doctor visit, or home medication).

## Project Structure

```
NadirCare/
├── src/main/              # Android app source code
│   ├── kotlin/com/nadircare/app/
│   │   ├── MainActivity.kt
│   │   ├── ApiService.kt
│   │   ├── ResponseModel.kt
│   │   └── RetrofitClient.kt
│   ├── res/               # Android resources
│   └── AndroidManifest.xml
├── backend/               # FastAPI backend
│   ├── main.py
│   ├── report_processor.py
│   ├── recommendation_engine.py
│   ├── requirements.txt
│   └── README.md
└── build.gradle.kts       # Android build configuration
```

## Setup Instructions

### Android App

1. Open the project in Android Studio
2. Sync Gradle files to download dependencies
3. Build and run on an emulator or device

**Note:** The app is configured to connect to `http://10.0.2.2:8000` (Android emulator localhost).
For physical devices, update `RetrofitClient.kt` with your computer's IP address.

### Backend API

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR:
   - **macOS**: `brew install tesseract`
   - **Ubuntu**: `sudo apt-get install tesseract-ocr`
   - **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki

4. Set up environment variable (optional, for GenAI integration):
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

5. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Features

- **File Upload**: Select and upload medical reports (JPG, PNG, PDF)
- **Text Extraction**: OCR processing for images and PDFs
- **GenAI Analysis**: Anthropic Claude 3.5 Sonnet parsing of medical text
- **Recommendation Engine**: Rule-based categorization:
  - **ADMISSION**: Critical conditions requiring hospital stay
  - **DOCTOR_VISIT**: Moderate conditions requiring consultation
  - **HOME_MEDICATION**: Minor conditions manageable at home

## API Endpoints

- `GET /` - Health check
- `POST /upload` - Upload medical report (multipart/form-data)

## MVP Limitations

- No user accounts or data persistence
- Single file upload per request
- Basic error handling
- Rule-based logic (not medically validated)
- No offline support

## Next Steps

To improve the MVP:
1. Add proper error handling and validation
2. Implement user authentication
3. Add data persistence
4. Improve GenAI prompts for better medical parsing
5. Add more sophisticated recommendation logic
6. Add offline support

