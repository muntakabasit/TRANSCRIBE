//
//  BackgroundTaskManager.swift
//  DAWT-Transcribe
//
//  Manages background tasks and notifications for transcription
//  Enhanced with rich notifications, sounds, and badge support
//

import UIKit
import UserNotifications

class BackgroundTaskManager {
    static let shared = BackgroundTaskManager()
    private var backgroundTaskID: UIBackgroundTaskIdentifier = .invalid

    private init() {
        requestNotificationPermissions()
    }

    // MARK: - Notification Permissions

    func requestNotificationPermissions() {
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound, .badge]) { granted, error in
            if granted {
                DAWTLogger.info("Notification permissions granted", category: DAWTLogger.system)
            } else if let error = error {
                DAWTLogger.error("Notification permission error: \(error)", category: DAWTLogger.system)
            }
        }
    }

    // MARK: - Background Tasks

    /// Start background task for long-running transcription
    func beginBackgroundTask(name: String = "Transcription") {
        backgroundTaskID = UIApplication.shared.beginBackgroundTask(withName: name) { [weak self] in
            self?.endBackgroundTask()
        }
    }

    /// End background task
    func endBackgroundTask() {
        if backgroundTaskID != .invalid {
            UIApplication.shared.endBackgroundTask(backgroundTaskID)
            backgroundTaskID = .invalid
        }
    }

    // MARK: - Rich Notifications

    /// Show notification when transcription completes
    func notifyTranscriptionComplete(success: Bool, duration: TimeInterval? = nil) {
        let content = UNMutableNotificationContent()

        if success {
            content.title = "Transcription Complete ✓"
            content.body = duration.map { "Your \(Int($0))s recording is ready to share" }
                          ?? "Your transcription is ready to share"
            content.sound = UNNotificationSound(named: UNNotificationSoundName("completion.wav"))
            content.badge = 0  // Clear badge
        } else {
            content.title = "Couldn't Finish Right Now"
            content.body = "Your audio is safe. Try again when you're ready."
            content.sound = .default
        }

        // Add category for actions
        content.categoryIdentifier = "TRANSCRIPTION_COMPLETE"
        content.userInfo = ["success": success]

        // Deliver immediately (no trigger)
        let request = UNNotificationRequest(
            identifier: UUID().uuidString,
            content: content,
            trigger: nil
        )

        UNUserNotificationCenter.current().add(request) { error in
            if let error = error {
                DAWTLogger.error("Failed to schedule notification: \(error)", category: DAWTLogger.system)
            } else {
                DAWTLogger.info("Notification scheduled successfully", category: DAWTLogger.system)
            }
        }
    }

    /// Show notification for video extraction progress (optional)
    func notifyExtractionStarted(filename: String) {
        let content = UNMutableNotificationContent()
        content.title = "Extracting Audio"
        content.body = "Getting audio ready from \(filename)"
        content.sound = nil  // Silent
        content.interruptionLevel = .passive  // Non-intrusive

        let request = UNNotificationRequest(
            identifier: "extraction-\(UUID().uuidString)",
            content: content,
            trigger: nil
        )

        UNUserNotificationCenter.current().add(request)
    }

    /// Clear all pending/delivered notifications
    func clearAllNotifications() {
        UNUserNotificationCenter.current().removeAllPendingNotificationRequests()
        UNUserNotificationCenter.current().removeAllDeliveredNotifications()

        // Reset badge
        DispatchQueue.main.async {
            UIApplication.shared.applicationIconBadgeNumber = 0
        }
    }

    /// Clear badge only
    func clearBadge() {
        DispatchQueue.main.async {
            UIApplication.shared.applicationIconBadgeNumber = 0
        }
    }

    // MARK: - Notification Actions

    /// Register notification categories and actions
    func registerNotificationCategories() {
        let viewAction = UNNotificationAction(
            identifier: "VIEW_ACTION",
            title: "View Transcript",
            options: [.foreground]
        )

        let shareAction = UNNotificationAction(
            identifier: "SHARE_ACTION",
            title: "Share",
            options: [.foreground]
        )

        let category = UNNotificationCategory(
            identifier: "TRANSCRIPTION_COMPLETE",
            actions: [viewAction, shareAction],
            intentIdentifiers: [],
            options: []
        )

        UNUserNotificationCenter.current().setNotificationCategories([category])
    }
}
