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

    @State private var permissionState: PermissionState = .unknown
    @State private var didCheckOnAppear = false

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
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
                        handleToggleChange(newValue)
                    }
                ))
                .labelsHidden()
                .tint(DAWTDesign.Colors.accent)
            }

            if permissionState == .denied {
                HStack(spacing: 10) {
                    Text("Notifications are off in System Settings.")
                        .font(.system(size: 12))
                        .foregroundColor(DAWTDesign.Colors.textSecondary)

                    Spacer()

                    Button("Open Settings") {
                        openSystemSettings()
                    }
                    .font(.system(size: 12, weight: .semibold))
                    .foregroundColor(DAWTDesign.Colors.accent)
                }
                .padding(.top, 2)
            }
        }
        .padding(16)
        .background(DAWTDesign.Colors.background)
        .cornerRadius(12)
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(DAWTDesign.Colors.divider, lineWidth: 1)
        )
        .task {
            // Only run once per view lifetime.
            guard !didCheckOnAppear else { return }
            didCheckOnAppear = true
            await refreshPermissionState()

            // If user previously enabled the toggle but permissions were later revoked,
            // keep the UI honest.
            if notifyWhenReady && permissionState == .denied {
                notifyWhenReady = false
            }
        }
    }

    // MARK: - Toggle Logic

    private func handleToggleChange(_ newValue: Bool) {
        if newValue {
            Task {
                await enableNotificationsIfPossible()
            }
        } else {
            permissionState = (permissionState == .unknown) ? .unknown : permissionState
            notifyWhenReady = false
        }
    }

    @MainActor
    private func enableNotificationsIfPossible() async {
        await refreshPermissionState()

        switch permissionState {
        case .authorized:
            notifyWhenReady = true

        case .notDetermined:
            let granted = await requestNotificationPermission()
            await refreshPermissionState()

            if granted {
                notifyWhenReady = true
            } else {
                notifyWhenReady = false
                permissionState = .denied
            }

        case .denied:
            // User said no (or system said no). Keep toggle off and explain why.
            notifyWhenReady = false

        case .unknown:
            // Fallback: try requesting once.
            let granted = await requestNotificationPermission()
            await refreshPermissionState()
            notifyWhenReady = granted
        }
    }

    // MARK: - Permissions

    private func refreshPermissionState() async {
        let center = UNUserNotificationCenter.current()
        let settings = await center.notificationSettings()

        await MainActor.run {
            switch settings.authorizationStatus {
            case .authorized, .provisional, .ephemeral:
                permissionState = .authorized
            case .denied:
                permissionState = .denied
            case .notDetermined:
                permissionState = .notDetermined
            @unknown default:
                permissionState = .unknown
            }
        }
    }

    private func requestNotificationPermission() async -> Bool {
        let center = UNUserNotificationCenter.current()

        // Keep it lightweight: alert + sound.
        // Badge is optional; only add if you actually set badge counts.
        do {
            let granted = try await center.requestAuthorization(options: [.alert, .sound])
            return granted
        } catch {
            return false
        }
    }

    private func openSystemSettings() {
        // App-prefs deep links are not officially guaranteed, but this is widely used.
        // If it fails, the button simply does nothing.
        if let url = URL(string: "x-apple.systempreferences:com.apple.preference.notifications") {
            #if os(macOS)
            NSWorkspace.shared.open(url)
            #else
            UIApplication.shared.open(url)
            #endif
        }
    }

    // MARK: - Local Types

    private enum PermissionState: Equatable {
        case unknown
        case notDetermined
        case authorized
        case denied
    }
}

#Preview {
    VStack(spacing: 16) {
        NotificationToggle()
    }
    .padding()
    .background(Color(white: 0.95))
}
