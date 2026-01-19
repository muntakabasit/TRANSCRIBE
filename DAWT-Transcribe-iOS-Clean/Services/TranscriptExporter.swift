//
//  TranscriptExporter.swift
//  DAWT-Transcribe
//
//  Service for exporting transcripts as TXT and MD files
//

import Foundation

class TranscriptExporter {
    // Generate TXT file content
    static func generateTXT(transcription: Transcription) -> String {
        var output = "TRANSCRIPTION\n"

        if let sourceFile = transcription.sourceFile {
            output += "\(sourceFile) — \(transcription.dateString)\n\n"
        } else {
            output += "Recording — \(transcription.dateString)\n\n"
        }

        for segment in transcription.segments {
            output += "\(segment.startTime)  \(segment.text)\n"
        }

        return output
    }

    // Generate MD file content
    static func generateMarkdown(transcription: Transcription) -> String {
        var output = "# Transcription\n\n"

        let sourceName = transcription.sourceFile ?? "Recording"
        output += "**Source:** \(sourceName)  \n"
        output += "**Date:** \(transcription.dateString)  \n"
        output += "**Duration:** \(transcription.durationString)  \n"
        output += "**Language:** \(transcription.language)\n\n"
        output += "---\n\n"

        for segment in transcription.segments {
            output += "- **\(segment.startTime)** — \(segment.text)\n"
        }

        return output
    }

    // Export as files and return URLs for sharing
    static func exportFiles(transcription: Transcription) -> [URL] {
        var urls: [URL] = []

        let tempDir = FileManager.default.temporaryDirectory
        let timestamp = Int(transcription.date.timeIntervalSince1970)

        // TXT file
        let txtURL = tempDir.appendingPathComponent("transcription-\(timestamp).txt")
        if let txtData = generateTXT(transcription: transcription).data(using: .utf8) {
            try? txtData.write(to: txtURL)
            urls.append(txtURL)
        }

        // MD file
        let mdURL = tempDir.appendingPathComponent("transcription-\(timestamp).md")
        if let mdData = generateMarkdown(transcription: transcription).data(using: .utf8) {
            try? mdData.write(to: mdURL)
            urls.append(mdURL)
        }

        return urls
    }
}
