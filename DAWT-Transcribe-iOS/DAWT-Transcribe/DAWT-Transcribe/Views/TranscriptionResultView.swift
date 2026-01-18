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
    @State private var shareItemsPrepared = false

    @Environment(\.dismiss) private var dismiss

    var body: some View {
        ZStack {
            DAWTDesign.Colors.background
                .ignoresSafeArea()

            ScrollView {
                VStack(alignment: .leading, spacing: 0) {
                    // Status section
                    VStack(alignment: .leading, spacing: 8) {
                        DAWTDesign.Typography.header("Transcription complete")

                        DAWTDesign.Typography.subtext("Tap Share to send or save.")
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding(.top, 20)

                    // Metadata section
                    VStack(alignment: .leading, spacing: 4) {
                        DAWTDesign.Typography.metadata("LANGUAGE: \(transcription.language)")
                        DAWTDesign.Typography.metadata("DURATION: \(transcription.durationString)")

                        // Platform source info
                        if let platform = transcription.platform, transcription.sourceType == .url {
                            DAWTDesign.Typography.metadata("SOURCE: \(platform.icon) \(platform.displayName)")
                        }
                    }
                    .padding(.top, 24)

                    // Open Original button for URL sources
                    if let sourceURL = transcription.sourceURL,
                       transcription.sourceType == .url,
                       let url = URL(string: sourceURL) {
                        Button {
                            UIApplication.shared.open(url)
                        } label: {
                            HStack(spacing: 8) {
                                Image(systemName: "link")
                                Text("OPEN ORIGINAL")
                                    .font(.system(size: 13, weight: .semibold))
                            }
                            .foregroundColor(DAWTDesign.Colors.accent)
                            .padding(.horizontal, 16)
                            .padding(.vertical, 12)
                            .background(
                                RoundedRectangle(cornerRadius: 8)
                                    .stroke(DAWTDesign.Colors.accent, lineWidth: 1)
                            )
                        }
                        .padding(.top, 16)
                    }

                    // Divider
                    Rectangle()
                        .fill(DAWTDesign.Colors.divider)
                        .frame(height: 1)
                        .padding(.vertical, 24)

                    // Transcript section
                    DAWTDesign.Typography.sectionLabel("TRANSCRIPT")
                        .padding(.bottom, 16)

                    // Segments with hairline separators
                    VStack(spacing: 0) {
                        ForEach(Array(transcription.segments.enumerated()), id: \.element.id) { index, segment in
                            TranscriptCard(segment: segment)

                            if index < transcription.segments.count - 1 {
                                Rectangle()
                                    .fill(DAWTDesign.Colors.divider.opacity(0.3))
                                    .frame(height: 0.5)
                            }
                        }
                    }

                    // Share button (primary action)
                    DAWTPrimaryButton(title: "Share") {
                        shareTranscription()
                    }
                    .padding(.top, 32)

                    // New transcription button (secondary)
                    Button {
                        onNewTranscription()
                        dismiss()
                    } label: {
                        Text("New transcription")
                            .font(.system(size: 17))
                            .foregroundColor(DAWTDesign.Colors.textSecondary)
                            .frame(maxWidth: .infinity)
                            .padding(.vertical, 16)
                    }
                    .padding(.top, 16)
                    .padding(.bottom, 40)
                }
                .padding(.horizontal, DAWTDesign.Spacing.screenHorizontal)
            }

            // Toast overlay
            ToastView(message: "Shared", isShowing: $showingToast)
        }
        .navigationBarTitleDisplayMode(.inline)
        .sheet(isPresented: $showingShareSheet) {
            ShareSheet(items: shareItems) {
                showingToast = true
            }
        }
    }

    private func shareTranscription() {
        print("📤 Share button tapped")

        // CRITICAL: Always ensure items exist before presenting
        if shareItems.isEmpty {
            print("⚠️ shareItems is empty, preparing synchronously...")
            let items = TranscriptExporter.prepareShareItems(transcription: transcription)

            if items.isEmpty {
                print("❌ prepareShareItems returned empty, using plain text fallback")
                shareItems = [TranscriptExporter.getPlainText(transcription: transcription)]
            } else {
                print("✅ Prepared \(items.count) items")
                shareItems = items
            }
            shareItemsPrepared = true
        } else {
            print("♻️ Using cached share items (\(shareItems.count) items)")
        }

        // Final safety check
        if shareItems.isEmpty {
            print("🚨 CRITICAL: shareItems still empty, forcing plain text")
            shareItems = [TranscriptExporter.getPlainText(transcription: transcription)]
        }

        print("🎬 Presenting share sheet with \(shareItems.count) items: \(shareItems)")
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
                sourceType: .microphone,
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
