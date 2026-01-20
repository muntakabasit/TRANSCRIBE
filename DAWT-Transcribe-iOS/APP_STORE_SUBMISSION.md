# DAWT-Transcribe App Store Submission Guide

## Pre-Submission Checklist

### ✅ Already Complete
- [x] Backend API deployed to Fly.io (`https://transcribe-h3f8nq.fly.dev`)
- [x] iOS app updated with production URL
- [x] All debug print statements removed
- [x] App icon created and installed (1024x1024)
- [x] Git repository up to date

### 📋 Required Before Submission

#### 1. App Store Connect Account
- [ ] Apple Developer Program membership ($99/year)
- [ ] App Store Connect account created
- [ ] App created in App Store Connect

#### 2. App Information & Metadata
- [ ] App name (DAWT-Transcribe or Transcribe)
- [ ] App description (short & long)
- [ ] Keywords for search
- [ ] Support URL
- [ ] Privacy Policy URL
- [ ] Copyright information

#### 3. Screenshots (Required)
- [ ] iPhone 6.7" (1290 x 2796) - iPhone 15 Pro Max
- [ ] iPhone 6.5" (1242 x 2688) - iPhone 11 Pro Max (optional but recommended)

#### 4. App Privacy Details
- [ ] Privacy nutrition label information
- [ ] Data collection disclosure
- [ ] Third-party SDK disclosure

#### 5. Build & Archive
- [ ] Final build in Release mode
- [ ] Archive created
- [ ] Upload to App Store Connect
- [ ] TestFlight testing (recommended)

---

## Step-by-Step Submission Process

### Step 1: Verify Build Configuration

**Open Xcode:**
```bash
cd /Users/abdulbasitmuntaka/DAWT_Transcriber/DAWT-Transcribe-iOS
open DAWT-Transcribe/DAWT-Transcribe.xcodeproj
```

**Check Project Settings:**
1. Select project in navigator (top item)
2. Select "DAWT-Transcribe" target
3. Go to **General** tab
4. Verify:
   - Display Name: `DAWT-Transcribe` or `Transcribe`
   - Bundle Identifier: `com.dawt.transcribe` (or your chosen ID)
   - Version: `1.0` (or your version)
   - Build: `1` (increment for each submission)
   - Deployment Target: iOS 16.0 or higher

**Check Signing & Capabilities:**
1. Go to **Signing & Capabilities** tab
2. Select your Team
3. Enable **Automatic Signing** (or configure manual signing)
4. Ensure provisioning profile is valid

---

### Step 2: Test Build Locally

**Clean Build:**
```
Product → Clean Build Folder (Cmd+Shift+K)
```

**Build for Release:**
```
Product → Scheme → Edit Scheme
- Select "Run" on left
- Change "Build Configuration" to "Release"
- Click "Close"
```

**Run on Physical Device:**
1. Connect your iPhone
2. Select your device from the scheme menu (top-left)
3. Run (Cmd+R)
4. **Test thoroughly:**
   - Record audio and transcribe
   - Transcribe a YouTube URL
   - Check sharing functionality
   - Verify icon appears correctly
   - Test in both light and dark mode

---

### Step 3: Create App Store Connect Listing

**Go to App Store Connect:**
https://appstoreconnect.apple.com

**Create New App:**
1. Click "My Apps" → "+" → "New App"
2. Fill in:
   - **Platform:** iOS
   - **Name:** DAWT-Transcribe (or Transcribe)
   - **Primary Language:** English
   - **Bundle ID:** Select from dropdown
   - **SKU:** `dawt-transcribe-001` (unique identifier)
   - **User Access:** Full Access

**Fill App Information:**

**Category:**
- Primary: Productivity
- Secondary: Utilities

