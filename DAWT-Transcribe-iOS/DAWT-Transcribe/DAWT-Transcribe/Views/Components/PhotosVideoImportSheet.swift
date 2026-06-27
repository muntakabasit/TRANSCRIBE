//
//  PhotosVideoImportSheet.swift
//  DAWT-Transcribe
//
//  One-video Photos import for the Transcribe source flow.
//

import CoreTransferable
import PhotosUI
import SwiftUI
import UniformTypeIdentifiers

struct PhotosVideoImportSheet: View {
    let onImport: (URL) -> Void
    let onFailure: (String) -> Void

    @Environment(\.dismiss) private var dismiss
    @State private var selectedItem: PhotosPickerItem?
    @State private var isImporting = false

    var body: some View {
        ZStack {
            DAWTDesign.Colors.background
                .ignoresSafeArea()

            VStack(spacing: 0) {
                RoundedRectangle(cornerRadius: 2.5)
                    .fill(Color.gray.opacity(0.3))
                    .frame(width: 36, height: 5)
                    .padding(.top, 8)
                    .padding(.bottom, 28)

                VStack(alignment: .leading, spacing: 10) {
                    DAWTDesign.Typography.sectionLabel("PHOTOS VIDEO")
                    DAWTDesign.Typography.subtext("Choose one saved video to transcribe.")
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(.horizontal, DAWTDesign.Spacing.screenHorizontal)

                Spacer()

                VStack(spacing: 12) {
                    PhotosPicker(selection: $selectedItem, matching: .videos) {
                        DAWTDesign.Typography.button(isImporting ? "Preparing..." : "Choose Video")
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .frame(height: DAWTDesign.Spacing.buttonHeight)
                            .background(DAWTDesign.Colors.accent)
                            .cornerRadius(12)
                    }
                    .disabled(isImporting)
                    .opacity(isImporting ? 0.6 : 1.0)

                    Button("Cancel") {
                        dismiss()
                    }
                    .foregroundColor(DAWTDesign.Colors.textSecondary)
                    .disabled(isImporting)
                }
                .padding(.horizontal, DAWTDesign.Spacing.screenHorizontal)
                .padding(.bottom, 32)
            }
        }
        .onChange(of: selectedItem) { item in
            importVideo(from: item)
        }
    }

    private func importVideo(from item: PhotosPickerItem?) {
        guard let item else { return }

        Task {
            await MainActor.run {
                isImporting = true
            }

            do {
                let importedVideo = try await item.loadTransferable(type: PhotosImportedVideo.self)

                await MainActor.run {
                    isImporting = false

                    if let importedVideo {
                        onImport(importedVideo.url)
                        dismiss()
                    } else {
                        onFailure("Couldn't import that video from Photos.")
                    }
                }
            } catch {
                await MainActor.run {
                    isImporting = false
                    onFailure("That video couldn't be prepared for transcription. Try a shorter or different video.")
                }
            }
        }
    }
}

private struct PhotosImportedVideo: Transferable {
    let url: URL

    static var transferRepresentation: some TransferRepresentation {
        FileRepresentation(contentType: .movie) { video in
            SentTransferredFile(video.url)
        } importing: { received in
            let sourceURL = received.file
            let fileExtension = sourceURL.pathExtension.isEmpty ? "mov" : sourceURL.pathExtension
            let destinationURL = FileManager.default.temporaryDirectory
                .appendingPathComponent(UUID().uuidString)
                .appendingPathExtension(fileExtension)

            if FileManager.default.fileExists(atPath: destinationURL.path) {
                try FileManager.default.removeItem(at: destinationURL)
            }

            try FileManager.default.copyItem(at: sourceURL, to: destinationURL)
            return PhotosImportedVideo(url: destinationURL)
        }
    }
}

#Preview {
    PhotosVideoImportSheet(
        onImport: { _ in },
        onFailure: { _ in }
    )
}
