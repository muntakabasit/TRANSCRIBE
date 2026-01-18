# DAWT-Transcribe iOS v1.0

**A constitutional tool for turning audio into text when you're tired.**

## What This Is

DAWT-Transcribe is a native iOS app that records or imports audio and generates timestamped transcripts — all on-device, no internet required. Built following the [DAWT Constitution](../DAWT_MANIFESTO.md), designed for 2am use when you're tired and just need it to work.

## Core Features (v1.0)

1. ✅ Record audio
2. ✅ Import audio file
3. ✅ **Transcribe from URL** (direct audio/video links)
4. ✅ Transcribe (on-device)
5. ✅ Display transcript with timestamps
6. ✅ Share via iOS Share Sheet (TXT + MD files)
7. ✅ View history of transcriptions
8. ✅ Re-open past transcription

**That's it.** No analytics. No cloud sync. No subscriptions. No shame mechanisms.

## Design Principles

Every decision follows the DAWT Constitution:

### The App MUST:
1. Work when user is tired, distracted, stressed
2. Have NO shame mechanisms (no streaks, countdowns, guilt)
3. Allow exit anytime with full dignity (no penalties, no loss)
4. Never optimize at user's expense
5. Use AI as tool only, never authority
6. Avoid over-design (dashboards, infinite feeds, layered onboarding)

### Interface Rules:
- One dominant object per screen ✓
- One primary interaction per screen ✓
- No scrolling for core action ✓
- Minimal language ✓
- Function before explanation ✓

### The Auntie Test:
> "Would Auntie Julie feel more capable after using this — or smaller?"

If smaller → design is invalid.

## Project Structure

```
DAWT-Transcribe-iOS/
├── App/
│   └── DAWT_TranscribeApp.swift          # Main app entry point
├── Views/
│   ├── HomeView.swift                    # Home screen
│   ├── TranscriptionResultView.swift     # Result display
│   ├── HistoryView.swift                 # Past transcriptions
│   └── Components/
│       ├── TranscriptCard.swift          # Segment display card
│       ├── DAWTPrimaryButton.swift       # Gold button component
│       ├── ToastView.swift               # "Shared" notification
│       ├── ShareSheet.swift              # iOS share wrapper
│       └── LoadingStateView.swift        # Transcription progress
├── Models/
│   ├── Transcription.swift               # Core data model
│   ├── Segment.swift                     # Timestamped text segment
│   └── TranscriptionState.swift          # State enum
├── Services/
│   ├── TranscriptionManager.swift        # Transcription orchestration
│   ├── AudioRecorder.swift               # Record audio
│   ├── AudioImporter.swift               # Import from Files
│   ├── TranscriptExporter.swift          # Generate TXT/MD files
│   └── BackgroundTaskManager.swift       # Background processing
├── Storage/
│   ├── TranscriptionStore.swift          # Save/load JSON
│   └── FileManager+DAWT.swift            # Directory helpers
├── DesignSystem/
│   └── DAWTDesign.swift                  # Design tokens
├── BUILD_INSTRUCTIONS.md                 # Setup guide
├── TESTING_CHECKLIST.md                  # Complete test plan
└── README.md                             # This file
```

## Technical Stack

- **Platform**: iOS 16.0+
- **Framework**: SwiftUI (native)
- **Transcription**: WhisperKit (on-device) *or stub for Phase 1*
- **Storage**: Local JSON files in Documents/DAWT/
- **No dependencies** on cloud services, analytics, or third-party SDKs

## Phase 1 Implementation Status

**Current state: COMPLETE**

- ✅ All data models implemented
- ✅ Complete design system with DAWT tokens
- ✅ All UI screens (Home, Result, History, Recording)
- ✅ Audio recording and import
- ✅ Stub transcription (2-second delay, sample data)
- ✅ Share functionality (TXT + MD export)
- ✅ Local storage with JSON persistence
- ✅ Background processing support
- ✅ Loading, error, and partial states
- ⏳ **TODO**: WhisperKit integration (Phase 3)
- ⏳ **TODO**: App icon and launch screen

**This is a working vertical slice.** You can:
1. Import audio
2. See loading state
3. Get stub transcript
4. Share as TXT/MD
5. View in history
6. Re-open past transcripts

All that's missing is real transcription (WhisperKit) and visual assets.

## Getting Started

See [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) for complete setup guide.

**Quick start:**

