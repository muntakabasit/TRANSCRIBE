# DAWT-Transcribe iOS Build Instructions

## Overview

This is a native iOS app built with SwiftUI that provides on-device audio transcription following the DAWT Constitution principles.

## Prerequisites

- macOS 13.0+ (Ventura or later)
- Xcode 15.0+
- iOS 16.0+ deployment target
- Apple Developer account (for device testing)

## Project Setup

### 1. Create New Xcode Project

1. Open Xcode
2. File → New → Project
3. Select "iOS" → "App"
4. Configure:
   - Product Name: `DAWT-Transcribe`
   - Team: Select your team
   - Organization Identifier: `com.yourname` (use your own)
   - Interface: SwiftUI
   - Language: Swift
   - Storage: None
   - Include Tests: Optional

### 2. Import Source Files

Copy all files from `DAWT-Transcribe-iOS/` directory into your Xcode project:

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

To import:
1. Right-click on project in Navigator
2. "Add Files to DAWT-Transcribe..."
3. Select folders with "Create groups" option
4. Ensure "DAWT-Transcribe" target is checked

### 3. Configure Info.plist

Add required permissions in Info.plist (or Project Settings → Info tab):

```xml
<key>NSMicrophoneUsageDescription</key>
<string>DAWT-Transcribe needs microphone access to record audio for transcription</string>

<key>UIBackgroundModes</key>
<array>
    <string>audio</string>
    <string>fetch</string>
</array>

<key>UISupportsDocumentBrowser</key>
<true/>
```

### 4. Add WhisperKit Dependency (Optional - Phase 3)

For Phase 1, the app uses stub transcription data. To add real transcription:

1. File → Add Package Dependencies
2. Enter URL: `https://github.com/argmaxinc/WhisperKit`
3. Dependency Rule: Up to Next Major Version
4. Add to target: DAWT-Transcribe

Then uncomment the WhisperKit integration code in `TranscriptionManager.swift:91-109`

### 5. Build Settings

**General Tab:**
- Deployment Target: iOS 16.0
- Supported Destinations: iPhone, iPad (optional)

**Signing & Capabilities:**
- Automatically manage signing: ✓
- Team: Select your team
- Add Capability: Background Modes
  - ✓ Audio, AirPlay, and Picture in Picture
  - ✓ Background fetch

**Build Settings:**
- Swift Language Version: Swift 5

## Running the App

### Simulator

1. Select iPhone simulator (e.g., iPhone 15 Pro)
2. Product → Run (⌘R)
3. Note: Audio recording doesn't work in simulator - use "Import Audio File" instead

### Device

1. Connect iPhone via USB
2. Select device in toolbar
3. Trust computer on device if prompted
4. Product → Run (⌘R)

## Testing Audio Files

For testing without recording:

1. Add test audio files to your Mac
2. AirDrop to iPhone, or use Files app
3. In app, tap "Import Audio File"
4. Select test file

Recommended test files:
- Short voice memos (10-30 seconds)
- Clear speech, minimal background noise
- Formats: M4A, WAV, MP3

## Build Configuration

### Debug Configuration (Default)

- Fast compilation
- Includes debug symbols
- Uses stub transcription

### Release Configuration

- Optimized performance
- Should include WhisperKit integration
- Archive for TestFlight/App Store

To build for release:
1. Product → Archive
2. Distribute App → App Store Connect / TestFlight

## File Structure in App

The app creates this structure in Documents directory:

```
Documents/
└── DAWT/
    ├── Transcriptions/
    │   └── by_date/
    │       └── 2026-01-15/
    │           └── [uuid].json
    └── Audio/ (for source files if needed)
```

## Troubleshooting

### "Failed to register bundle identifier"
- Change bundle identifier in General tab to unique value
- Use: `com.[yourname].dawt-transcribe`

### Microphone permission denied
- Settings → Privacy & Security → Microphone → DAWT-Transcribe → Toggle ON

### File import not working
- Check Info.plist has document browser key
- Try restarting app

### App crashes on transcription
- Check Console logs in Xcode
- Verify audio file format is supported
- Ensure background modes are enabled

### WhisperKit build errors
- Ensure Xcode 15+ (required for Swift 5.9)
- Clean build folder: Product → Clean Build Folder
- Close Xcode, delete DerivedData, reopen

## Performance Notes

### Phase 1 (Current - Stub Implementation)
- Instant "transcription" (2 second delay for UX)
- No model loading required
- Perfect for UI/UX testing

### Phase 3 (WhisperKit Integration)
- First transcription: ~10-30 seconds (model loading)
- Subsequent: ~5-15 seconds depending on audio length
- Uses ~200-500 MB RAM during transcription
- Model size: ~150-400 MB depending on variant

Recommended WhisperKit model for v1.0:
- `tiny` or `base` for speed
- `small` for better accuracy
- Download happens on first use

## App Size

- Phase 1 (stub): ~2-3 MB
- Phase 3 (WhisperKit): ~150-400 MB (including model)

## Next Steps

After successful build:

1. Test core flow: Import → Transcribe → Share
2. Verify storage: History should persist between launches
3. Test background: Start transcription, background app, verify notification
4. Integrate WhisperKit for real transcription
5. Add app icon and launch screen
6. Submit to TestFlight

## Constitutional Checkpoints

After building, verify:

- ✅ Works when user is tired/distracted? (Simple flow, clear states)
- ✅ No shame mechanisms? (No streaks, penalties, guilt)
- ✅ Full exit dignity? (Can leave at any time, progress saved)
- ✅ One dominant object per screen? (Yes - button, transcript, history item)
- ✅ Passes Auntie Test? (Would Auntie feel more capable? Yes.)

If any checkbox fails, return to code and fix before release.

## Support

For issues with:
- Xcode/build: Check Apple Developer Forums
- WhisperKit: Check https://github.com/argmaxinc/WhisperKit/issues
- DAWT principles: Review DAWT_MANIFESTO.md
