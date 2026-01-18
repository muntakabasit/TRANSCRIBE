# WhisperKit Integration Guide - Real Transcription

**Get actual transcription working in 10 minutes.**

---

## Current State

Right now your app uses **stub transcription** (fake data for testing UI).

After following this guide, you'll have **real on-device transcription** powered by OpenAI's Whisper model.

---

## Step 1: Add WhisperKit Package (2 minutes)

### In Xcode:

1. **File → Add Package Dependencies**

2. **Enter URL:**
   ```
   https://github.com/argmaxinc/WhisperKit
   ```

3. **Dependency Rule:** Up to Next Major Version

4. **Add to Target:** DAWT-Transcribe

5. **Click "Add Package"**

Xcode will download WhisperKit (~10-20 seconds).

---

## Step 2: Enable WhisperKit in Build Settings (1 minute)

### In Xcode:

1. **Select your project** (DAWT-Transcribe at top of navigator)

2. **Select DAWT-Transcribe target**

3. **Build Settings tab**

4. **Search for:** "Swift Compiler - Custom Flags"

5. **Under "Other Swift Flags"**:
   - Click the `+` button
   - Add: `-DWHISPERKIT_ENABLED`

   Should look like:
   ```
   Other Swift Flags
     Debug: -DWHISPERKIT_ENABLED
     Release: -DWHISPERKIT_ENABLED
   ```

6. **Build** (⌘B) to verify no errors

---

## Step 3: Verify Integration (30 seconds)

The code is already set up! I updated `TranscriptionManager.swift` to:

✅ Use WhisperKit when `WHISPERKIT_ENABLED` flag is set
✅ Fall back to stub when flag is not set
✅ Handle initialization and transcription

You don't need to modify any code. Just verify the build succeeds.

---

## Step 4: Test Real Transcription (5 minutes)

### First Run:

1. **Build and Run** on device (⌘R)

2. **Important:** First transcription will:
   - Download Whisper model (~150-400 MB depending on model)
   - Take 10-30 seconds to initialize
   - Show iOS download progress

3. **Subsequent transcriptions:**
   - Use cached model
   - Transcribe in 5-15 seconds (depending on audio length)

### Test Flow:

1. Tap "NEW TRANSCRIPTION"
2. Choose "Record Audio" or "Import Audio File"
3. Record 10-15 seconds of clear speech
4. Wait for transcription
5. **You should see REAL transcribed text** (not stub data)

---

## Step 5: Troubleshooting

### Build Errors

**Error:** `Cannot find 'WhisperKit' in scope`
- **Fix:** Make sure you added `-DWHISPERKIT_ENABLED` flag
- **Or:** Package didn't install. Try: File → Add Package Dependencies again

**Error:** `Unsupported Swift version`
- **Fix:** Xcode 15+ required. Update Xcode if needed.

**Error:** Memory issues during build
- **Fix:** Close other apps. Clean build folder (⇧⌘K) and try again.

### Runtime Errors

**Issue:** First transcription takes forever
- **Expected:** Model download can take 1-2 minutes on slow connection
- **Fix:** Be patient. Subsequent runs will be fast.

**Issue:** Transcription quality is poor
- **Fix:** Speak clearly, reduce background noise
- **Or:** Try a different Whisper model (see Model Selection below)

**Issue:** App crashes during transcription
- **Fix:** Older devices (iPhone 12 or earlier) may struggle with larger models
- **Solution:** Use `tiny` model instead of `base` (see below)

---

## Model Selection (Advanced - Optional)

WhisperKit supports multiple model sizes:

| Model | Size | Speed | Accuracy | Best For |
|-------|------|-------|----------|----------|
| `tiny` | ~75 MB | Fastest | Lower | Quick tests, older devices |
| `base` | ~150 MB | Fast | Good | **Recommended for v1.0** |
| `small` | ~500 MB | Slower | Better | Accuracy-critical use |
| `medium` | ~1.5 GB | Slow | Best | Not recommended for mobile |

**Default:** WhisperKit auto-selects `base` model (good balance).

### To Change Model:

If you want to force a specific model, update `TranscriptionManager.swift`:

```swift
func initializeWhisperKit() async {
    do {
        // Force tiny model for older devices
        whisperKit = try await WhisperKit(modelFolder: "tiny")

        // Or force small for better accuracy
        // whisperKit = try await WhisperKit(modelFolder: "small")

        print("WhisperKit initialized successfully")
    } catch {
        print("Failed to initialize WhisperKit: \(error)")
    }
}
```

**Note:** This is optional. Default auto-selection works great.

---

## Performance Expectations

