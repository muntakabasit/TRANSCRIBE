//
//  TranscriptionStore.swift
//  DAWT-Transcribe
//
//  Service for saving and loading transcriptions
//

import Foundation
import Combine

class TranscriptionStore: ObservableObject {
    @Published var transcriptions: [Transcription] = []

    init() {
        setupDirectories()
        loadTranscriptions()
    }

    // MARK: - Setup

    private func setupDirectories() {
        do {
            try FileManager.default.ensureDAWTDirectories()
        } catch {
            print("Failed to create DAWT directories: \(error)")
        }
    }

    // MARK: - Save

    func save(_ transcription: Transcription) {
        do {
            // Create date directory
            let dateDirectory = FileManager.default.directoryForDate(transcription.date)
            try FileManager.default.createDirectory(at: dateDirectory, withIntermediateDirectories: true)

            // Save JSON file
            let fileURL = dateDirectory.appendingPathComponent("\(transcription.id.uuidString).json")
            let data = try JSONEncoder().encode(transcription)
            try data.write(to: fileURL)

            // Update in-memory list
            if let index = transcriptions.firstIndex(where: { $0.id == transcription.id }) {
                transcriptions[index] = transcription
            } else {
                transcriptions.append(transcription)
            }

            // Sort by date (newest first)
            transcriptions.sort { $0.date > $1.date }

        } catch {
            print("Failed to save transcription: \(error)")
        }
    }

    // MARK: - Load

    func loadTranscriptions() {
        var loaded: [Transcription] = []

        do {
            let transcriptionsDir = FileManager.default.transcriptionsDirectory

            // Check if directory exists
            guard FileManager.default.fileExists(atPath: transcriptionsDir.path) else {
                transcriptions = []
                return
            }

            // Get all date directories
            let dateDirectories = try FileManager.default.contentsOfDirectory(
                at: transcriptionsDir,
                includingPropertiesForKeys: nil
            )

            // Load transcriptions from each date directory
            for dateDirectory in dateDirectories {
                let jsonFiles = try FileManager.default.contentsOfDirectory(
                    at: dateDirectory,
                    includingPropertiesForKeys: nil
                ).filter { $0.pathExtension == "json" }

                for jsonFile in jsonFiles {
                    let data = try Data(contentsOf: jsonFile)
                    let transcription = try JSONDecoder().decode(Transcription.self, from: data)
                    loaded.append(transcription)
                }
            }

            // Sort by date (newest first)
            loaded.sort { $0.date > $1.date }
            transcriptions = loaded

        } catch {
            print("Failed to load transcriptions: \(error)")
            transcriptions = []
        }
    }

    // MARK: - Delete

    func delete(_ transcription: Transcription) {
        do {
            let dateDirectory = FileManager.default.directoryForDate(transcription.date)
            let fileURL = dateDirectory.appendingPathComponent("\(transcription.id.uuidString).json")

            try FileManager.default.removeItem(at: fileURL)

            // Remove from in-memory list
            transcriptions.removeAll { $0.id == transcription.id }

        } catch {
            print("Failed to delete transcription: \(error)")
        }
    }

    // MARK: - Get by ID

    func transcription(withID id: UUID) -> Transcription? {
        transcriptions.first { $0.id == id }
    }
}
