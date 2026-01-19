# DAWT-Transcriber Backend Deployment Guide

## Option 1: Render.com (Recommended - Free Tier Available)

### Steps:

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Connect Repository**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `DAWT_Transcriber` repo

3. **Configure Service**
   - **Name**: `dawt-transcriber`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Instance Type**: Free (or Starter for $7/month)

4. **Environment Variables** (if needed)
   - None required for basic deployment

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for first deploy
   - You'll get a URL like: `https://dawt-transcriber.onrender.com`

### Important Notes:
- Free tier sleeps after 15 min inactivity (first request takes 30-60s to wake)
- Upgrade to Starter ($7/mo) for always-on service
- SSL (HTTPS) is automatic on Render

---

## Option 2: Railway.app (Alternative)

### Steps:

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `DAWT_Transcriber`

3. **Configure**
   - Railway auto-detects Python
   - Add environment variable: `PORT=5001`
   - Deploy automatically starts

4. **Get URL**
   - Go to Settings → Generate Domain
   - You'll get: `https://dawt-transcriber.up.railway.app`

### Pricing:
- $5/month credit free
- Pay-as-you-go after that

---

## After Deployment

### Update iOS App

1. Get your production URL (e.g., `https://dawt-transcriber.onrender.com`)

2. Update `APIClient.swift`:
   ```swift
   static let baseURL = "https://dawt-transcriber.onrender.com"
   ```

3. Update `Info.plist`:
   - Remove `NSAllowsArbitraryLoads = true`
   - Remove HTTP exception for local IP
   - HTTPS works by default (no exceptions needed)

4. Rebuild and test on iPhone

---

## Testing Production Backend

### Test endpoints:
```bash
# Health check
curl https://your-url.onrender.com/

# Test URL transcription
curl -X POST https://your-url.onrender.com/transcribe \
  -H "Content-Type: application/json" \
  -d '{"url": "https://tiktok.com/...", "lang": "en"}'
```

---

## Troubleshooting

**Issue**: "Application failed to respond"
- **Fix**: Increase timeout in Render settings (free tier has limits)

**Issue**: "Module not found"
- **Fix**: Check requirements.txt includes all dependencies

**Issue**: "Port already in use"
- **Fix**: Render sets PORT env var automatically, make sure main.py uses it

---

## Cost Comparison

| Service | Free Tier | Paid Tier | Always On |
|---------|-----------|-----------|-----------|
| Render  | Yes (sleeps) | $7/mo | Paid only |
| Railway | $5 credit/mo | Pay-as-you-go | Yes |
| Fly.io  | Limited | ~$5/mo | Yes |

**Recommendation**: Start with Render free tier, upgrade to $7/mo if sleep time is annoying.
