# DAWT-Transcribe Testing Checklist

## Phase 1: Core Flow Testing

### Home Screen
- [ ] App launches successfully
- [ ] "DAWT-TRANSCRIBE" title displays correctly
- [ ] "NEW TRANSCRIPTION" button is centered and prominent
- [ ] "History" link displays with count (0 on first launch)
- [ ] Background color matches design (#F9F7F4)

### Action Sheet
- [ ] Tapping "NEW TRANSCRIPTION" shows action sheet
- [ ] Action sheet has three options: Record Audio, Import Audio File, Cancel
- [ ] Tapping "Cancel" dismisses action sheet
- [ ] Tapping outside action sheet dismisses it

### Audio Import Flow
- [ ] Tapping "Import Audio File" opens Files picker
- [ ] Files picker shows audio files (M4A, WAV, MP3)
- [ ] Selecting audio file closes picker
- [ ] Loading state appears immediately after selection
- [ ] Loading shows "Transcribing..." message
- [ ] Subtitle says "You can leave this screen. We'll keep working."

### Audio Recording Flow (Device Only)
- [ ] Tapping "Record Audio" shows recording screen
- [ ] Microphone permission prompt appears (first time)
- [ ] Red circle appears after permission granted
- [ ] "RECORDING" status displays
- [ ] Tapping circle stops recording
- [ ] Recording saves and starts transcription
- [ ] Cancel button works and dismisses recording screen

### Transcription Result Screen
- [ ] Navigates automatically when transcription completes
- [ ] Status shows "TRANSCRIPTION COMPLETE"
- [ ] Subtitle says "Tap Share to send or save."
- [ ] Language displays: "LANGUAGE: EN"
- [ ] Duration displays: "DURATION: 0:19" (or actual duration)
- [ ] Divider line appears correctly
- [ ] "TRANSCRIPT" section label appears
- [ ] Segments display in white cards with padding
- [ ] Each segment shows timestamp (e.g., "0:00 - 0:10")
- [ ] Each segment shows transcript text
- [ ] Multiple segments have spacing between them
- [ ] "NEW TRANSCRIPTION" button appears at bottom
- [ ] Back button (←) appears in nav bar
- [ ] Share button (↑) appears in nav bar

### Share Functionality
- [ ] Tapping share button opens iOS share sheet
- [ ] Share sheet shows both TXT and MD files
- [ ] TXT file contains correct format:
  ```
  TRANSCRIPTION
  filename — date

  00:13  text...
  ```
- [ ] MD file contains correct format with headers and metadata
- [ ] Can share to Messages, Mail, Files, etc.
- [ ] After sharing, toast appears: "Shared"
- [ ] Toast disappears after 2 seconds

### History Screen
- [ ] Tapping "History" navigates to history screen
- [ ] Empty state shows "NO HISTORY" when no transcriptions
- [ ] After transcription, history count updates
- [ ] History items display with date, preview text, and duration
- [ ] Tapping history item opens that transcription
- [ ] Swiping left shows delete button
- [ ] Confirming delete removes item
- [ ] History list ordered by date (newest first)

### Navigation
- [ ] Back button returns from result to home
- [ ] Back button returns from history to home
- [ ] "NEW TRANSCRIPTION" button from result returns to home
- [ ] Navigation stack doesn't build up incorrectly

## Phase 2: State Management

### Loading States
- [ ] Loading overlay appears during transcription
- [ ] Loading overlay blocks interaction
- [ ] Progress spinner animates
- [ ] Status text updates appropriately
- [ ] User can background app during transcription

### Error States
- [ ] Invalid audio file shows failed state
- [ ] Failed state shows: "Couldn't finish right now"
- [ ] Failed state shows: "Your audio is safe. Try again when you're ready."
- [ ] Can navigate away from failed state
- [ ] Can try new transcription after failure

### Partial States (if implemented)
- [ ] Interrupted transcription shows partial state
- [ ] Partial state shows: "We saved what we could"
- [ ] Can share partial transcription
- [ ] Partial transcription saves to history

## Phase 3: Data Persistence

### Storage
- [ ] Transcriptions persist between app launches
- [ ] History loads previous transcriptions correctly
- [ ] JSON files created in Documents/DAWT/Transcriptions/by_date/
- [ ] Directory structure follows spec
- [ ] Files organized by date (YYYY-MM-DD)
- [ ] Each transcription has unique UUID filename

### Data Integrity
- [ ] Segment timestamps match audio
- [ ] Full text property works correctly
- [ ] Preview text truncates at 50 chars
- [ ] Duration string formats correctly (M:SS)
- [ ] Date string formats correctly

## Phase 4: Background Processing

### Backgrounding
- [ ] Start transcription, background app
- [ ] Transcription continues in background
- [ ] Notification appears when complete
- [ ] Notification content correct: "Transcription complete"
- [ ] Tapping notification opens app
- [ ] Result available when returning to app

### Notifications
- [ ] Permission prompt appears on first launch
- [ ] Notification only shows when app is backgrounded
- [ ] No notification when app in foreground
- [ ] Notification shows even if task takes >30 seconds

## Phase 5: WhisperKit Integration (when implemented)

### Model Loading
- [ ] First transcription downloads model (if needed)
- [ ] Progress indication during model download
- [ ] Model persists for subsequent uses
- [ ] App handles model download failure gracefully

### Transcription Quality
- [ ] Transcription accuracy acceptable for clear speech
- [ ] Timestamps align with audio
- [ ] Handles multiple speakers reasonably
- [ ] Handles background noise reasonably
- [ ] Performance acceptable (<30 seconds for 1 minute audio)

## Phase 6: Design System Compliance

### Typography
- [ ] Headers: 20pt, semibold, tracking +1.5
- [ ] Metadata: 11pt, medium, tracking +1.2, uppercase
- [ ] Section labels: 13pt, semibold, tracking +2, uppercase
- [ ] Body text: 16pt, regular, line spacing +6
- [ ] Button text: 14pt, semibold, tracking +1.5
- [ ] Timestamps: 12pt, #888888

### Colors
- [ ] Background: #F9F7F4
- [ ] Cards: #FFFFFF
- [ ] Accent (buttons): #E8B44C
- [ ] Text primary: #1A1A1A
- [ ] Text secondary: #666666
- [ ] Divider: #E0E0E0, 1px

### Spacing
- [ ] Screen padding: 24pt horizontal, 16pt vertical
- [ ] Between sections: 32pt
- [ ] Between cards: 16pt
- [ ] Card padding: 20pt
- [ ] Button height: 56pt

### Layout
- [ ] One dominant object per screen
- [ ] No scrolling required for primary action
- [ ] Touch targets minimum 44x44pt
- [ ] Consistent spacing throughout

## DAWT Constitution Compliance

### Core Principles
- [ ] **Works when tired**: Can complete flow at 2am without thinking
- [ ] **No shame**: Zero guilt mechanisms, no streaks, no penalties
- [ ] **Exit with dignity**: Can leave anytime, all progress saved
- [ ] **No dark patterns**: No tricks, no manipulation, no forced engagement
- [ ] **AI as tool**: Transcription is utility, not authority

### Interface Principles
- [ ] One dominant object per screen ✓
- [ ] One primary interaction per screen ✓
- [ ] No scrolling for core action ✓
- [ ] Minimal language ✓
- [ ] Function before explanation ✓

### Auntie Test
- [ ] Would Auntie Julie feel MORE capable after using?
- [ ] Would she feel empowered, not diminished?
- [ ] Would she trust the app?
- [ ] Would she recommend it to others?

If Auntie test fails on ANY point → Design is invalid. Fix it.

## Device Testing Matrix

### iOS Versions
- [ ] iOS 16.0 (minimum)
- [ ] iOS 17.0
- [ ] Latest iOS version

### Device Sizes
- [ ] iPhone SE (small screen)
- [ ] iPhone 15 Pro (standard)
- [ ] iPhone 15 Pro Max (large)
- [ ] iPad (if supporting)

### Accessibility
- [ ] VoiceOver navigation works
- [ ] Dynamic Type scaling works
- [ ] Minimum touch targets (44x44pt)
- [ ] Color contrast meets WCAG AA
- [ ] Works in light and dark mode (if supporting dark mode)

## Performance Testing

### Memory
- [ ] No memory leaks during transcription
- [ ] Memory usage acceptable (<500 MB during transcription)
- [ ] Memory releases after transcription complete

### Battery
- [ ] Battery drain acceptable during transcription
- [ ] No excessive drain when idle
- [ ] Background processing doesn't kill battery

### Storage
- [ ] App size reasonable
- [ ] Transcription files not excessively large
- [ ] Old transcriptions can be deleted to free space

## Edge Cases

### Empty States
- [ ] No transcriptions: Shows empty state
- [ ] No segments: Handles gracefully
- [ ] No audio: Shows appropriate error

### Boundary Conditions
- [ ] Very short audio (1 second)
- [ ] Long audio (10+ minutes)
- [ ] Large history (100+ transcriptions)
- [ ] Special characters in filenames

### Interruptions
- [ ] Phone call during transcription
- [ ] Low battery during transcription
- [ ] Low storage during save
- [ ] App termination during transcription

### Permissions
- [ ] Microphone denied: Shows error, explains how to fix
- [ ] Notifications denied: App still works, just no notifications
- [ ] Files access denied: Shows error

## Release Readiness

### Pre-release
- [ ] All Phase 1 tests pass
- [ ] All DAWT Constitution checks pass
- [ ] No known critical bugs
- [ ] App icon added (1024x1024)
- [ ] Launch screen added
- [ ] App Store screenshots prepared
- [ ] Privacy policy prepared (if needed)

### App Store Submission
- [ ] Bundle identifier configured
- [ ] Version number set (1.0.0)
- [ ] Build number incremented
- [ ] Signing certificates valid
- [ ] Archive created successfully
- [ ] TestFlight upload successful
- [ ] TestFlight testing complete

## Success Criteria

v1.0 is complete and ready for release when:

> "I can record or import audio on my iPhone, get clean timestamped transcript within minutes, share it as TXT/MD, and access past transcriptions — all offline, at 2am, when tired."

**AND** all constitutional checkpoints pass.

If this statement is false or any checkpoint fails → NOT ready for release.
