//
//  TranscriptionState.swift
//  DAWT-Transcribe
//
//  States for the transcription process
//

import Foundation

enum TranscriptionState: String, Codable {
    case idle
    case recording
    case importing
    case transcribing
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
            return "Importing audio..."
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
}
