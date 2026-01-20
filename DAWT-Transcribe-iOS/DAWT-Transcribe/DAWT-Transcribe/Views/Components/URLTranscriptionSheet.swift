//
//  URLTranscriptionSheet.swift
//  DAWT-Transcribe
//
//  Bottom sheet for URL transcription input
//

import SwiftUI

struct URLTranscriptionSheet: View {
    @Binding var isPresented: Bool
    let onSubmit: (URL) -> Void

    @State private var urlText: String = ""
    @State private var errorMessage: String?
    @FocusState private var isFieldFocused: Bool

    var body: some View {
        ZStack {
            DAWTDesign.Colors.background
                .ignoresSafeArea()

            VStack(spacing: 0) {
                // Handle (drag indicator)
                RoundedRectangle(cornerRadius: 2.5)
                    .fill(Color.gray.opacity(0.3))
                    .frame(width: 36, height: 5)
                    .padding(.top, 8)
                    .padding(.bottom, 20)

                // Title
                HStack {
                    DAWTDesign.Typography.header("Paste a link")
                    Spacer()
                }
                .padding(.horizontal, DAWTDesign.Spacing.screenHorizontal)
                .padding(.bottom, 20)

                // URL Field
                VStack(alignment: .leading, spacing: 8) {
                    TextField("https://example.com/audio.mp3", text: $urlText)
                        .textFieldStyle(.plain)
                        .keyboardType(.URL)
                        .autocapitalization(.none)
                        .autocorrectionDisabled()
                        .focused($isFieldFocused)
                        .padding(16)
                        .background(DAWTDesign.Colors.cardBackground)
                        .cornerRadius(12)
                        .overlay(
                            RoundedRectangle(cornerRadius: 12)
                                .stroke(
                                    errorMessage != nil ? Color.red.opacity(0.6) :
                                    isFieldFocused ? DAWTDesign.Colors.accent :
                                    DAWTDesign.Colors.divider,
                                    lineWidth: isFieldFocused ? 2 : 1
                                )
                        )

                    // Helper or error text
                    if let error = errorMessage {
                        Text(error)
                            .font(.system(size: 13))
                            .foregroundColor(.red.opacity(0.8))
                    } else {
                        DAWTDesign.Typography.subtext("Direct audio/video links work best (mp3, m4a, mp4).")
                    }
                }
                .padding(.horizontal, DAWTDesign.Spacing.screenHorizontal)

                Spacer()

                // Buttons
                VStack(spacing: 12) {
                    DAWTPrimaryButton(title: "TRANSCRIBE") {
                        handleSubmit()
                    }
                    .disabled(urlText.trimmingCharacters(in: .whitespaces).isEmpty)
                    .opacity(urlText.trimmingCharacters(in: .whitespaces).isEmpty ? 0.4 : 1.0)

                    Button("Cancel") {
                        isPresented = false
                    }
                    .foregroundColor(DAWTDesign.Colors.textSecondary)
                }
                .padding(.horizontal, DAWTDesign.Spacing.screenHorizontal)
                .padding(.bottom, 32)
            }
        }
        .onAppear {
            // Auto-focus field
            isFieldFocused = true

            // Check clipboard for URL
            if let clipboardString = UIPasteboard.general.string,
               let _ = URL(string: clipboardString),
               clipboardString.starts(with: "http") {
                urlText = clipboardString
            }
        }
    }

    private func handleSubmit() {
        let trimmed = urlText.trimmingCharacters(in: .whitespaces)

        guard !trimmed.isEmpty else { return }

        guard let url = URL(string: trimmed),
              url.scheme == "http" || url.scheme == "https" else {
            errorMessage = "Please enter a valid URL starting with http:// or https://"
            return
        }

        // Clear error and submit
        errorMessage = nil
        onSubmit(url)
        isPresented = false
    }
}

#Preview {
    URLTranscriptionSheet(isPresented: .constant(true)) { url in
    }
}
