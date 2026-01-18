# DAWT-Transcribe iOS - Quick Start Guide

**Get the app running in 15 minutes.**

## Prerequisites

- Mac with Xcode 15+ installed
- iPhone running iOS 16+ (simulator works but can't record audio)
- USB cable to connect iPhone

## Step 1: Create Xcode Project (5 minutes)

1. Open Xcode
2. File → New → Project
3. Choose: **iOS** → **App**
4. Configure:
   ```
   Product Name: DAWT-Transcribe
   Team: [Select your team]
   Organization Identifier: com.yourname
   Interface: SwiftUI
   Language: Swift
   Storage: None
   Include Tests: [Optional]
   ```
5. Click **Next**, choose location, click **Create**

## Step 2: Import Source Files (3 minutes)

1. In Finder, navigate to: `DAWT_Transcriber/DAWT-Transcribe-iOS/`

2. Drag these folders into your Xcode project Navigator:
   - App/
   - Views/
   - Models/
   - Services/
   - Storage/
   - DesignSystem/

3. In the popup:
   - ✓ **Copy items if needed**
   - ✓ **Create groups**
   - ✓ Select **DAWT-Transcribe** target
   - Click **Finish**

## Step 3: Configure Permissions (2 minutes)

1. In Xcode, select project in Navigator (top item)
2. Select **DAWT-Transcribe** target
3. Go to **Info** tab
4. Click **+** button to add keys:

   **Key 1:**
   - Key: `Privacy - Microphone Usage Description`
   - Type: String
   - Value: `DAWT-Transcribe needs microphone access to record audio for transcription`

   **Key 2:**
   - Key: `Supports Document Browser`
   - Type: Boolean
   - Value: YES

5. Go to **Signing & Capabilities** tab
6. Click **+ Capability**
7. Add **Background Modes**
8. Check these boxes:
   - ✓ Audio, AirPlay, and Picture in Picture
   - ✓ Background fetch

## Step 4: Fix Bundle Identifier (1 minute)

1. Stay in **Signing & Capabilities** tab
2. Change Bundle Identifier to: `com.[yourname].dawt-transcribe`
   - Replace `[yourname]` with your actual name or organization
   - Example: `com.johnsmith.dawt-transcribe`

## Step 5: Build and Run (2 minutes)

### For Simulator (Import Only):
1. Select simulator: iPhone 15 Pro (top toolbar)
2. Click ▶️ or press ⌘R
3. Wait for build (first time is slower)
4. App launches on simulator

### For Device (Full Features):
1. Connect iPhone via USB
2. Select your iPhone in top toolbar
3. Click ▶️ or press ⌘R
4. On iPhone: Trust this computer (if prompted)
5. Enter iPhone passcode
6. Wait for build and install
7. App launches on device

## Step 6: Test Basic Flow (2 minutes)

### On Device (Recommended):
1. Tap **NEW TRANSCRIPTION**
2. Choose **Record Audio**
3. Allow microphone access (first time)
4. Tap red circle to start recording
5. Speak for 5-10 seconds
6. Tap circle again to stop
7. See loading screen (2 seconds)
8. See transcript result with stub data
9. Tap **Share** button (↑)
10. Choose Files, Messages, or Mail
11. Verify TXT and MD files appear

### On Simulator (Import Only):
1. Tap **NEW TRANSCRIPTION**
2. Choose **Import Audio File**
3. Select any audio file (M4A, WAV, MP3)
4. See loading screen (2 seconds)
5. See transcript result
6. Test share functionality

## Troubleshooting

### "Failed to register bundle identifier"
- Go to **Signing & Capabilities**
- Change Bundle Identifier to unique value
- Example: `com.[yourname].dawt-transcribe`

### "No provisioning profiles found"
- Ensure you're logged into Xcode with Apple ID
- Xcode → Settings → Accounts → Add Apple ID
- Select your team in project settings

### "iPhone is not available"
- Disconnect and reconnect iPhone
- Trust computer on iPhone
- Restart Xcode if needed

### Build errors about missing files
- Check all folders were imported correctly
- Project Navigator should show:
  - DAWT-Transcribe/
    - App/
    - Views/
    - Models/
    - Services/
    - Storage/
    - DesignSystem/

### App crashes immediately
- Check Console in Xcode for errors
- Verify Info.plist has microphone permission
- Try cleaning: Product → Clean Build Folder (⇧⌘K)

### Recording doesn't work on simulator
- **Expected**: Simulator can't access microphone
- **Solution**: Use real device OR test with "Import Audio File"

## What You Should See

### Home Screen
- Warm off-white background (#F9F7F4)
- "DAWT-TRANSCRIBE" title at top
- Large gold "NEW TRANSCRIPTION" button centered
- "History (0)" link below button

### After Transcription
- White cards with timestamps
- Sample text: "I love you. I care about you..."
- Gold "NEW TRANSCRIPTION" button at bottom
- Share button (↑) in top right

### History Screen
- Empty state: "NO HISTORY" (first time)
- After transcription: List of past items
- Swipe left to delete

## Next Steps

### Phase 1 Testing (Current)
- [x] Import audio file
- [x] See stub transcription
- [x] Share as TXT/MD
- [x] View history
- [ ] Test on multiple devices
- [ ] Complete TESTING_CHECKLIST.md

### Phase 4: Add Real Transcription
1. File → Add Package Dependencies
2. Enter: `https://github.com/argmaxinc/WhisperKit`
3. Add to target: DAWT-Transcribe
4. Open `Services/TranscriptionManager.swift`
5. Uncomment lines 91-109 (WhisperKit integration)
6. Build and test with real audio

### Phase 5: Polish
1. Add app icon (1024x1024)
2. Create launch screen
3. Test on multiple devices
4. Complete full testing checklist
5. Archive and submit to TestFlight

## Files You Should Have

If you did everything correctly, Xcode should show:

```
DAWT-Transcribe/
├── App/
│   └── DAWT_TranscribeApp.swift
├── Views/
│   ├── HomeView.swift
│   ├── TranscriptionResultView.swift
│   ├── HistoryView.swift
│   └── Components/
│       ├── TranscriptCard.swift
│       ├── DAWTPrimaryButton.swift
│       ├── ToastView.swift
│       ├── ShareSheet.swift
│       └── LoadingStateView.swift
├── Models/
│   ├── Transcription.swift
│   ├── Segment.swift
│   └── TranscriptionState.swift
├── Services/
│   ├── TranscriptionManager.swift
│   ├── AudioRecorder.swift
│   ├── AudioImporter.swift
│   ├── TranscriptExporter.swift
│   └── BackgroundTaskManager.swift
├── Storage/
│   ├── TranscriptionStore.swift
│   └── FileManager+DAWT.swift
└── DesignSystem/
    └── DAWTDesign.swift
```

**Total: 21 Swift files**

## Success Check

You've successfully set up the app if:

- ✅ App launches without crashes
- ✅ Home screen looks correct (gold button, off-white background)
- ✅ Can import or record audio
- ✅ See loading state
- ✅ Get stub transcript result
- ✅ Can share as files
- ✅ History saves and loads

If any checkbox fails, see Troubleshooting section or BUILD_INSTRUCTIONS.md.

## Getting Help

1. **Build issues**: See BUILD_INSTRUCTIONS.md Section "Troubleshooting"
2. **Testing questions**: See TESTING_CHECKLIST.md
3. **Design questions**: See README.md and DAWT_MANIFESTO.md
4. **File structure**: See PROJECT_FILES.md

## You're Done! 🎉

You now have a working DAWT-Transcribe app. The only thing missing is real transcription (WhisperKit in Phase 4).

Everything else — UI, storage, sharing, history, background processing — is production-ready.

**Next:** Test the full flow, then integrate WhisperKit for real transcription.

---

*Built following the DAWT Constitution.*
*For tired people who just need it to work.*
