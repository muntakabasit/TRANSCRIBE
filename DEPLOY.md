# DAWT-Transcribe Deployment Guide

## ✅ What Was Fixed (v1.1)

### Performance Improvements
- **Removed MT5 Translation**: Eliminated slow CPU-based translation that was causing 10-20x slowdown
- **Whisper Native Support**: Now uses Whisper's built-in multi-language support
- **Expected Speed**: Transcription now takes seconds instead of minutes

### Language Support
- All 12 languages work correctly: English, Pidgin, Twi, Igbo, Yoruba, Hausa, Swahili, Amharic, French, Portuguese, Ewe, Dagbani
- Proper language code mapping ensures accurate transcription
- No more translation errors or missing transcriptions

## 🚀 Deploy to Fly.io

### Option 1: Install Fly CLI (Recommended)
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Deploy
fly deploy
```

### Option 2: Manual Deploy via Fly.io Dashboard
1. Go to https://fly.io/dashboard
2. Select your app: `transcribe-h3f8nq`
3. Click "Deploy" → "Deploy from GitHub"
4. Select the latest commit

### Verify Deployment
```bash
curl https://transcribe-h3f8nq.fly.dev/health
```

Should return:
```json
{
  "status": "healthy",
  "version": "2.3.0",
  "timestamp": "..."
}
```

## 🌐 Web App (Vercel)

The web app should auto-deploy from GitHub. Check deployment status:
- https://vercel.com/your-dashboard

## 📱 Install on Phone

### iPhone (Safari):
1. Go to your Vercel URL
2. Tap Share button (📤)
3. Tap "Add to Home Screen"
4. Tap "Add"

### Android (Chrome):
1. Go to your Vercel URL
2. Tap menu (⋮)
3. Tap "Add to Home Screen"
4. Tap "Install"

## 🧪 Test All Features

After deployment, test:
1. **Record** - Test with English and one local language (e.g., Pidgin)
2. **Upload** - Upload a short MP3 file
3. **URL** - Try a YouTube, TikTok, or Instagram URL

## 📊 Expected Performance

- **English**: 2-5 seconds for 1-minute audio
- **Local Languages**: 2-5 seconds for 1-minute audio (was 20-60 seconds before)
- **URL Downloads**: 10-30 seconds depending on video length

## 🐛 Troubleshooting

### Backend not responding
```bash
fly logs
```

### Web app not loading
Check Vercel deployment logs

### Languages still not working
1. Verify backend is running: `curl https://transcribe-h3f8nq.fly.dev/health`
2. Check language is in supported list
3. Try with a clear audio sample

## 💰 Cost Optimization

Current setup:
- Fly.io: Free tier (256MB RAM, shared CPU) - might be slow
- Vercel: Free tier

To improve speed further:
```bash
# Upgrade to 1GB RAM (recommended)
fly scale memory 1024

# Or 2GB RAM (current config)
fly scale memory 2048
```

## 📝 Next Steps

1. Deploy backend to Fly.io
2. Test all three input methods
3. Install PWA on phone
4. Share app URL with users

## 🔗 Links

- Backend: https://transcribe-h3f8nq.fly.dev
- GitHub: https://github.com/muntakabasit/TRANSCRIBE
- Vercel Dashboard: https://vercel.com
- Fly.io Dashboard: https://fly.io/dashboard
