//
//  AudioImporter.swift
//  DAWT-Transcribe
//
//  Service for importing audio files from Files app
//

import SwiftUI
import UniformTypeIdentifiers
import Combine

class AudioImporter: ObservableObject {
    @Published var isPresented = false
    @Published var importedURL: URL?

    func presentPicker() {
        isPresented = true
    }

    func handleImport(result: Result<[URL], Error>) {
        switch result {
        case .success(let urls):
            guard let url = urls.first else { return }

            // Copy file to temporary location for processing
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
            }

        case .failure(let error):
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
                UTType.audio,
                UTType.mp3,
                UTType.wav,
                UTType.mpeg4Audio,
                UTType(filenameExtension: "m4a") ?? .audio
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
