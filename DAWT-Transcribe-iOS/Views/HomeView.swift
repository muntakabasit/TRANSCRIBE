//
//  HomeView.swift
//  DAWT-Transcribe
//
//  Main home screen with NEW TRANSCRIPTION button
//

import SwiftUI

struct HomeView: View {
    @StateObject private var audioImporter = AudioImporter()
    @StateObject private var audioRecorder = AudioRecorder()
    @StateObject private var transcriptionManager = TranscriptionManager()
    @StateObject private var transcriptionStore = TranscriptionStore()

    @State private var showingActionSheet = false
    @State private var showingRecordingView = false
    @State private var showingHistory = false
    @State private var navigateToResult = false

    var body: some View {
        NavigationStack {
            ZStack {
                DAWTDesign.Colors.background
                    .ignoresSafeArea()

                VStack(spacing: 0) {
                    // Title
                    HStack {
                        DAWTDesign.Typography.header("DAWT-TRANSCRIBE")
                        Spacer()
                    }
                    .padding(.top, 60)
                    .padding(.horizontal, DAWTDesign.Spacing.screenHorizontal)

                    Spacer()

                    // Primary action button
                    VStack(spacing: 24) {
                        DAWTPrimaryButton(title: "NEW TRANSCRIPTION") {
                            showingActionSheet = true
                        }

                        // History link
                        Button {
                            showingHistory = true
                        } label: {
                            DAWTDesign.Typography.link("History (\(transcriptionStore.transcriptions.count))")
                        }
                    }
                    .padding(.horizontal, DAWTDesign.Spacing.screenHorizontal)

                    Spacer()
                }

                // Loading overlay
                if transcriptionManager.isTranscribing,
                   let transcription = transcriptionManager.currentTranscription {
                    LoadingStateView(state: transcription.state)
                }
            }
            .confirmationDialog("", isPresented: $showingActionSheet, titleVisibility: .hidden) {
                Button("Record Audio") {
                    showingRecordingView = true
                }
                Button("Import Audio File") {
                    audioImporter.presentPicker()
                }
                Button("Cancel", role: .cancel) {}
            }
            .sheet(isPresented: $showingRecordingView) {
                RecordingView(
                    audioRecorder: audioRecorder,
                    onComplete: { url in
                        showingRecordingView = false
                        startTranscription(audioURL: url)
                    }
                )
            }
            .sheet(isPresented: $audioImporter.isPresented) {
                AudioDocumentPicker(
                    isPresented: $audioImporter.isPresented,
                    onPick: audioImporter.handleImport
                )
            }
            .onChange(of: audioImporter.importedURL) { url in
                if let url = url {
                    startTranscription(audioURL: url)
                }
            }
            .onChange(of: transcriptionManager.currentTranscription) { transcription in
                if let transcription = transcription, transcription.state == .complete {
                    navigateToResult = true
                }
            }
            .navigationDestination(isPresented: $navigateToResult) {
                if let transcription = transcriptionManager.currentTranscription {
                    TranscriptionResultView(
                        transcription: transcription,
                        transcriptionStore: transcriptionStore,
                        onNewTranscription: {
                            transcriptionManager.reset()
                            navigateToResult = false
                        }
                    )
                }
            }
            .navigationDestination(isPresented: $showingHistory) {
                HistoryView(transcriptionStore: transcriptionStore)
            }
        }
    }

    private func startTranscription(audioURL: URL) {
        Task {
            await transcriptionManager.transcribe(audioURL: audioURL)

            // Save to store when complete
            if let transcription = transcriptionManager.currentTranscription {
                await MainActor.run {
                    transcriptionStore.save(transcription)
                }
            }
        }
    }
}

// MARK: - Recording View

struct RecordingView: View {
    @ObservedObject var audioRecorder: AudioRecorder
    let onComplete: (URL) -> Void

    @Environment(\.dismiss) private var dismiss

    var body: some View {
        ZStack {
            DAWTDesign.Colors.background
                .ignoresSafeArea()

            VStack(spacing: 40) {
                Spacer()

                // Status
                VStack(spacing: 12) {
                    DAWTDesign.Typography.header(audioRecorder.isRecording ? "RECORDING" : "READY")

                    if audioRecorder.isRecording {
                        DAWTDesign.Typography.subtext("Tap Stop when finished")
                    }
                }

                // Record/Stop button
                Button {
                    if audioRecorder.isRecording {
                        audioRecorder.stopRecording()
                        if let url = audioRecorder.recordingURL {
                            onComplete(url)
                        }
                    } else {
                        audioRecorder.startRecording()
                    }
                } label: {
                    Circle()
                        .fill(audioRecorder.isRecording ? Color.red : DAWTDesign.Colors.accent)
                        .frame(width: 80, height: 80)
                }

                Spacer()

                // Cancel button
                Button("Cancel") {
                    if audioRecorder.isRecording {
                        audioRecorder.stopRecording()
                    }
                    dismiss()
                }
                .foregroundColor(DAWTDesign.Colors.textSecondary)
            }
            .padding()
        }
    }
}

#Preview {
    HomeView()
}
