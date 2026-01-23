//
//  TranscriptionManager.swift
//  DAWT-Transcribe
//
//  Service for managing transcription with premium 3-step progress
//  NOTE: This uses API backend for transcription
//

import Foundation
import AVFoundation
import Combine

class TranscriptionManager: ObservableObject {
    @Published var currentTranscription: Transcription?
    @Published var isTranscribing = false

    // MARK: - Transcription with 3-Step Progress

    func transcribe(audioURL: URL, sourceType: SourceType = .file, isVideoSource: Bool = false) async {
        // Clear any pending notifications from previous jobs
        BackgroundTaskManager.shared.clearPendingNotifications()

        // Start background task
        BackgroundTaskManager.shared.beginBackgroundTask(name: "Transcription")

        await MainActor.run {
            isTranscribing = true
            currentTranscription = Transcription(
                date: Date(),
                sourceFile: audioURL.lastPathComponent,
                sourceType: sourceType,
                state: isVideoSource ? .extractingAudio : .preparing
            )
        }

        do {
            // Step 1: Preparing (0.33 progress)
            if !isVideoSource {
                await updateState(.preparing)
                try await Task.sleep(nanoseconds: 500_000_000) // 0.5s for UX smoothness
            }

            // Get audio duration
            let asset = AVAsset(url: audioURL)
            let duration = try await asset.load(.duration).seconds

            // Step 2: Listening (0.66 progress)
            await updateState(.listening)

            // Use backend API for transcription
            let response = try await APIClient.transcribeAudioFile(audioURL: audioURL)
            let segments = APIClient.convertToSegments(from: response)

            // Step 3: Structuring (0.85 progress)
            await updateState(.structuring)
            try await Task.sleep(nanoseconds: 300_000_000) // 0.3s for UX smoothness

            // Complete
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

            // Haptic for completion (only one haptic, on success)
            HapticsManager.shared.transcriptionCompleted()

            // Notify user if opted in and app is backgrounded
            let notifyPreference = UserDefaults.standard.bool(forKey: "notifyWhenReady")
            if notifyPreference {
                BackgroundTaskManager.shared.notifyTranscriptionComplete(success: true, duration: duration)
            }

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

            // Haptic for failure
            HapticsManager.shared.transcriptionFailed()

            // Notify user of failure if opted in and backgrounded
            let notifyPreference = UserDefaults.standard.bool(forKey: "notifyWhenReady")
            if notifyPreference {
                BackgroundTaskManager.shared.notifyTranscriptionComplete(success: false)
            }
        }

        // End background task
        BackgroundTaskManager.shared.endBackgroundTask()
    }

    private func updateState(_ state: TranscriptionState) async {
        await MainActor.run {
            guard var transcription = currentTranscription else { return }
            transcription.state = state
            currentTranscription = transcription
        }
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
        } catch {
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
