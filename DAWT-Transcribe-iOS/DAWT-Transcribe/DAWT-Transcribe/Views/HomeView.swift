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
    @State private var showingURLSheet = false
    @State private var showingHistory = false
    @State private var navigateToResult = false
    @State private var isTranscribingURL = false
    @State private var urlErrorMessage: String?
    @State private var showingURLError = false

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
                        DAWTPrimaryButton(title: "New transcription") {
                            showingActionSheet = true
                        }

                        // History link
                        Button {
                            showingHistory = true
                        } label: {
                            DAWTDesign.Typography.link("History →")
                        }
                    }
                    .padding(.horizontal, DAWTDesign.Spacing.screenHorizontal)

                    Spacer()
                }

                // Loading overlay
                if transcriptionManager.isTranscribing,
                   let transcription = transcriptionManager.currentTranscription {
                    LoadingStateView(state: transcription.state)
                } else if isTranscribingURL {
                    ZStack {
                        Color.black.opacity(0.4)
                            .ignoresSafeArea()

                        VStack(spacing: 16) {
                            ProgressView()
                                .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                .scaleEffect(1.5)

                            Text("Transcribing from URL...")
                                .font(.system(size: 17, weight: .medium))
                                .foregroundColor(.white)

                            Text("This may take a moment")
                                .font(.system(size: 14))
                                .foregroundColor(.white.opacity(0.8))
                        }
                        .padding(32)
                        .background(
                            RoundedRectangle(cornerRadius: 16)
                                .fill(Color(white: 0.15))
                        )
                    }
                }
            }
            .confirmationDialog("", isPresented: $showingActionSheet, titleVisibility: .hidden) {
                Button("Record Audio") {
                    showingRecordingView = true
                }
                Button("Import Audio File") {
                    audioImporter.presentPicker()
                }
                Button("Transcribe from Link") {
                    showingURLSheet = true
                }
                Button("Cancel", role: .cancel) {}
            }
            .sheet(isPresented: $showingRecordingView) {
                RecordingView(
                    audioRecorder: audioRecorder,
                    onComplete: { url in
                        showingRecordingView = false
                        startTranscription(audioURL: url, sourceType: .microphone)
                    }
                )
            }
            .sheet(isPresented: $audioImporter.isPresented) {
                AudioDocumentPicker(
                    isPresented: $audioImporter.isPresented,
                    onPick: audioImporter.handleImport
                )
            }
            .sheet(isPresented: $showingURLSheet) {
                URLTranscriptionSheet(isPresented: $showingURLSheet) { url in
                    handleURLTranscription(url: url)
                }
                .presentationDetents([.medium])
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
            .alert("Transcription Failed", isPresented: $showingURLError) {
                Button("OK", role: .cancel) { }
            } message: {
                Text(urlErrorMessage ?? "Couldn't transcribe from URL. Please try again.")
            }
        }
    }

    private func startTranscription(audioURL: URL, sourceType: SourceType = .file) {
        Task {
            await transcriptionManager.transcribe(
                audioURL: audioURL,
                sourceType: sourceType
            )

            // Save to store when complete
            if let transcription = transcriptionManager.currentTranscription {
                await MainActor.run {
                    transcriptionStore.save(transcription)
                }
            }
        }
    }

    private func handleURLTranscription(url: URL) {
        Task {
            await MainActor.run {
                isTranscribingURL = true
            }

            do {
                // Detect platform from URL
                let urlString = url.absoluteString
                let platform = Platform.detect(from: urlString)

                print("🔗 Transcribing URL: \(urlString)")
                print("🎯 Detected platform: \(platform.displayName)")

                // Call backend API to transcribe URL
                let response = try await APIClient.transcribeURL(url: urlString)

                print("✅ Got response from backend")
                print("📝 Segments count: \(response.segments?.count ?? 0)")

                // Convert API response to segments
                let segments = APIClient.convertToSegments(from: response)

                // Create transcription with URL metadata
                let transcription = Transcription(
                    duration: response.duration,
                    language: response.language ?? "EN",
                    sourceType: .url,
                    sourceURL: urlString,
                    platform: platform,
                    segments: segments,
                    state: .complete
                )

                // Save to store
                await MainActor.run {
                    isTranscribingURL = false
                    transcriptionStore.save(transcription)
                    transcriptionManager.currentTranscription = transcription
                    navigateToResult = true
                }

            } catch let error as APIError {
                // Show user-friendly error
                print("❌ API Error: \(error.userMessage)")
                await MainActor.run {
                    isTranscribingURL = false
                    urlErrorMessage = error.userMessage
                    showingURLError = true
                }
            } catch {
                print("❌ Network Error: \(error.localizedDescription)")
                await MainActor.run {
                    isTranscribingURL = false
                    urlErrorMessage = "Network error: \(error.localizedDescription)"
                    showingURLError = true
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
