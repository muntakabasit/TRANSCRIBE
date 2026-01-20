//
//  ShareSheet.swift
//  DAWT-Transcribe
//
//  UIKit wrapper for iOS Share Sheet (UIActivityViewController)
//

import SwiftUI
import UIKit

struct ShareSheet: UIViewControllerRepresentable {
    let items: [Any]
    let onDismiss: () -> Void

    func makeUIViewController(context: Context) -> UIActivityViewController {
        // Safety check
        let shareItems = items.isEmpty ? ["No content to share"] : items

        let controller = UIActivityViewController(
            activityItems: shareItems,
            applicationActivities: nil
        )

        controller.completionWithItemsHandler = { _, completed, _, _ in
            if completed {
                onDismiss()
            }
        }

        return controller
    }

    func updateUIViewController(_ uiViewController: UIActivityViewController, context: Context) {
        // No updates needed
    }
}