1. Open Xcode 15+
2. Create new iOS App project: "DAWT-Transcribe"
3. Copy all files from this directory
4. Add Info.plist keys (microphone permission, background modes)
5. Run on device (simulator can't record audio)

## Testing

See [TESTING_CHECKLIST.md](TESTING_CHECKLIST.md) for complete test plan.

**Must-test flows:**

1. ✅ Import audio → See loading → Get transcript → Share
2. ✅ View history → Open past transcription
3. ✅ Background app during transcription → Get notification
4. ✅ Record audio (device only) → Transcribe
5. ✅ Delete from history

## Export Formats

### TXT Format
```
TRANSCRIPTION
test_audio.wav — Jan 15, 2026

0:00  I love you. I care about you.
0:11  I'm here for you, always.
```

### Markdown Format
```markdown
# Transcription

**Source:** test_audio.wav
**Date:** Jan 15, 2026
**Duration:** 0:19
**Language:** EN

---

- **0:00** — I love you. I care about you.
- **0:11** — I'm here for you, always.
```

## Design System

### Colors
- Background: `#F9F7F4` (warm off-white)
- Cards: `#FFFFFF` (pure white)
- Accent: `#E8B44C` (warm gold - buttons only)
- Text Primary: `#1A1A1A` (near black)
- Text Secondary: `#666666`
- Divider: `#E0E0E0` (1px hairline)

### Typography
- Headers: System, 20pt, semibold, tracking +1.5
- Metadata: System, 11pt, medium, tracking +1.2, uppercase
- Section labels: System, 13pt, semibold, tracking +2, uppercase
- Body text: System, 16pt, regular, line spacing +6
- Button text: System, 14pt, semibold, tracking +1.5

### Spacing
- Screen padding: 24pt horizontal, 16pt vertical
- Between sections: 32pt
- Between cards: 16pt
- Card internal padding: 20pt
- Button height: 56pt

## Storage Structure

```
Documents/
└── DAWT/
    ├── Transcriptions/
    │   └── by_date/
    │       └── 2026-01-15/
    │           ├── [uuid-1].json
    │           └── [uuid-2].json
    └── Audio/ (optional source files)
```

Each JSON file:
```json
{
  "id": "uuid",
  "date": "2026-01-15T12:00:00Z",
  "duration": 19.5,
  "language": "EN",
  "sourceFile": "test_audio.wav",
  "state": "complete",
  "segments": [
    {
      "id": "uuid",
      "timestamp": "0:00 - 0:10",
      "startTime": "0:00",
      "endTime": "0:10",
      "text": "I love you. I care about you."
    }
  ]
}
```

## WhisperKit Integration (Phase 3)

Currently using stub implementation. To add real transcription:

1. Add WhisperKit package: `https://github.com/argmaxinc/WhisperKit`
2. Uncomment WhisperKit code in `TranscriptionManager.swift:91-109`
3. Initialize on app launch: `await transcriptionManager.initializeWhisperKit()`
4. Model downloads on first transcription (~150-400 MB)

**Model recommendations:**
- `tiny`: Fastest, lower accuracy
- `base`: Good balance (recommended for v1.0)
- `small`: Better accuracy, slower

## URL Transcription

The app supports transcribing from direct audio/video links:

**How it works:**
1. Tap "NEW TRANSCRIPTION"
2. Select "Transcribe from Link"
3. Paste URL (clipboard auto-detected)
4. App downloads file → transcribes → shows result

**Supported formats:**
- Direct links to: MP3, M4A, WAV, MP4, etc.
- Example: `https://example.com/audio.mp3`

**Not supported in v1.0:**
- YouTube URLs (requires separate API/service)
- Social media embeds (Instagram, TikTok, etc.)
- Streaming-only links

**Why:** Direct links only = simple, reliable, no legal complexity.

## Known Limitations (v1.0)

1. **No real transcription yet** - Using stub data until WhisperKit integrated
2. **English only** - Whisper supports many languages, but v1.0 defaults to EN
3. **No editing** - Transcripts are read-only
4. **No speaker diarization** - Can't distinguish multiple speakers
5. **iPhone only** - iPad support possible but not optimized
6. **Direct URLs only** - No YouTube/social media in v1.0

These are intentional constraints for v1.0. Future versions can expand if needed.

## What This App Will NOT Do

Following the DAWT Constitution, this app will NEVER:

- Track usage metrics or analytics
- Show ads or upsell subscriptions
- Sync to cloud (unless explicitly added and user opts in)
- Penalize you for not using it
- Show streaks, daily goals, or guilt mechanisms
- Add social features or sharing pressure
- Over-complicate with dashboards, infinite feeds, or layered onboarding
- Use AI as authority (it's a tool, not an oracle)

## Success Criteria

v1.0 is complete when:

> "I can record or import audio on my iPhone, get clean timestamped transcript within minutes, share it as TXT/MD, and access past transcriptions — all offline, at 2am, when tired."

**AND** all DAWT Constitution checkpoints pass.

## Next Steps

1. ✅ Build vertical slice with stub transcription
2. ⏳ Integrate WhisperKit
3. ⏳ Add app icon (1024x1024)
4. ⏳ Add launch screen
5. ⏳ Test on multiple devices
6. ⏳ Submit to TestFlight
7. ⏳ Release v1.0

## Contributing

This is a constitutional implementation. Any changes must:

1. Pass all DAWT Constitution tests
2. Pass the Auntie Test
3. Maintain simplicity (no feature creep)
4. Work when user is tired

If in doubt, read [DAWT_MANIFESTO.md](../DAWT_MANIFESTO.md).

## License

See main project LICENSE.

## Questions?

Read the testing checklist, build instructions, and DAWT Manifesto first. If still unclear, open an issue.

---

**Built with constitutional integrity.**
**For tired people who just need it to work.**
