//
//  AudioRecorder.swift
//  DAWT-Transcribe
//
//  Service for recording audio
//

import AVFoundation
import SwiftUI
import Combine

class AudioRecorder: NSObject, ObservableObject {
    @Published var isRecording = false
    @Published var recordingURL: URL?

    private var audioRecorder: AVAudioRecorder?

    func startRecording() {
        // Request microphone permission
        AVAudioSession.sharedInstance().requestRecordPermission { [weak self] allowed in
            guard allowed else {
                return
            }

            DispatchQueue.main.async {
                self?.setupAndStartRecording()
            }
        }
    }

    private func setupAndStartRecording() {
        let audioSession = AVAudioSession.sharedInstance()

        do {
            try audioSession.setCategory(.playAndRecord, mode: .default)
            try audioSession.setActive(true)

            let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
            let audioFilename = documentsPath.appendingPathComponent("recording-\(Date().timeIntervalSince1970).m4a")

            let settings: [String: Any] = [
                AVFormatIDKey: Int(kAudioFormatMPEG4AAC),
                AVSampleRateKey: 44100.0,
                AVNumberOfChannelsKey: 1,
                AVEncoderAudioQualityKey: AVAudioQuality.high.rawValue
            ]

            audioRecorder = try AVAudioRecorder(url: audioFilename, settings: settings)
            audioRecorder?.record()

            isRecording = true
            recordingURL = audioFilename

        } catch {
            // Recording setup failed - error handled by UI state
        }
    }

    func stopRecording() {
        audioRecorder?.stop()
        isRecording = false

        do {
            try AVAudioSession.sharedInstance().setActive(false)
        } catch {
            // Audio session deactivation failed - non-critical
        }
    }
}
