//
//  DAWTPrimaryButton.swift
//  DAWT-Transcribe
//
//  Primary action button following DAWT design system
//

import SwiftUI

struct DAWTPrimaryButton: View {
    let title: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            DAWTDesign.Typography.button(title)
                .foregroundColor(.white)
                .dawtPrimaryButton()
        }
    }
}

#Preview {
    VStack(spacing: 20) {
        DAWTPrimaryButton(title: "NEW TRANSCRIPTION") {}
        DAWTPrimaryButton(title: "SHARE") {}
    }
    .padding()
    .background(DAWTDesign.Colors.background)
}
