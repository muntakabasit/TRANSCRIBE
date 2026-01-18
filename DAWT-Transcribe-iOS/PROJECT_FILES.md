# DAWT-Transcribe iOS - Complete File List

## Project Structure

This document lists all files in the project with their purpose and dependencies.

## Core App

### App/
- **DAWT_TranscribeApp.swift**
  - Main app entry point with @main
  - Configures AppDelegate for notifications and background tasks
  - Dependencies: SwiftUI, UIKit

## Views

### Views/
- **HomeView.swift**
  - Main home screen with NEW TRANSCRIPTION button
  - Manages navigation to result and history
  - Handles audio import and recording flows
  - Dependencies: SwiftUI, AudioImporter, AudioRecorder, TranscriptionManager, TranscriptionStore

- **TranscriptionResultView.swift**
  - Displays completed transcription with segments
  - Share functionality
  - Navigation to new transcription
  - Dependencies: SwiftUI, Transcription, TranscriptExporter, ShareSheet, ToastView

- **HistoryView.swift**
  - Lists past transcriptions
  - Delete and re-open functionality
  - Empty state handling
  - Dependencies: SwiftUI, TranscriptionStore, Transcription

### Views/Components/
- **TranscriptCard.swift**
  - Single segment display with timestamp and text
  - White card with DAWT styling
  - Dependencies: SwiftUI, Segment, DAWTDesign

- **DAWTPrimaryButton.swift**
  - Gold accent button component
  - Follows DAWT design system
  - Dependencies: SwiftUI, DAWTDesign

- **ToastView.swift**
  - Bottom toast notification (2 seconds)
  - Used for "Shared" confirmation
  - Dependencies: SwiftUI

- **ShareSheet.swift**
  - UIKit wrapper for UIActivityViewController
  - Handles iOS share sheet
  - Dependencies: SwiftUI, UIKit

- **LoadingStateView.swift**
  - Full-screen loading overlay
  - Shows during transcription
  - Dependencies: SwiftUI, TranscriptionState, DAWTDesign

## Models

### Models/
- **Transcription.swift**
  - Core data model for transcription
  - Includes segments, metadata, state
  - Codable for JSON storage
  - Dependencies: Foundation, Segment, TranscriptionState

- **Segment.swift**
  - Single timestamped text segment
  - Helper methods for time formatting
  - Codable for JSON storage
  - Dependencies: Foundation

- **TranscriptionState.swift**
  - Enum for transcription states (idle, transcribing, complete, failed, partial)
  - Display text for each state
  - Dependencies: Foundation

## Services

### Services/
- **TranscriptionManager.swift**
  - Orchestrates transcription process
  - Currently uses stub implementation
  - WhisperKit integration code commented out for Phase 3
  - Background task management
  - Dependencies: Foundation, AVFoundation, Transcription, Segment, BackgroundTaskManager

- **AudioRecorder.swift**
  - Records audio using AVAudioRecorder
  - Handles microphone permissions
  - Saves to Documents directory
  - Dependencies: AVFoundation, SwiftUI

- **AudioImporter.swift**
  - Imports audio files from Files app
  - UIDocumentPickerViewController wrapper
  - Supports M4A, WAV, MP3, MPEG4 audio
  - Dependencies: SwiftUI, UniformTypeIdentifiers, UIKit

- **TranscriptExporter.swift**
  - Generates TXT and MD files from transcription
  - Formats according to spec
  - Creates temporary files for sharing
  - Dependencies: Foundation, Transcription

- **BackgroundTaskManager.swift**
  - Manages UIBackgroundTask for transcription
  - Shows notifications when complete
  - Singleton pattern
  - Dependencies: UIKit, UserNotifications

## Storage

### Storage/
- **TranscriptionStore.swift**
  - Saves and loads transcriptions to/from JSON
  - Manages in-memory list
  - Creates date-organized directory structure
  - Dependencies: Foundation, Transcription, FileManager+DAWT

- **FileManager+DAWT.swift**
  - Extensions for DAWT directory structure
  - Helper methods for paths
  - Directory creation
  - Dependencies: Foundation

## Design System

### DesignSystem/
- **DAWTDesign.swift**
  - Complete design system tokens
  - Colors, typography, spacing
  - View modifiers for consistent styling
  - Color hex support extension
  - Dependencies: SwiftUI

## Documentation

### Root Level
- **README.md**
  - Project overview
  - Features, principles, structure
  - Technical stack
  - Phase 1 status

- **BUILD_INSTRUCTIONS.md**
  - Complete setup guide
  - Xcode configuration
  - Info.plist setup
  - WhisperKit integration
  - Troubleshooting

- **TESTING_CHECKLIST.md**
  - Comprehensive test plan
  - Constitutional compliance tests
  - Device testing matrix
  - Edge cases
  - Release criteria

- **Info.plist.example**
  - Example Info.plist configuration
  - Required keys for permissions
  - Background modes
  - Document browser support

- **PROJECT_FILES.md**
  - This file
  - Complete file listing with dependencies

## Import Order for Xcode

When adding files to Xcode project, import in this order to avoid dependency issues:

1. **DesignSystem/**
   - DAWTDesign.swift

2. **Models/**
   - TranscriptionState.swift
   - Segment.swift
   - Transcription.swift

3. **Storage/**
   - FileManager+DAWT.swift
   - TranscriptionStore.swift

4. **Services/**
   - BackgroundTaskManager.swift
   - TranscriptExporter.swift
   - AudioRecorder.swift
   - AudioImporter.swift
   - TranscriptionManager.swift

5. **Views/Components/**
   - TranscriptCard.swift
   - DAWTPrimaryButton.swift
   - ToastView.swift
   - ShareSheet.swift
   - LoadingStateView.swift

6. **Views/**
   - HistoryView.swift
   - TranscriptionResultView.swift
   - HomeView.swift

7. **App/**
   - DAWT_TranscribeApp.swift

## File Statistics

- **Total Swift files**: 21
- **Total lines of code**: ~1,500
- **Views**: 8 files
- **Models**: 3 files
- **Services**: 5 files
- **Storage**: 2 files
- **Design System**: 1 file
- **App**: 1 file
- **Documentation**: 4 markdown files

## Key Dependencies

### External (Phase 3 - Optional)
- WhisperKit: https://github.com/argmaxinc/WhisperKit
  - For real on-device transcription
  - Not included in Phase 1

### Internal
- No internal dependencies between modules beyond what's listed above
- Clean architecture with clear separation of concerns
- Models don't depend on Views or Services
- Services depend on Models but not Views
- Views depend on everything (presentation layer)

## Constitutional Compliance

Every file follows DAWT Constitution principles:
- ✅ Simple, focused purpose
- ✅ No unnecessary complexity
- ✅ Works when user is tired
- ✅ No shame mechanisms
- ✅ Function before explanation

## Next Steps

1. Import all files into Xcode project
2. Configure Info.plist
3. Build and test Phase 1 vertical slice
4. Integrate WhisperKit (Phase 3)
5. Add app icon and launch screen
6. Release v1.0

See BUILD_INSTRUCTIONS.md for detailed setup steps.
