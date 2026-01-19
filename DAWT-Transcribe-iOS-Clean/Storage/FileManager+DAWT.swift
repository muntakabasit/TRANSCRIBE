//
//  FileManager+DAWT.swift
//  DAWT-Transcribe
//
//  FileManager extensions for DAWT directory structure
//

import Foundation

extension FileManager {
    // Get DAWT base directory
    var dawtDirectory: URL {
        let documentsDirectory = urls(for: .documentDirectory, in: .userDomainMask)[0]
        return documentsDirectory.appendingPathComponent("DAWT")
    }

    // Get transcriptions directory
    var transcriptionsDirectory: URL {
        dawtDirectory.appendingPathComponent("Transcriptions/by_date")
    }

    // Get audio directory
    var audioDirectory: URL {
        dawtDirectory.appendingPathComponent("Audio")
    }

    // Ensure DAWT directories exist
    func ensureDAWTDirectories() throws {
        try createDirectory(at: transcriptionsDirectory, withIntermediateDirectories: true)
        try createDirectory(at: audioDirectory, withIntermediateDirectories: true)
    }

    // Get directory for a specific date
    func directoryForDate(_ date: Date) -> URL {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        let dateString = formatter.string(from: date)
        return transcriptionsDirectory.appendingPathComponent(dateString)
    }
}
