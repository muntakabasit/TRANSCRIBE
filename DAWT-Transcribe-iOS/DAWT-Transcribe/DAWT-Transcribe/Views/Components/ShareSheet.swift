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

    func makeUIViewController(context: Context) -> UIViewController {
        guard !items.isEmpty else {
            assertionFailure("ShareSheet received empty activity items.")
            return UIViewController()
        }

        let controller = UIActivityViewController(
            activityItems: items,
            applicationActivities: nil
        )

        controller.completionWithItemsHandler = { _, completed, _, _ in
            if completed {
                onDismiss()
            }
        }

        return controller
    }

    func updateUIViewController(_ uiViewController: UIViewController, context: Context) {
        // No updates needed
    }
}
