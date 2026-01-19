//
//  TranscriptionResultView.swift
//  DAWT-Transcribe
//
//  Result screen showing completed transcription with segments
//

import SwiftUI

struct TranscriptionResultView: View {
    let transcription: Transcription
    @ObservedObject var transcriptionStore: TranscriptionStore
    let onNewTranscription: () -> Void

    @State private var showingShareSheet = false
    @State private var shareItems: [Any] = []
    @State private var showingToast = false

    @Environment(\.dismiss) private var dismiss

    var body: some View {
        ZStack {
            DAWTDesign.Colors.background
                .ignoresSafeArea()

            ScrollView {
                VStack(alignment: .leading, spacing: 0) {
                    // Status section
                    VStack(alignment: .leading, spacing: 8) {
                        DAWTDesign.Typography.header(transcription.state.displayText.uppercased())

                        if !transcription.state.subtitleText.isEmpty {
                            DAWTDesign.Typography.subtext(transcription.state.subtitleText)
                        }
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(.top, 20)

                    // Metadata section
                    VStack(alignment: .leading, spacing: 4) {
                        DAWTDesign.Typography.metadata("LANGUAGE: \(transcription.language)")
                        DAWTDesign.Typography.metadata("DURATION: \(transcription.durationString)")
                    }
                    .padding(.top, 24)

                    // Divider
                    Rectangle()
                        .fill(DAWTDesign.Colors.divider)
                        .frame(height: 1)
                        .padding(.vertical, 24)

                    // Transcript section
                    DAWTDesign.Typography.sectionLabel("TRANSCRIPT")
                        .padding(.bottom, 16)

                    // Segments
                    VStack(spacing: DAWTDesign.Spacing.betweenCards) {
                        ForEach(transcription.segments) { segment in
                            TranscriptCard(segment: segment)
                        }
                    }

                    // New transcription button
                    DAWTPrimaryButton(title: "NEW TRANSCRIPTION") {
                        onNewTranscription()
                        dismiss()
                    }
                    .padding(.top, 32)
                    .padding(.bottom, 40)
                }
                .padding(.horizontal, DAWTDesign.Spacing.screenHorizontal)
            }

            // Toast overlay
            ToastView(message: "Shared", isShowing: $showingToast)
        }
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Button {
                    shareTranscription()
                } label: {
                    Image(systemName: "square.and.arrow.up")
                        .foregroundColor(DAWTDesign.Colors.textPrimary)
                }
            }
        }
        .sheet(isPresented: $showingShareSheet) {
            ShareSheet(items: shareItems) {
                showingToast = true
            }
        }
    }

    private func shareTranscription() {
        let urls = TranscriptExporter.exportFiles(transcription: transcription)
        shareItems = urls
        showingShareSheet = true
    }
}

#Preview {
    NavigationStack {
        TranscriptionResultView(
            transcription: Transcription(
                date: Date(),
                duration: 19,
                language: "EN",
                sourceFile: "test_audio.wav",
                segments: [
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
                ],
                state: .complete
            ),
            transcriptionStore: TranscriptionStore(),
            onNewTranscription: {}
        )
    }
}
