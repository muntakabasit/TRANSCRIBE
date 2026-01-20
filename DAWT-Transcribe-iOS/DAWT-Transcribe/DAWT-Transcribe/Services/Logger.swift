//
//  Logger.swift
//  DAWT-Transcribe
//
//  Production-ready logging utility
//

import Foundation
import os.log

enum DAWTLogger {
    private static let subsystem = Bundle.main.bundleIdentifier ?? "com.dawt.transcribe"

    static let general = Logger(subsystem: subsystem, category: "general")
    static let network = Logger(subsystem: subsystem, category: "network")
    static let audio = Logger(subsystem: subsystem, category: "audio")
    static let storage = Logger(subsystem: subsystem, category: "storage")
    static let sharing = Logger(subsystem: subsystem, category: "sharing")

    #if DEBUG
    static var isDebugEnabled = true
    #else
    static var isDebugEnabled = false
    #endif

    static func debug(_ message: String, category: Logger = general) {
        if isDebugEnabled {
            category.debug("\(message)")
        }
    }

    static func info(_ message: String, category: Logger = general) {
        category.info("\(message)")
    }

    static func error(_ message: String, category: Logger = general) {
        category.error("\(message)")
    }
}