**App Description (Example):**
```
DAWT-Transcribe is a powerful audio transcription app that converts speech to text with high accuracy. Perfect for students, journalists, content creators, and anyone who needs reliable transcription.

Features:
• Record and transcribe audio in real-time
• Transcribe YouTube videos and online content
• Support for multiple languages including African languages
• Export transcripts as text or markdown
• Beautiful, native iOS interface
• Privacy-focused with local processing

Supports: English, Pidgin, Twi, Igbo, Yoruba, Hausa, Swahili, Amharic, French, Portuguese, Ewe, and Dagbani.
```

**Keywords (Example):**
```
transcribe, transcription, speech to text, audio to text, voice, recorder, notes, subtitle, youtube, accessibility
```

**Support URL:**
```
https://github.com/muntakabasit/TRANSCRIBE
```

**Privacy Policy URL:**
You need to create a privacy policy. See Step 4 below.

---

### Step 4: Create Privacy Policy

Create a simple privacy policy page. Here's a template:

```markdown
# Privacy Policy for DAWT-Transcribe

Last updated: January 20, 2026

## Data Collection
DAWT-Transcribe processes audio transcriptions through our backend service. We collect:
- Audio files you choose to transcribe
- URLs you provide for transcription
- Transcription results

## Data Usage
- Audio data is processed solely for transcription
- No audio is permanently stored on our servers
- Transcription results are stored locally on your device
- We do not share your data with third parties

## Data Retention
- Audio files are deleted immediately after transcription
- Transcripts are stored only on your device
- You can delete transcripts at any time

## Third-Party Services
We use:
- Fly.io for hosting our transcription backend
- OpenAI Whisper for speech recognition

## Contact
For privacy concerns: [your-email@example.com]
```

**Host Your Privacy Policy:**
Option 1: Create a GitHub Page
```bash
cd /Users/abdulbasitmuntaka/DAWT_Transcriber
echo "# Privacy Policy for DAWT-Transcribe..." > PRIVACY.md
git add PRIVACY.md
git commit -m "Add privacy policy"
git push origin main
```
Then enable GitHub Pages in repo settings.

Option 2: Use a free service like:
- https://www.privacypolicies.com/
- https://www.freeprivacypolicy.com/

---

### Step 5: Take Screenshots

**Required Sizes:**
- iPhone 6.7" (1290 x 2796) - iPhone 15 Pro Max

**How to Take Screenshots:**

1. **Run app on simulator:**
   ```
   Xcode → Window → Devices and Simulators → Simulators
   Select: iPhone 15 Pro Max
   ```

2. **Launch app in simulator:**
   ```
   Product → Destination → iPhone 15 Pro Max
   Product → Run (Cmd+R)
   ```

3. **Navigate to key screens:**
   - Home screen with "Record" and "URL" buttons
   - Recording in progress
   - Transcription result view
   - History view with saved transcripts

4. **Take screenshots:**
   - In Simulator: `Cmd+S` (saves to Desktop)
   - Take 3-5 screenshots showing core functionality

5. **Clean up screenshots:**
   - Remove status bar time (set to 9:41 in simulator)
   - Ensure good contrast and visibility
   - Show actual transcription content

**Screenshot Tips:**
- Show the app icon in the status bar
- Use realistic content (not "Lorem ipsum")
- Demonstrate the main value proposition
- Keep UI clean and professional

---

### Step 6: Fill Privacy Nutrition Label

In App Store Connect → App Privacy:

**Data Collection:**
1. **Audio Data**
   - Collected: Yes
   - Linked to user: No
   - Used for: App Functionality
   - Purpose: Speech transcription

2. **User Content**
   - Collected: Yes (transcription results)
   - Linked to user: No
   - Used for: App Functionality

**Third-Party SDKs:**
- None (or list if using analytics)

---

### Step 7: Create Archive & Submit

**Archive Build:**
1. In Xcode, select scheme: **Any iOS Device (arm64)**
2. Go to: `Product → Archive`
3. Wait for archive to complete (5-10 minutes)
4. Organizer window will open

**Distribute to App Store:**
1. In Organizer, select your archive
2. Click **Distribute App**
3. Select **App Store Connect**
4. Click **Upload**
5. Select signing options:
   - **Automatically manage signing** (recommended)
   - Or use manual signing
