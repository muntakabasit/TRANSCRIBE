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

    // Get plain text transcript for sharing
    static func getPlainText(transcription: Transcription) -> String {
        if transcription.segments.isEmpty {
            return "No transcript available"
        }

        var output = ""
        for segment in transcription.segments {
            output += "\(segment.text)\n"
        }

        let result = output.trimmingCharacters(in: .whitespacesAndNewlines)
        return result.isEmpty ? "No transcript available" : result
    }

    // Export as files and return share items (String + URLs)
    // GUARANTEE: Always returns at least plain text (never empty array)
    static func prepareShareItems(transcription: Transcription) -> [Any] {
        var items: [Any] = []

        // CRITICAL: Always include plain text transcript first
        let plainText = getPlainText(transcription: transcription)
        print("📝 Plain text length: \(plainText.count) characters")

        // Safety check: ensure we have text to share
        guard !plainText.isEmpty else {
            print("🚨 Plain text is empty, returning fallback")
            return ["No transcript available"]
        }

        items.append(plainText)
        print("✅ Added plain text to items (count: \(items.count))")

        // Try to create files
        let tempDir = FileManager.default.temporaryDirectory

        // Generate filename: Transcribe_YYYY-MM-DD_HHMM_<Source>
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-MM-dd_HHmm"
        let dateString = dateFormatter.string(from: transcription.date)

        let sourceType = transcription.sourceType.rawValue.capitalized
        let baseFilename = "Transcribe_\(dateString)_\(sourceType)"

        // TXT file
        let txtURL = tempDir.appendingPathComponent("\(baseFilename).txt")
        print("📄 Attempting to create TXT at: \(txtURL.path)")
        if let txtData = generateTXT(transcription: transcription).data(using: .utf8) {
            do {
                try txtData.write(to: txtURL, options: .atomic)
                if FileManager.default.fileExists(atPath: txtURL.path) {
                    print("✅ TXT file created and verified")
                    items.append(txtURL)
                } else {
                    print("⚠️ TXT file write succeeded but file doesn't exist")
                }
            } catch {
                print("❌ Failed to write TXT file: \(error)")
            }
        } else {
            print("❌ Failed to convert TXT to data")
        }

        // MD file
        let mdURL = tempDir.appendingPathComponent("\(baseFilename).md")
        print("📄 Attempting to create MD at: \(mdURL.path)")
        if let mdData = generateMarkdown(transcription: transcription).data(using: .utf8) {
            do {
                try mdData.write(to: mdURL, options: .atomic)
                if FileManager.default.fileExists(atPath: mdURL.path) {
                    print("✅ MD file created and verified")
                    items.append(mdURL)
                } else {
                    print("⚠️ MD file write succeeded but file doesn't exist")
                }
            } catch {
                print("❌ Failed to write MD file: \(error)")
            }
        } else {
            print("❌ Failed to convert MD to data")
        }

        print("📦 Total items prepared: \(items.count)")
        return items
    }
}
