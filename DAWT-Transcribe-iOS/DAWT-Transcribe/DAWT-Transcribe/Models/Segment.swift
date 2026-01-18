//
//  Segment.swift
//  DAWT-Transcribe
//
//  A single timestamped segment of transcribed text
//

import Foundation

struct Segment: Identifiable, Codable, Equatable {
    let id: UUID
    let timestamp: String      // e.g., "0:00 - 0:10"
    let startTime: String      // e.g., "0:00"
    let endTime: String        // e.g., "0:10"
    let text: String

    init(id: UUID = UUID(), timestamp: String, startTime: String, endTime: String, text: String) {
        self.id = id
        self.timestamp = timestamp
        self.startTime = startTime
        self.endTime = endTime
        self.text = text
    }

    // Helper to create segment from start/end times in seconds
    static func from(startSeconds: Double, endSeconds: Double, text: String) -> Segment {
        let startTime = Self.formatTime(startSeconds)
        let endTime = Self.formatTime(endSeconds)
        let timestamp = "\(startTime) - \(endTime)"

        return Segment(
            timestamp: timestamp,
            startTime: startTime,
            endTime: endTime,
            text: text
        )
    }

    private static func formatTime(_ seconds: Double) -> String {
        let totalSeconds = Int(seconds)
        let minutes = totalSeconds / 60
        let secs = totalSeconds % 60
        return String(format: "%d:%02d", minutes, secs)
    }
}