6. Click **Upload**
7. Wait for upload to complete

**In App Store Connect:**
1. Go to your app → TestFlight tab
2. Wait for processing (30 minutes - 2 hours)
3. Once processed, build appears in TestFlight
4. Test with TestFlight (recommended)
5. Go to **App Store** tab
6. Click **+ Version or Platform** → iOS
7. Fill in version information
8. Select build from dropdown
9. Click **Submit for Review**

---

### Step 8: TestFlight Testing (Recommended)

Before submitting to App Store, test with TestFlight:

1. In App Store Connect → TestFlight
2. Add Internal Testers (your email)
3. Click **Add Group** → Create test group
4. Enable build for testing
5. Install TestFlight app on iPhone
6. Receive invitation email
7. Test thoroughly for 1-2 days
8. Fix any bugs, create new build, upload again

---

## Review Guidelines Compliance

**Make sure your app:**
- [ ] Has a clear, accurate description
- [ ] Screenshots match actual app functionality
- [ ] Doesn't crash or have critical bugs
- [ ] Privacy policy is accurate and accessible
- [ ] Respects user privacy
- [ ] Doesn't use private APIs
- [ ] Follows Apple's Human Interface Guidelines
- [ ] Provides value and functionality

**Common Rejection Reasons to Avoid:**
- ❌ Crashes on launch
- ❌ Incomplete functionality
- ❌ Misleading screenshots
- ❌ Missing privacy policy
- ❌ Accessing private data without permission
- ❌ Broken links in app description

---

## Post-Submission

**Review Timeline:**
- Initial review: 24-48 hours
- Resubmission after rejection: 24 hours

**Status Updates:**
1. **Waiting for Review** - In queue
2. **In Review** - Being tested by Apple
3. **Pending Developer Release** - Approved (you control release)
4. **Ready for Sale** - Live on App Store
5. **Rejected** - Review feedback provided, fix and resubmit

**If Rejected:**
1. Read rejection message carefully
2. Fix the issues mentioned
3. Respond in Resolution Center if needed
4. Increment build number
5. Create new archive
6. Upload and resubmit

---

## Quick Command Reference

**Build for testing:**
```bash
cd /Users/abdulbasitmuntaka/DAWT_Transcriber/DAWT-Transcribe-iOS
open DAWT-Transcribe/DAWT-Transcribe.xcodeproj

# Then in Xcode:
# Product → Clean Build Folder (Cmd+Shift+K)
# Product → Run (Cmd+R)
```

**Create archive:**
```
# In Xcode:
# 1. Select scheme: Any iOS Device (arm64)
# 2. Product → Archive
# 3. Wait for completion
# 4. Click "Distribute App"
```

**Increment build number:**
```bash
# Update in Xcode:
# Target → General → Build (increment by 1)
```

---

## Support Resources

- **App Store Connect:** https://appstoreconnect.apple.com
- **Apple Developer:** https://developer.apple.com
- **Review Guidelines:** https://developer.apple.com/app-store/review/guidelines/
- **Human Interface Guidelines:** https://developer.apple.com/design/human-interface-guidelines/
- **App Store Connect Help:** https://developer.apple.com/help/app-store-connect/

---

## Checklist Summary

Before clicking "Submit for Review":

- [ ] App builds and runs without crashes
- [ ] All features work as described
- [ ] App icon is professional and appropriate
- [ ] Screenshots are accurate and high-quality
- [ ] Description clearly explains the app
- [ ] Privacy policy is complete and hosted
- [ ] Privacy nutrition label is filled out
- [ ] Support URL works
- [ ] TestFlight testing completed (optional but recommended)
- [ ] Build number incremented from previous submission
- [ ] All required metadata filled in App Store Connect

---

**Good luck with your submission! 🚀**

Need help? Open an issue at: https://github.com/muntakabasit/TRANSCRIBE/issues
