//
//  AudioImporter.swift
//  DAWT-Transcribe
//
//  Service for importing audio and video files from Files app
//  Supports audio extraction from video files (mp4, mov)
//

import SwiftUI
import UniformTypeIdentifiers
import Combine
import AVFoundation

class AudioImporter: ObservableObject {
    @Published var isPresented = false
    @Published var importedURL: URL?
    @Published var isExtractingAudio = false
    @Published var extractionProgress: Double = 0.0

    func presentPicker() {
        isPresented = true
    }

    func handleImport(result: Result<[URL], Error>) {
        switch result {
        case .success(let urls):
            guard let url = urls.first else { return }

            // Check if this is a video file
            let fileExtension = url.pathExtension.lowercased()
            let isVideo = ["mp4", "mov", "m4v", "avi", "mkv"].contains(fileExtension)

            if isVideo {
                // Extract audio from video
                Task {
                    await extractAudioFromVideo(url)
                }
            } else {
                // Process audio file directly
                copyAudioFile(url)
            }

        case .failure(let error):
            DAWTLogger.error("Import failed: \(error)", category: DAWTLogger.audio)
        }
    }

    private func copyAudioFile(_ url: URL) {
        let tempURL = FileManager.default.temporaryDirectory
            .appendingPathComponent(url.lastPathComponent)

        do {
            // Remove existing file if present
            if FileManager.default.fileExists(atPath: tempURL.path) {
                try FileManager.default.removeItem(at: tempURL)
            }

            // Copy to temp location
            try FileManager.default.copyItem(at: url, to: tempURL)
            importedURL = tempURL
        } catch {
            DAWTLogger.error("Failed to copy imported audio file: \(error)", category: DAWTLogger.audio)
        }
    }

    private func extractAudioFromVideo(_ videoURL: URL) async {
        await MainActor.run {
            isExtractingAudio = true
            extractionProgress = 0.0
        }

        let asset = AVAsset(url: videoURL)

        // Create output URL for extracted audio
        let outputURL = FileManager.default.temporaryDirectory
            .appendingPathComponent(UUID().uuidString)
            .appendingPathExtension("m4a")

        // Remove existing file if present
        if FileManager.default.fileExists(atPath: outputURL.path) {
            try? FileManager.default.removeItem(at: outputURL)
        }

        // Configure export session
        guard let exportSession = AVAssetExportSession(
            asset: asset,
            presetName: AVAssetExportPresetAppleM4A
        ) else {
            await MainActor.run {
                isExtractingAudio = false
                DAWTLogger.error("Failed to create export session", category: DAWTLogger.audio)
            }
            return
        }

        exportSession.outputURL = outputURL
        exportSession.outputFileType = .m4a

        // Start export
        await exportSession.export()

        await MainActor.run {
            isExtractingAudio = false

            switch exportSession.status {
            case .completed:
                DAWTLogger.info("Audio extracted successfully from video", category: DAWTLogger.audio)
                importedURL = outputURL

            case .failed:
                let errorMessage = exportSession.error?.localizedDescription ?? "Unknown error"
                DAWTLogger.error("Audio extraction failed: \(errorMessage)", category: DAWTLogger.audio)

            case .cancelled:
                DAWTLogger.info("Audio extraction cancelled", category: DAWTLogger.audio)

            default:
                break
            }
        }
    }
}

// SwiftUI wrapper for document picker
struct AudioDocumentPicker: UIViewControllerRepresentable {
    @Binding var isPresented: Bool
    let onPick: (Result<[URL], Error>) -> Void

    func makeUIViewController(context: Context) -> UIDocumentPickerViewController {
        let picker = UIDocumentPickerViewController(
            forOpeningContentTypes: [
                // Audio formats
                UTType.audio,
                UTType.mp3,
                UTType.wav,
                UTType.mpeg4Audio,
                UTType(filenameExtension: "m4a") ?? .audio,
                UTType(filenameExtension: "aac") ?? .audio,
                UTType(filenameExtension: "flac") ?? .audio,
                UTType(filenameExtension: "ogg") ?? .audio,
                // Video formats
                UTType.movie,
                UTType.mpeg4Movie,
                UTType.quickTimeMovie,
                UTType(filenameExtension: "avi") ?? .movie,
                UTType(filenameExtension: "mkv") ?? .movie
            ],
            asCopy: true
        )
        picker.delegate = context.coordinator
        picker.allowsMultipleSelection = false
        return picker
    }

    func updateUIViewController(_ uiViewController: UIDocumentPickerViewController, context: Context) {}

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: NSObject, UIDocumentPickerDelegate {
        let parent: AudioDocumentPicker

        init(_ parent: AudioDocumentPicker) {
            self.parent = parent
        }

        func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
            parent.onPick(.success(urls))
            parent.isPresented = false
        }

        func documentPickerWasCancelled(_ controller: UIDocumentPickerViewController) {
            parent.isPresented = false
        }
    }
}