### First Transcription (Model Download)
- Download: 10-60 seconds (depends on connection)
- Initialize: 5-10 seconds
- Transcribe: 5-15 seconds
- **Total:** 20-85 seconds

### Subsequent Transcriptions
- Initialize: 0 seconds (already cached)
- Transcribe: 3-10 seconds for 1 minute of audio
- **Total:** 3-10 seconds

### Battery Impact
- Moderate during transcription (similar to video recording)
- Negligible when idle

### Storage
- Model: 150-400 MB (one-time download)
- Transcripts: ~5-10 KB each

---

## Disabling WhisperKit (Back to Stub)

If you want to go back to stub for testing:

1. **Build Settings → Other Swift Flags**
2. **Remove** `-DWHISPERKIT_ENABLED`
3. **Build** (⌘B)

App will use stub data again. No code changes needed.

---

## What Happens Under the Hood

### With WhisperKit Enabled:
```
1. Import/Record audio
   ↓
2. Check if WhisperKit initialized
   ↓
3. If first time: Download model
   ↓
4. Transcribe with Whisper
   ↓
5. Convert Whisper segments to app format
   ↓
6. Display real transcription
```

### With WhisperKit Disabled (Stub):
```
1. Import/Record audio
   ↓
2. Wait 2 seconds (simulate processing)
   ↓
3. Return fake segments
   ↓
4. Display stub data
```

---

## Supported Languages

Whisper supports 99+ languages:

**Major languages:**
- English (EN)
- Spanish (ES)
- French (FR)
- German (DE)
- Chinese (ZH)
- Japanese (JA)
- And 90+ more...

**Auto-detection:** WhisperKit automatically detects the language.

**v1.0 limitation:** App currently shows "EN" for all transcripts. Future versions can add language detection display.

---

## Privacy & On-Device Processing

**Important:** WhisperKit runs **100% on-device**.

- ✅ No internet required (after model download)
- ✅ No audio uploaded to servers
- ✅ No cloud API calls
- ✅ No tracking
- ✅ Complete privacy

**This is why DAWT-Transcribe uses WhisperKit.**

---

## Known Issues & Limitations

### WhisperKit Limitations (v1.0):

1. **No streaming:** Must wait for full audio before transcription
2. **No speaker diarization:** Can't identify different speakers
3. **Resource intensive:** Uses significant CPU during transcription
4. **Model size:** Large initial download
5. **iOS 16+ only:** Requires modern iOS version

### These are acceptable tradeoffs for privacy and offline capability.

---

## Success Checklist

After setup, verify:

- [ ] WhisperKit package installed in Xcode
- [ ] `-DWHISPERKIT_ENABLED` flag added to build settings
- [ ] App builds without errors (⌘B)
- [ ] First transcription downloads model successfully
- [ ] Real transcribed text appears (not stub data)
- [ ] Subsequent transcriptions are faster
- [ ] Can use app offline (after model download)

**If all checkboxes pass: You're ready to ship!**

---

## Next Steps

1. **Test thoroughly:**
   - Different audio sources (record, import, URL)
   - Different lengths (10 sec to 5 min)
   - Background noise
   - Different accents

2. **Optimize if needed:**
   - Switch to `tiny` model for older devices
   - Add progress indication during model download
   - Handle offline scenarios

3. **Ship to TestFlight:**
   - Archive build
   - Upload to App Store Connect
   - Invite beta testers

---

## FAQ

**Q: Can I ship the app without WhisperKit?**
A: Yes, but it will only show stub data. Users won't get real transcriptions.

**Q: Is WhisperKit free?**
A: Yes, it's open source (MIT license). No API fees, no subscriptions.

**Q: Does it work offline?**
A: Yes, after the initial model download. Perfect for planes, remote areas, etc.

**Q: Can users choose the model?**
A: Not in v1.0. WhisperKit auto-selects. You can add model selection in v1.1+.

**Q: What about YouTube/TikTok URLs?**
A: WhisperKit transcribes audio files. URL downloading is separate (already implemented for direct links only).

**Q: Will this drain battery?**
A: Moderate drain during transcription (similar to video recording). Negligible when idle.

---

## Support

**WhisperKit issues:** https://github.com/argmaxinc/WhisperKit/issues
**DAWT-Transcribe issues:** Use your own repo

---

## Summary

1. **Add Package:** WhisperKit from GitHub
2. **Add Flag:** `-DWHISPERKIT_ENABLED` in build settings
3. **Build:** ⌘B
4. **Test:** Record audio, see real transcription
5. **Ship:** Archive and upload to TestFlight

**That's it. Real transcription in 10 minutes.**

---

*Built with WhisperKit for privacy and offline capability.*
*Following the DAWT Constitution: technology humility, no extraction.*
