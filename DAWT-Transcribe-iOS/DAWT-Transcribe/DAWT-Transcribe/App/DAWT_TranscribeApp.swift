//
//  DAWT_TranscribeApp.swift
//  DAWT-Transcribe
//
//  Main app entry point
//

import SwiftUI

@main
struct DAWT_TranscribeApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

    var body: some Scene {
        WindowGroup {
            HomeView()
        }
    }
}

// MARK: - App Delegate (for notifications and background processing)

class AppDelegate: NSObject, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey : Any]? = nil
    ) -> Bool {
        // Request notification permissions
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound]) { granted, error in
            if granted {
            } else if let error = error {
            }
        }

        return true
    }

    // Background task handling
    func application(
        _ application: UIApplication,
        performFetchWithCompletionHandler completionHandler: @escaping (UIBackgroundFetchResult) -> Void
    ) {
        // Handle background transcription completion if needed
        completionHandler(.noData)
    }
}
