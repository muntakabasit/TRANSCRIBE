//
//  HapticsManager.swift
//  DAWT-Transcribe
//
//  Premium haptic feedback system for delightful user interactions
//  Provides contextual haptics for recording, importing, transcribing, and sharing
//

import UIKit
import CoreHaptics

/// Manages haptic feedback throughout the app with contextual patterns
class HapticsManager {
    static let shared = HapticsManager()

    private var engine: CHHapticEngine?
    private var supportsHaptics: Bool = false

    private init() {
        setupHapticsEngine()
    }

    // MARK: - Setup

    private func setupHapticsEngine() {
        guard CHHapticEngine.capabilitiesForHardware().supportsHaptics else {
            supportsHaptics = false
            return
        }

        do {
            engine = try CHHapticEngine()
            try engine?.start()
            supportsHaptics = true

            // Handle engine reset
            engine?.resetHandler = { [weak self] in
                do {
                    try self?.engine?.start()
                } catch {
                    DAWTLogger.error("Failed to restart haptics engine: \(error)", category: DAWTLogger.system)
                }
            }

            // Handle engine stopped
            engine?.stoppedHandler = { reason in
                DAWTLogger.info("Haptics engine stopped: \(reason)", category: DAWTLogger.system)
            }

        } catch {
            DAWTLogger.error("Failed to create haptics engine: \(error)", category: DAWTLogger.system)
            supportsHaptics = false
        }
    }

    // MARK: - Recording Haptics

    /// Haptic for starting recording (medium impact)
    func recordingStarted() {
        let generator = UIImpactFeedbackGenerator(style: .medium)
        generator.impactOccurred()
    }

    /// Haptic for stopping recording (light impact)
    func recordingStopped() {
        let generator = UIImpactFeedbackGenerator(style: .light)
        generator.impactOccurred()
    }

    /// Haptic pulse during active recording (subtle)
    func recordingPulse() {
        guard supportsHaptics else { return }

        let intensity = CHHapticEventParameter(parameterID: .hapticIntensity, value: 0.3)
        let sharpness = CHHapticEventParameter(parameterID: .hapticSharpness, value: 0.2)
        let event = CHHapticEvent(eventType: .hapticTransient, parameters: [intensity, sharpness], relativeTime: 0)

        playPattern([event])
    }

    // MARK: - Import Haptics

    /// Haptic for successful file import
    func fileImported() {
        let generator = UINotificationFeedbackGenerator()
        generator.notificationOccurred(.success)
    }

    /// Haptic for import error
    func importFailed() {
        let generator = UINotificationFeedbackGenerator()
        generator.notificationOccurred(.error)
    }

    // MARK: - Transcription Progress Haptics

    /// Subtle haptic for each progress step (Preparing → Listening → Structuring)
    func transcriptionStepCompleted() {
        let generator = UIImpactFeedbackGenerator(style: .soft)
        generator.impactOccurred(intensity: 0.7)
    }

    /// Haptic for transcription completion (success pattern)
    func transcriptionCompleted() {
        guard supportsHaptics else {
            let generator = UINotificationFeedbackGenerator()
            generator.notificationOccurred(.success)
            return
        }

        // Custom success pattern: quick double tap
        let tap1 = CHHapticEvent(
            eventType: .hapticTransient,
            parameters: [
                CHHapticEventParameter(parameterID: .hapticIntensity, value: 0.8),
                CHHapticEventParameter(parameterID: .hapticSharpness, value: 0.5)
            ],
            relativeTime: 0
        )

        let tap2 = CHHapticEvent(
            eventType: .hapticTransient,
            parameters: [
                CHHapticEventParameter(parameterID: .hapticIntensity, value: 1.0),
                CHHapticEventParameter(parameterID: .hapticSharpness, value: 0.8)
            ],
            relativeTime: 0.1
        )

        playPattern([tap1, tap2])
    }

    /// Haptic for transcription failure
    func transcriptionFailed() {
        let generator = UINotificationFeedbackGenerator()
        generator.notificationOccurred(.error)
    }

    // MARK: - Interaction Haptics

    /// Light haptic for button taps
    func buttonTapped() {
        let generator = UIImpactFeedbackGenerator(style: .light)
        generator.impactOccurred()
    }

    /// Haptic for primary action button (New Transcription)
    func primaryAction() {
        let generator = UIImpactFeedbackGenerator(style: .medium)
        generator.impactOccurred()
    }

    /// Haptic for selection (picker, toggle)
    func selectionChanged() {
        let generator = UISelectionFeedbackGenerator()
        generator.selectionChanged()
    }

    /// Haptic for toggle switch
    func toggleSwitched() {
        let generator = UIImpactFeedbackGenerator(style: .light)
        generator.impactOccurred(intensity: 0.6)
    }

    // MARK: - Share Haptics

    /// Haptic for copy action
    func textCopied() {
        let generator = UIImpactFeedbackGenerator(style: .light)
        generator.impactOccurred()
    }

    /// Haptic for share sheet presentation
    func shareSheetPresented() {
        let generator = UIImpactFeedbackGenerator(style: .light)
        generator.impactOccurred(intensity: 0.5)
    }

    // MARK: - Navigation Haptics

    /// Haptic for navigation push
    func navigatedForward() {
        let generator = UIImpactFeedbackGenerator(style: .light)
        generator.impactOccurred(intensity: 0.4)
    }

    /// Haptic for navigation back
    func navigatedBack() {
        let generator = UIImpactFeedbackGenerator(style: .light)
        generator.impactOccurred(intensity: 0.3)
    }

    // MARK: - Warning Haptics

    /// Haptic for warning/alert
    func warning() {
        let generator = UINotificationFeedbackGenerator()
        generator.notificationOccurred(.warning)
    }

    // MARK: - Custom Pattern Playback

    private func playPattern(_ events: [CHHapticEvent]) {
        guard supportsHaptics, let engine = engine else { return }

        do {
            let pattern = try CHHapticPattern(events: events, parameters: [])
            let player = try engine.makePlayer(with: pattern)
            try player.start(atTime: 0)
        } catch {
            DAWTLogger.error("Failed to play haptic pattern: \(error)", category: DAWTLogger.system)
        }
    }

    // MARK: - Audio Extraction Progress Haptic

    /// Subtle pulse during video audio extraction
    func extractionProgress() {
        guard supportsHaptics else { return }

        let intensity = CHHapticEventParameter(parameterID: .hapticIntensity, value: 0.25)
        let sharpness = CHHapticEventParameter(parameterID: .hapticSharpness, value: 0.15)
        let event = CHHapticEvent(eventType: .hapticTransient, parameters: [intensity, sharpness], relativeTime: 0)

        playPattern([event])
    }
}

// MARK: - Convenience Extensions

extension HapticsManager {
    /// Prepare haptic generator for upcoming interaction (reduces latency)
    func prepare() {
        let generator = UIImpactFeedbackGenerator(style: .medium)
        generator.prepare()
    }
}
