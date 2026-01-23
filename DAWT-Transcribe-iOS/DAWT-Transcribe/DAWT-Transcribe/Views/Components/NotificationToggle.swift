//
//  NotificationToggle.swift
//  DAWT-Transcribe
//
//  Simple notification toggle for "Notify me when it's ready"
//

import SwiftUI

struct NotificationToggle: View {
    @Binding var isEnabled: Bool

    var body: some View {
        HStack(spacing: 12) {
            VStack(alignment: .leading, spacing: 2) {
                Text("Notify me when it's ready")
                    .font(.system(size: 14, weight: .medium))
                    .foregroundColor(DAWTDesign.Colors.textPrimary)

                Text("One alert. No spam.")
                    .font(.system(size: 12))
                    .foregroundColor(DAWTDesign.Colors.textSecondary)
            }

            Spacer()

            Toggle("", isOn: $isEnabled)
                .labelsHidden()
                .tint(DAWTDesign.Colors.accent)
        }
        .padding(16)
        .background(DAWTDesign.Colors.background)
        .cornerRadius(12)
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(DAWTDesign.Colors.divider, lineWidth: 1)
        )
    }
}

#Preview {
    VStack(spacing: 16) {
        NotificationToggle(isEnabled: .constant(false))
        NotificationToggle(isEnabled: .constant(true))
    }
    .padding()
    .background(Color(white: 0.95))
}
