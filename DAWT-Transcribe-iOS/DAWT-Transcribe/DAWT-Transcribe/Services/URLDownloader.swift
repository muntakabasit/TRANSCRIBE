//
//  URLDownloader.swift
//  DAWT-Transcribe
//
//  Service for downloading audio/video from URLs
//

import Foundation
import Combine

class URLDownloader: ObservableObject {
    @Published var isDownloading = false
    @Published var downloadedURL: URL?
    @Published var errorMessage: String?

    func download(from url: URL) async throws -> URL {
        await MainActor.run {
            isDownloading = true
            errorMessage = nil
        }

        do {
            // Download the file
            let (tempURL, response) = try await URLSession.shared.download(from: url)

            // Verify it's audio/video
            guard let mimeType = response.mimeType else {
                throw DownloadError.invalidFileType
            }

            let audioVideoTypes = [
                "audio/", "video/",
                "application/octet-stream" // Some servers send this for media files
            ]

            let isMediaFile = audioVideoTypes.contains { mimeType.starts(with: $0) }
            guard isMediaFile else {
                throw DownloadError.notMediaFile(mimeType)
            }

            // Move to a permanent temp location with proper extension
            let fileExtension = url.pathExtension.isEmpty ? "m4a" : url.pathExtension
            let fileName = "\(UUID().uuidString).\(fileExtension)"
            let destinationURL = FileManager.default.temporaryDirectory
                .appendingPathComponent(fileName)

            // Remove if exists
            if FileManager.default.fileExists(atPath: destinationURL.path) {
                try FileManager.default.removeItem(at: destinationURL)
            }

            try FileManager.default.moveItem(at: tempURL, to: destinationURL)

            await MainActor.run {
                isDownloading = false
                downloadedURL = destinationURL
            }

            return destinationURL

        } catch let error as DownloadError {
            await MainActor.run {
                isDownloading = false
                errorMessage = error.userMessage
            }
            throw error

        } catch {
            await MainActor.run {
                isDownloading = false
                errorMessage = "Couldn't use that link. Try a direct audio/video link."
            }
            throw DownloadError.downloadFailed(error)
        }
    }

    func reset() {
        isDownloading = false
        downloadedURL = nil
        errorMessage = nil
    }
}

enum DownloadError: Error {
    case invalidFileType
    case notMediaFile(String)
    case downloadFailed(Error)

    var userMessage: String {
        switch self {
        case .invalidFileType:
            return "Couldn't determine file type. Try a direct audio/video link."
        case .notMediaFile(let mimeType):
            return "That link doesn't point to audio/video (found: \(mimeType))."
        case .downloadFailed:
            return "Couldn't use that link. Try a direct audio/video link."
        }
    }
}
