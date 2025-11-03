# 🚀 Deploying NadirCare Backend to Render

This guide will help you deploy your FastAPI backend to Render's free tier.

## Prerequisites

- GitHub account
- Render account (sign up at [render.com](https://render.com))
- Your code pushed to GitHub

## 📁 Important Files

- `render.yaml` - Render configuration
- `build.sh` - Python dependencies installation
- `apt-packages.txt` - System packages (Tesseract & Poppler)
- `requirements.txt` - Python packages

## 📋 Step-by-Step Deployment

### 1. Push Your Code to GitHub

If you haven't already:

```bash
cd /Users/ankit/AndroidStudioProjects/NadirCare
git add backend/
git commit -m "Add Render deployment configuration"
git push origin main
```

### 2. Create a New Web Service on Render

1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** button → **"Web Service"**
3. Connect your GitHub repository
4. Select your **NadirCare** repository

### 3. Configure Your Service

Fill in the following settings:

- **Name**: `nadircare-backend` (or any name you prefer)
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)
- **Root Directory**: `backend`
- **Runtime**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Instance Type**: **Free** (select from dropdown)

### 4. Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**:

| Key | Value | Notes |
|-----|-------|-------|
| `OPENAI_API_KEY` | `your-actual-api-key` | Your OpenAI API key (optional) |
| `PYTHON_VERSION` | `3.12.0` | Python version |

**Note**: If you don't have an OpenAI API key, the backend will work with mock data.

### 5. Deploy!

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Run the build script (installs Tesseract & Poppler)
   - Install Python dependencies
   - Start your FastAPI server
3. Wait 5-10 minutes for first deployment

### 6. Get Your Backend URL

Once deployed, you'll get a URL like:
```
https://nadircare-backend.onrender.com
```

Test it:
```bash
curl https://nadircare-backend.onrender.com/
```

Should return: `{"message":"MedDiagnose API is running"}`

## 🔧 Update Android App

Update the backend URL in your Android app:

**File**: `app/src/main/kotlin/com/meddiagnose/app/RetrofitClient.kt`

Change:
```kotlin
private const val BASE_URL = "http://10.0.2.2:8000/"
```

To:
```kotlin
private const val BASE_URL = "https://nadircare-backend.onrender.com/"
```

## ⚠️ Important Notes

### Free Tier Limitations

- **Sleep after 15 minutes of inactivity**: First request after sleep takes ~30 seconds
- **750 hours/month**: Enough for development and light usage
- **Limited memory**: 512 MB RAM

### Cold Starts

When the service "wakes up" from sleep:
- First request: ~30-60 seconds
- Subsequent requests: Normal speed (~1-2 seconds)

**Solution**: Implement a keep-alive ping or upgrade to paid tier ($7/month).

### Environment Variables

To update environment variables:
1. Go to your service dashboard
2. Click **"Environment"** tab
3. Add/update variables
4. Click **"Save Changes"** (triggers auto-redeploy)

## 🔍 Monitoring & Debugging

### View Logs

1. Go to your service dashboard
2. Click **"Logs"** tab
3. See real-time logs (same as your local terminal)

### Common Issues

**Build fails with "Read-only file system" error:**
- This happens if trying to use `apt-get` directly in build.sh
- Solution: Use `apt-packages.txt` file instead (already configured)
- System packages listed in `apt-packages.txt` are installed automatically

**Other build failures:**
- Check logs for errors
- Ensure `build.sh` has execute permissions: `chmod +x backend/build.sh`
- Verify all files are committed to GitHub

**Service crashes:**
- Check logs for Python errors
- Verify all dependencies are in `requirements.txt`

**Slow response:**
- Service may be sleeping (free tier limitation)
- Consider upgrading or using a keep-alive service

## 🚀 Next Steps

### Option 1: Keep-Alive (Prevent Sleep)

Use a free service like [UptimeRobot](https://uptimerobot.com/) or [Cron-Job.org](https://cron-job.org/) to ping your backend every 14 minutes:

```
https://nadircare-backend.onrender.com/
```

### Option 2: Upgrade to Paid Tier

$7/month gets you:
- No sleep mode
- More memory (512 MB → Multiple GB)
- Faster performance
- No cold starts

## 📊 Render Dashboard Features

- **Logs**: Real-time application logs
- **Events**: Deployment history
- **Metrics**: CPU, Memory, Response times
- **Shell**: Access to service shell (paid tiers only)
- **Environment**: Manage environment variables

## 🔐 Security Best Practices

1. **Never commit API keys** to GitHub
2. **Use environment variables** for all secrets
3. **Update CORS settings** in production:
   ```python
   # In main.py, update allow_origins:
   allow_origins=["https://your-android-app-domain.com"],
   ```

## 📝 Redeployment

Render automatically redeploys when you push to GitHub:

```bash
git add .
git commit -m "Update backend"
git push origin main
```

Watch deployment progress in Render dashboard.

## 🆘 Support

- Render Docs: [https://render.com/docs](https://render.com/docs)
- Render Community: [https://community.render.com](https://community.render.com)
- FastAPI Docs: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)

---

**Your backend is now live! 🎉**

Access it at: `https://your-service-name.onrender.com`

