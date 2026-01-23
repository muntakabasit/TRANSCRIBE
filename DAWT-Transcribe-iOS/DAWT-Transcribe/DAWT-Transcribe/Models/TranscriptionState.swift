//
//  TranscriptionState.swift
//  DAWT-Transcribe
//
//  States for the transcription process with premium 3-step flow
//

import Foundation

enum TranscriptionState: String, Codable {
    case idle
    case recording
    case importing
    case extractingAudio      // New: Video audio extraction
    case preparing            // Step 1: Preparing file
    case listening            // Step 2: Listening to audio
    case structuring          // Step 3: Structuring transcript
    case transcribing         // Legacy: Generic transcribing
    case complete
    case failed
    case partial

    var displayText: String {
        switch self {
        case .idle:
            return "Ready"
        case .recording:
            return "Recording..."
        case .importing:
            return "Importing..."
        case .extractingAudio:
            return "Extracting audio..."
        case .preparing:
            return "Preparing"
        case .listening:
            return "Listening"
        case .structuring:
            return "Structuring"
        case .transcribing:
            return "Transcribing..."
        case .complete:
            return "Transcription complete"
        case .failed:
            return "Couldn't finish right now"
        case .partial:
            return "We saved what we could"
        }
    }

    var subtitleText: String {
        switch self {
        case .extractingAudio:
            return "Getting audio ready from your video..."
        case .preparing:
            return "Step 1 of 3 · Getting everything ready"
        case .listening:
            return "Step 2 of 3 · Understanding your words"
        case .structuring:
            return "Step 3 of 3 · Creating your transcript"
        case .transcribing:
            return "You can leave this screen. We'll keep working."
        case .complete:
            return "Tap Share to send or save."
        case .partial:
            return "You can share this now or try again later."
        case .failed:
            return "Your audio is safe. Try again when you're ready."
        default:
            return ""
        }
    }

    /// Returns the progress percentage for this state (0.0 to 1.0)
    var progress: Double {
        switch self {
        case .idle, .recording, .importing:
            return 0.0
        case .extractingAudio:
            return 0.1
        case .preparing:
            return 0.33
        case .listening:
            return 0.66
        case .structuring, .transcribing:
            return 0.85
        case .complete:
            return 1.0
        case .failed, .partial:
            return 0.0
        }
    }

    /// Whether this state shows active progress
    var isProcessing: Bool {
        switch self {
        case .extractingAudio, .preparing, .listening, .structuring, .transcribing:
            return true
        default:
            return false
        }
    }
}
