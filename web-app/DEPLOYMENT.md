# Deploying DAWT-Transcribe Web App to Vercel

## Problem: "Function size too large" Error

This happens when Vercel tries to include your Python backend code in the web app build.

## ✅ Solution: Configure Vercel Correctly

### Option 1: Deploy from Vercel Dashboard (Recommended)

1. **Go to Vercel:** https://vercel.com/new
2. **Import your GitHub repository**
3. **IMPORTANT: Configure Root Directory**
   - Click "Edit" next to "Root Directory"
   - Enter: `web-app`
   - This tells Vercel to ONLY build the web-app folder
4. **Leave other settings as default**
5. **Click "Deploy"**

That's it! Vercel will now only see the web-app folder and ignore all the Python code.

### Option 2: Separate GitHub Repository (Alternative)

If you still have issues, create a separate repo for just the web app:

```bash
cd /Users/abdulbasitmuntaka/DAWT_Transcriber/web-app

# Initialize new git repo
git init
git add .
git commit -m "Initial commit: DAWT-Transcribe web app"

# Create new repo on GitHub: "DAWT-Transcribe-Web"
git remote add origin https://github.com/muntakabasit/DAWT-Transcribe-Web.git
git push -u origin main
```

Then deploy this separate repo to Vercel (no root directory needed).

### Option 3: Local Build Test

Test the build locally first:

```bash
cd /Users/abdulbasitmuntaka/DAWT_Transcriber/web-app

# Clean build
rm -rf .next node_modules
npm install
npm run build

# If build succeeds, you're good to deploy!
# If it fails, check the error messages
```

## 🔧 Vercel Configuration (Already Done)

The following files prevent Vercel from including backend code:

- ✅ `.gitignore` - Ignores node_modules, .next, etc.
- ✅ `.vercelignore` - Explicitly excludes Python files
- ✅ `vercel.json` - Build configuration

## 📝 Environment Variables

After deployment, add this environment variable in Vercel dashboard:

- **Name:** `NEXT_PUBLIC_API_URL`
- **Value:** `https://transcribe-h3f8nq.fly.dev`

(Go to Project Settings → Environment Variables)

## ✅ Deployment Checklist

Before deploying:

- [ ] Root directory set to `web-app` in Vercel
- [ ] Build runs locally without errors
- [ ] Backend API is running (check https://transcribe-h3f8nq.fly.dev/health)
- [ ] 2 missing components created (URLTranscribe, TranscriptDisplay)

## 🎯 Expected Result

After deployment:
- Your app will be live at `https://your-project.vercel.app`
- Users can record audio and transcribe URLs
- No App Store needed!
- Free forever (Vercel free tier)

## 🐛 Still Having Issues?

**Error: "Function size too large"**
- Make sure Root Directory is set to `web-app` in Vercel settings
- Or deploy from a separate repository (Option 2)

**Error: "Build failed"**
- Check that all components are created (URLTranscribe, TranscriptDisplay)
- Run `npm run build` locally to see the exact error

**Error: "API not working"**
- Verify backend is running: https://transcribe-h3f8nq.fly.dev/health
- Check environment variable is set in Vercel

## 💡 Pro Tip: Use Vercel CLI

Install Vercel CLI for faster deployments:

```bash
npm install -g vercel

cd /Users/abdulbasitmuntaka/DAWT_Transcriber/web-app
vercel login
vercel --prod
```

This automatically detects the correct configuration!

---

**Need help?** Open an issue: https://github.com/muntakabasit/TRANSCRIBE/issues
