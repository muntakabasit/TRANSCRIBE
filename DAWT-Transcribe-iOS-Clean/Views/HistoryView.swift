//
//  HistoryView.swift
//  DAWT-Transcribe
//
//  List of past transcriptions
//

import SwiftUI

struct HistoryView: View {
    @ObservedObject var transcriptionStore: TranscriptionStore
    @State private var selectedTranscription: Transcription?
    @State private var showingDetail = false

    var body: some View {
        ZStack {
            DAWTDesign.Colors.background
                .ignoresSafeArea()

            if transcriptionStore.transcriptions.isEmpty {
                // Empty state
                VStack(spacing: 12) {
                    DAWTDesign.Typography.header("NO HISTORY")
                    DAWTDesign.Typography.subtext("Your transcriptions will appear here")
                }
            } else {
                // List of transcriptions
                ScrollView {
                    VStack(spacing: DAWTDesign.Spacing.betweenCards) {
                        ForEach(transcriptionStore.transcriptions) { transcription in
                            HistoryCard(transcription: transcription)
                                .onTapGesture {
                                    selectedTranscription = transcription
                                    showingDetail = true
                                }
                                .swipeActions(edge: .trailing, allowsFullSwipe: false) {
                                    Button(role: .destructive) {
                                        withAnimation {
                                            transcriptionStore.delete(transcription)
                                        }
                                    } label: {
                                        Label("Delete", systemImage: "trash")
                                    }
                                }
                        }
                    }
                    .padding(.horizontal, DAWTDesign.Spacing.screenHorizontal)
                    .padding(.vertical, 20)
                }
            }
        }
        .navigationTitle("HISTORY")
        .navigationBarTitleDisplayMode(.inline)
        .navigationDestination(isPresented: $showingDetail) {
            if let transcription = selectedTranscription {
                TranscriptionResultView(
                    transcription: transcription,
                    transcriptionStore: transcriptionStore,
                    onNewTranscription: {
                        showingDetail = false
                    }
                )
            }
        }
    }
}

// MARK: - History Card

struct HistoryCard: View {
    let transcription: Transcription

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // Date
            DAWTDesign.Typography.sectionLabel(transcription.dateString.uppercased())

            // Preview text
            DAWTDesign.Typography.body(""\(transcription.previewText)"")

            // Duration
            HStack {
                DAWTDesign.Typography.timestamp(transcription.durationString)
                Spacer()
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .dawtCard()
    }
}

#Preview {
    NavigationStack {
        HistoryView(transcriptionStore: {
            let store = TranscriptionStore()
            store.transcriptions = [
                Transcription(
                    date: Date(),
                    duration: 19,
                    segments: [
                        Segment(
                            timestamp: "0:00 - 0:10",
                            startTime: "0:00",
                            endTime: "0:10",
                            text: "I love you. I care about you."
                        )
                    ],
                    state: .complete
                ),
                Transcription(
                    date: Date().addingTimeInterval(-86400),
                    duration: 45,
                    segments: [
                        Segment(
                            timestamp: "0:00 - 0:10",
                            startTime: "0:00",
                            endTime: "0:10",
                            text: "Child, the current is stronger than you think."
                        )
                    ],
                    state: .complete
                )
            ]
            return store
        }())
    }
}
