//
//  APIClient.swift
//  DAWT-Transcribe
//
//  Client for communicating with DAWT backend
//

import Foundation

class APIClient {
    // MARK: - Configuration

    // Development: Local network
    // Production: Update to your production URL
    static let baseURL = "http://172.20.10.2:5001"

    // MARK: - Transcription

    struct TranscribeURLRequest: Codable {
        let url: String
        let lang: String
    }

    struct TranscribeResponse: Codable {
        let success: Bool
        let full_text: String?
        let segments: [SegmentResponse]?
        let language: String?
        let duration: Double?
        let error: String?
    }

    struct SegmentResponse: Codable {
        let start: Double
        let end: Double
        let text: String
    }

    static func transcribeURL(url: String, language: String = "en") async throws -> TranscribeResponse {
        guard let endpoint = URL(string: "\(baseURL)/transcribe") else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: endpoint)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.timeoutInterval = 300 // 5 minutes for video download + transcription

        let body = TranscribeURLRequest(url: url, lang: language)
        request.httpBody = try JSONEncoder().encode(body)

        // Create a custom URLSession with longer timeout
        let configuration = URLSessionConfiguration.default
        configuration.timeoutIntervalForRequest = 300
        configuration.timeoutIntervalForResource = 600
        let session = URLSession(configuration: configuration)

        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }

        guard httpResponse.statusCode == 200 else {
            throw APIError.serverError(httpResponse.statusCode)
        }

        let transcribeResponse = try JSONDecoder().decode(TranscribeResponse.self, from: data)

        guard transcribeResponse.success else {
            throw APIError.transcriptionFailed(transcribeResponse.error ?? "Unknown error")
        }

        return transcribeResponse
    }

    // Convert API response to app Segment format
    static func convertToSegments(from response: TranscribeResponse) -> [Segment] {
        guard let segments = response.segments else { return [] }

        return segments.map { segment in
            Segment.from(
                startSeconds: segment.start,
                endSeconds: segment.end,
                text: segment.text
            )
        }
    }

    // MARK: - Audio File Upload

    static func transcribeAudioFile(audioURL: URL, language: String = "en") async throws -> TranscribeResponse {
        guard let endpoint = URL(string: "\(baseURL)/transcribe_file") else {
            throw APIError.invalidURL
        }

        // Create multipart form data
        let boundary = UUID().uuidString
        var request = URLRequest(url: endpoint)
        request.httpMethod = "POST"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        request.timeoutInterval = 300

        var body = Data()

        // Add language field
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"lang\"\r\n\r\n".data(using: .utf8)!)
        body.append("\(language)\r\n".data(using: .utf8)!)

        // Add audio file
        let audioData = try Data(contentsOf: audioURL)
        let filename = audioURL.lastPathComponent
        let mimeType = "audio/\(audioURL.pathExtension)"

        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(filename)\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: \(mimeType)\r\n\r\n".data(using: .utf8)!)
        body.append(audioData)
        body.append("\r\n".data(using: .utf8)!)
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)

        request.httpBody = body

        let configuration = URLSessionConfiguration.default
        configuration.timeoutIntervalForRequest = 300
        configuration.timeoutIntervalForResource = 600
        let session = URLSession(configuration: configuration)

        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }

        guard httpResponse.statusCode == 200 else {
            throw APIError.serverError(httpResponse.statusCode)
        }

        let transcribeResponse = try JSONDecoder().decode(TranscribeResponse.self, from: data)

        guard transcribeResponse.success else {
            throw APIError.transcriptionFailed(transcribeResponse.error ?? "Unknown error")
        }

        return transcribeResponse
    }
}

enum APIError: Error {
    case invalidURL
    case invalidResponse
    case serverError(Int)
    case transcriptionFailed(String)

    var userMessage: String {
        switch self {
        case .invalidURL:
            return "Invalid server URL. Check your network settings."
        case .invalidResponse:
            return "Couldn't connect to server. Is it running?"
        case .serverError(let code):
            return "Server error (\(code)). Try again later."
        case .transcriptionFailed(let message):
            return message
        }
    }
}
