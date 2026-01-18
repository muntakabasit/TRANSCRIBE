//
//  Transcription.swift
//  DAWT-Transcribe
//
//  Core data model for a transcription
//

import Foundation

struct Transcription: Identifiable, Codable, Equatable {
    let id: UUID
    let date: Date
    let duration: TimeInterval?
    let language: String
    let sourceFile: String?
    var segments: [Segment]
    var state: TranscriptionState

    var isComplete: Bool {
        state == .complete
    }

    var isFailed: Bool {
        state == .failed
    }

    var isPartial: Bool {
        state == .partial
    }

    init(
        id: UUID = UUID(),
        date: Date = Date(),
        duration: TimeInterval? = nil,
        language: String = "EN",
        sourceFile: String? = nil,
        segments: [Segment] = [],
        state: TranscriptionState = .idle
    ) {
        self.id = id
        self.date = date
        self.duration = duration
        self.language = language
        self.sourceFile = sourceFile
        self.segments = segments
        self.state = state
    }

    // Formatted duration string (e.g., "0:19")
    var durationString: String {
        guard let duration = duration else { return "—" }
        let totalSeconds = Int(duration)
        let minutes = totalSeconds / 60
        let seconds = totalSeconds % 60
        return String(format: "%d:%02d", minutes, seconds)
    }

    // Formatted date string
    var dateString: String {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        formatter.timeStyle = .none
        return formatter.string(from: date)
    }

    // First line of transcript for preview
    var previewText: String {
        guard let firstSegment = segments.first else {
            return "No transcript available"
        }
        let maxLength = 50
        if firstSegment.text.count > maxLength {
            return String(firstSegment.text.prefix(maxLength)) + "..."
        }
        return firstSegment.text
    }

    // Full transcript as plain text
    var fullText: String {
        segments.map { segment in
            "\(segment.startTime)  \(segment.text)"
        }.joined(separator: "\n")
    }
}
