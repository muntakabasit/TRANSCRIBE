//
//  TranscriptionManager.swift
//  DAWT-Transcribe
//
//  Service for managing transcription with WhisperKit
//  NOTE: This uses WhisperKit for on-device transcription
//  Install via: File > Add Package Dependencies > https://github.com/argmaxinc/WhisperKit
//

import Foundation
import AVFoundation
import Combine

class TranscriptionManager: ObservableObject {
    @Published var currentTranscription: Transcription?
    @Published var isTranscribing = false

    // MARK: - Transcription

    func transcribe(audioURL: URL, sourceType: SourceType = .file) async {
        // Start background task
        BackgroundTaskManager.shared.beginBackgroundTask(name: "Transcription")

        await MainActor.run {
            isTranscribing = true
            currentTranscription = Transcription(
                date: Date(),
                sourceFile: audioURL.lastPathComponent,
                sourceType: sourceType,
                state: .transcribing
            )
        }

        do {
            // Get audio duration
            let asset = AVAsset(url: audioURL)
            let duration = try await asset.load(.duration).seconds

            // Use backend API for transcription
            let response = try await APIClient.transcribeAudioFile(audioURL: audioURL)
            let segments = APIClient.convertToSegments(from: response)

            await MainActor.run {
                let baseTranscription = currentTranscription ?? Transcription()
                currentTranscription = Transcription(
                    id: baseTranscription.id,
                    date: baseTranscription.date,
                    duration: duration,
                    language: baseTranscription.language,
                    sourceFile: baseTranscription.sourceFile,
                    sourceType: baseTranscription.sourceType,
                    sourceURL: baseTranscription.sourceURL,
                    platform: baseTranscription.platform,
                    segments: segments,
                    state: .complete
                )
                isTranscribing = false
            }

            // Notify user if app is backgrounded
            BackgroundTaskManager.shared.notifyTranscriptionComplete(success: true)

        } catch {
            await MainActor.run {
                let baseTranscription = currentTranscription ?? Transcription()
                currentTranscription = Transcription(
                    id: baseTranscription.id,
                    date: baseTranscription.date,
                    duration: baseTranscription.duration,
                    language: baseTranscription.language,
                    sourceFile: baseTranscription.sourceFile,
                    sourceType: baseTranscription.sourceType,
                    sourceURL: baseTranscription.sourceURL,
                    platform: baseTranscription.platform,
                    segments: baseTranscription.segments,
                    state: .failed
                )
                isTranscribing = false
            }

            // Notify user of failure if app is backgrounded
            BackgroundTaskManager.shared.notifyTranscriptionComplete(success: false)
        }

        // End background task
        BackgroundTaskManager.shared.endBackgroundTask()
    }

    // MARK: - Stub Implementation (Phase 1)

    private func transcribeWithStub(audioURL: URL) async throws -> [Segment] {
        // Simulate transcription delay
        try await Task.sleep(nanoseconds: 2_000_000_000) // 2 seconds

        // Return stub segments for testing
        return [
            Segment(
                timestamp: "0:00 - 0:10",
                startTime: "0:00",
                endTime: "0:10",
                text: "I love you. I care about you. I'm thinking of you right now."
            ),
            Segment(
                timestamp: "0:11 - 0:17",
                startTime: "0:11",
                endTime: "0:17",
                text: "I'm here for you, always."
            )
        ]
    }

    // MARK: - WhisperKit Integration
    #if WHISPERKIT_ENABLED
    private var whisperKit: WhisperKit?

    func initializeWhisperKit() async {
        do {
            whisperKit = try await WhisperKit()
            print("WhisperKit initialized successfully")
        } catch {
            print("Failed to initialize WhisperKit: \(error)")
        }
    }

    private func transcribeWithWhisperKit(audioURL: URL) async throws -> [Segment] {
        guard let whisperKit = whisperKit else {
            throw TranscriptionError.notInitialized
        }

        let result = try await whisperKit.transcribe(audioPath: audioURL.path)

        return result.segments.map { segment in
            Segment.from(
                startSeconds: segment.start,
                endSeconds: segment.end,
                text: segment.text
            )
        }
    }
    #endif

    // MARK: - Reset

    func reset() {
        currentTranscription = nil
        isTranscribing = false
    }
}

enum TranscriptionError: Error {
    case notInitialized
    case failed
}
