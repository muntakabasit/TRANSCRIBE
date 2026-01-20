//
//  BackgroundTaskManager.swift
//  DAWT-Transcribe
//
//  Manages background task for transcription when app is backgrounded
//

import UIKit
import UserNotifications

class BackgroundTaskManager {
    static let shared = BackgroundTaskManager()
    private var backgroundTaskID: UIBackgroundTaskIdentifier = .invalid

    private init() {}

    // Start background task
    func beginBackgroundTask(name: String = "Transcription") {
        backgroundTaskID = UIApplication.shared.beginBackgroundTask(withName: name) { [weak self] in
            self?.endBackgroundTask()
        }
    }

    // End background task
    func endBackgroundTask() {
        if backgroundTaskID != .invalid {
            UIApplication.shared.endBackgroundTask(backgroundTaskID)
            backgroundTaskID = .invalid
        }
    }

    // Show notification when transcription completes
    func notifyTranscriptionComplete(success: Bool) {
        let content = UNMutableNotificationContent()
        content.title = "DAWT-Transcribe"
        content.body = success ? "Transcription complete" : "Transcription failed"
        content.sound = .default

        let request = UNNotificationRequest(
            identifier: UUID().uuidString,
            content: content,
            trigger: nil
        )

        UNUserNotificationCenter.current().add(request) { error in
            if let error = error {
            }
        }
    }
}
