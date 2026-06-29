//
//  DAWT_TranscribeTests.swift
//  DAWT-TranscribeTests
//
//  Created by Abdul Basit Muntaka on 16/01/2026.
//

import Foundation
import Testing
@testable import DAWT_Transcribe

struct DAWT_TranscribeTests {
    private func makeTranscription(segments: [String]) -> Transcription {
        Transcription(
            date: Date(),
            duration: 19,
            language: "EN",
            sourceFile: "test_audio.wav",
            sourceType: .microphone,
            segments: segments.enumerated().map { index, text in
                Segment(
                    timestamp: "\(index):00 - \(index):01",
                    startTime: "\(index):00",
                    endTime: "\(index):01",
                    text: text
                )
            },
            state: .complete
        )
    }

    @Test func validTranscriptProducesPreparedPayload() async throws {
        let transcription = makeTranscription(segments: ["Visible transcript text"])

        let payload = TranscriptionResultView.prepareSharePayload(for: transcription)

        #expect(payload != nil)
        #expect(payload?.activityItems.isEmpty == false)
    }

    @Test func emptySegmentsRejectSharePayload() async throws {
        let transcription = makeTranscription(segments: [])

        let payload = TranscriptionResultView.prepareSharePayload(for: transcription)

        #expect(payload == nil)
    }

    @Test func whitespaceOnlyTranscriptRejectsSharePayload() async throws {
        let transcription = makeTranscription(segments: ["   \n  "])

        let payload = TranscriptionResultView.prepareSharePayload(for: transcription)

        #expect(payload == nil)
    }

    @Test func placeholderTranscriptRejectsSharePayload() async throws {
        let transcription = makeTranscription(segments: [TranscriptionResultView.noTranscriptPlaceholder])

        let payload = TranscriptionResultView.prepareSharePayload(for: transcription)

        #expect(payload == nil)
    }

    @Test func canonicalTranscriptPreservesUnicodeAndLineBreaks() async throws {
        let transcription = makeTranscription(segments: ["Line one", "Line two — café ☕️"])

        let text = TranscriptionResultView.canonicalTranscriptText(for: transcription)

        #expect(text == "Line one\nLine two — café ☕️")
    }

    @Test func repeatedSharePayloadPreparationUsesCurrentTranscriptContent() async throws {
        let first = makeTranscription(segments: ["First transcript"])
        let second = makeTranscription(segments: ["Second transcript"])

        let firstPayload = TranscriptionResultView.prepareSharePayload(for: first)
        let secondPayload = TranscriptionResultView.prepareSharePayload(for: second)

        #expect(firstPayload?.activityItems.first as? String == "First transcript")
        #expect(secondPayload?.activityItems.first as? String == "Second transcript")
    }

}
