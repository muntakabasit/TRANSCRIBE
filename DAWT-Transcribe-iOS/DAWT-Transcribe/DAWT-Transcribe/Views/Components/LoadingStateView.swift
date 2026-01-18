//
//  LoadingStateView.swift
//  DAWT-Transcribe
//
//  Loading overlay for transcription in progress
//

import SwiftUI

struct LoadingStateView: View {
    let state: TranscriptionState

    var body: some View {
        ZStack {
            DAWTDesign.Colors.background
                .opacity(0.95)
                .ignoresSafeArea()

            VStack(spacing: 24) {
                // Progress indicator
                ProgressView()
                    .scaleEffect(1.5)
                    .tint(DAWTDesign.Colors.accent)

                // Status text
                VStack(spacing: 8) {
                    DAWTDesign.Typography.header(state.displayText.uppercased())

                    if !state.subtitleText.isEmpty {
                        DAWTDesign.Typography.subtext(state.subtitleText)
                            .multilineTextAlignment(.center)
                            .padding(.horizontal, 40)
                    }
                }
            }
        }
    }
}

#Preview {
    LoadingStateView(state: .transcribing)
}
