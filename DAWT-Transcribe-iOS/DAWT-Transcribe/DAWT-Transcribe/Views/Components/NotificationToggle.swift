//
//  NotificationToggle.swift
//  DAWT-Transcribe
//
//  Notification toggle with @AppStorage and permission request
//

import SwiftUI
import UserNotifications

struct NotificationToggle: View {
    @AppStorage("notifyWhenReady") private var notifyWhenReady = false

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

            Toggle("", isOn: Binding(
                get: { notifyWhenReady },
                set: { newValue in
                    if newValue {
                        // Request permission when user enables toggle
                        requestNotificationPermission { granted in
                            if granted {
                                notifyWhenReady = true
                            }
                        }
                    } else {
                        notifyWhenReady = false
                    }
                }
            ))
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

    private func requestNotificationPermission(completion: @escaping (Bool) -> Void) {
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound, .badge]) { granted, error in
            DispatchQueue.main.async {
                completion(granted)
            }
        }
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
