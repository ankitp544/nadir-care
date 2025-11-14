# NadirCare Backend API

FastAPI backend for medical report analysis using OCR and AI.

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Install system dependencies (macOS)
brew install tesseract poppler

# Run the server
python main.py
```

Server runs at: `http://localhost:8000`

### Environment Variables

- `ANTHROPIC_API_KEY` (optional) - Your Anthropic API key for Claude analysis
  - If not set, the API will use mock data

## 🌐 Cloud Deployment

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for complete deployment guide to Render (free tier).

### Quick Deploy to Render

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repository
4. Set root directory to `backend`
5. Deploy!

Render will automatically:
- Install Tesseract OCR
- Install Poppler (PDF processing)
- Install Python dependencies
- Start your API

## 📡 API Endpoints

### `GET /`
Health check endpoint.

**Response:**
```json
{
  "message": "NadirCare API is running"
}
```

### `POST /upload`
Upload a medical report (image or PDF) for analysis.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (JPG, PNG, or PDF)

**Response:**
```json
{
  "recommendation": "ADMISSION" | "DOCTOR_VISIT" | "HOME_MEDICATION",
  "severity": "low" | "moderate" | "high" | "critical",
  "reasoning": "Explanation of recommendation",
  "conditions": ["List of conditions"],
  "symptoms": ["List of symptoms"],
  "next_steps": ["Recommended actions"]
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@medical_report.pdf"
```

## 🛠️ Tech Stack

- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Tesseract OCR** - Text extraction from images
- **Poppler** - PDF processing
- **Pillow** - Image processing
- **Anthropic Claude 3.5 Sonnet** - Medical report analysis (optional)

## 📂 Project Structure

```
backend/
├── main.py                    # FastAPI app & endpoints
├── report_processor.py        # OCR & text extraction
├── recommendation_engine.py   # Medical recommendations
├── requirements.txt           # Python dependencies
├── render.yaml               # Render deployment config
├── build.sh                  # Build script for Render
├── DEPLOYMENT.md             # Deployment guide
└── README.md                 # This file
```

## 🔧 Development

### Running Tests

```bash
python test_backend.py
```

### Adding Dependencies

```bash
pip install package_name
pip freeze > requirements.txt
```

### Local Testing with Android Emulator

The Android emulator uses `10.0.2.2` to access `localhost`:
- Your app should point to: `http://10.0.2.2:8000`

### Local Testing with Physical Device

Use your computer's IP address:
```bash
# Find your IP (macOS)
ipconfig getifaddr en0

# Update Android app to use: http://YOUR_IP:8000
```

## 🔒 Security

- Set `ANTHROPIC_API_KEY` in environment variables (never commit to git)
- Update CORS settings in `main.py` for production
- Use HTTPS in production (Render provides free SSL)

## 📝 Notes

- OCR accuracy depends on image quality
- PDF processing requires Poppler
- Without Anthropic API key, mock data is returned
- First request after cold start may be slow (free tier limitation)

## 🆘 Troubleshooting

**Tesseract not found:**
```bash
brew install tesseract
```

**Poppler not found:**
```bash
brew install poppler
```

**Port 8000 already in use:**
```bash
lsof -ti:8000 | xargs kill -9
```

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Render Documentation](https://render.com/docs)
- [Anthropic API Documentation](https://docs.anthropic.com)

---

Built with ❤️ for NadirCare
