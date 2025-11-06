# 📱 Deploy DAWT-Transcribe to Your iPhone

## ✅ Deployment Status
DAWT-Transcribe is now configured for deployment with:
- **Autoscale Deployment** (pay-per-use, scales automatically)
- **PWA Support** (installable on iPhone like a real app)
- **App Icon** (Virgil Abloh/Off-White inspired design)

---

## 🚀 Step 1: Deploy on Replit

1. **Click "Deploy"** button in Replit (top right corner)
2. **Choose "Autoscale"** deployment type
3. **Confirm settings:**
   - Machine: 1vCPU, 2 GiB RAM (default)
   - Max machines: 3 (default)
   - Run command: `uvicorn main:app --host 0.0.0.0 --port 5000`
4. **Click "Publish"** to deploy

⏱️ **Wait 2-3 minutes** for deployment to complete.

---

## 💰 Cost Breakdown

### Monthly Credits (Included)
- **Core subscription**: $25/month in credits
- **Teams subscription**: $40/month per user in credits

### Autoscale Pricing (After credits used)
- **Base fee**: $1.00/month
- **Compute**: $3.20 per million units
- **Requests**: $1.20 per million requests

**Important:** You only pay when people use your app. When idle = $0!

### Estimated Cost for Your Use Case
- **Light use** (10-20 transcriptions/day): ~$5-10/month
- **Medium use** (50-100 transcriptions/day): ~$15-20/month
- **Your Core credits ($25)** will likely cover all usage!

---

## 📱 Step 2: Install on iPhone (Like a Real App!)

After deployment completes:

### Option A: Add to Home Screen (Safari)
1. **Open Safari** on your iPhone
2. **Visit your deployment URL** (e.g., `https://dawt-transcribe-yourname.replit.app`)
3. **Tap the Share button** (box with arrow)
4. **Scroll down** and tap "Add to Home Screen"
5. **Tap "Add"** in the top right
6. **Done!** DAWT icon appears on your home screen 🎉

### Option B: Use Safari Installation Prompt
1. Visit the URL in Safari
2. Look for the **"Install App"** banner at the bottom
3. Tap "Install" → "Add"
4. App icon appears on home screen

---

## 🎯 Using DAWT-Transcribe on iPhone

### From YouTube/TikTok:
1. Open YouTube/TikTok app
2. Copy video URL (Share → Copy Link)
3. Open DAWT app from home screen
4. Paste URL
5. Select language (Twi, Pidgin, etc.)
6. Tap "PROCESS" → Done! ✨

### From Browser:
1. Find a video you want to transcribe
2. Tap **"Share"** → **"DAWT"** (if you set up shortcuts)
3. Transcription starts automatically

---

## 🔐 Privacy & Sovereignty

### What Happens to Your Data:
- ✅ Audio processed on Replit servers (not your phone)
- ✅ Transcripts stored in PostgreSQL database
- ✅ You can export/delete anytime
- ⚠️ Data goes through Replit (not fully local)

### For 100% Local Privacy:
- Use **Option 2** from our conversation (Mac Mini setup)
- All processing stays on your home network
- Zero cloud dependency

---

## 📊 Monitor Usage & Costs

**Check your usage:**
1. Go to https://replit.com/account#resource-usage
2. View compute/request costs
3. See remaining monthly credits

**Tip:** Your $25 Core credits reset monthly!

---

## 🎨 PWA Features Enabled

✅ **Offline-ready** - Can view past transcriptions offline  
✅ **Full-screen mode** - Hides Safari UI when launched  
✅ **App icon** - Custom DAWT icon on home screen  
✅ **Splash screen** - Professional loading screen  
✅ **Shortcuts** - Quick access to History/New Transcription  

---

## 🚨 Troubleshooting

### "App won't install on iPhone"
- Use Safari (not Chrome/Firefox)
- Make sure deployment is live and accessible
- Clear Safari cache and try again

### "Transcription fails"
- Check video is <21 minutes
- Make sure Replit deployment is running
- Check resource usage (may need to upgrade credits)

### "App is slow"
- First request wakes up server (takes 5-10 seconds)
- Subsequent requests are fast
- Consider upgrading to more machines for faster response

---

## 🎯 Next Steps

1. **Deploy now** (click Deploy button in Replit)
2. **Install on iPhone** (add to home screen)
3. **Test transcription** with a short Twi/Pidgin video
4. **Start building training dataset** (100+ videos)
5. **Eventually migrate to Mac Mini** for full sovereignty

---

## 📞 Quick Reference

**Deployment URL:** (will appear after deployment)  
**API Endpoint:** `https://your-url.replit.app/submit`  
**Results Page:** `https://your-url.replit.app/results/job_ID`  
**History:** `https://your-url.replit.app/history.html`  

**Ready to deploy? Click "Deploy" in Replit!** 🚀
