//
//  ToastView.swift
//  DAWT-Transcribe
//
//  Simple toast notification (2 seconds, bottom of screen)
//

import SwiftUI

struct ToastView: View {
    let message: String
    @Binding var isShowing: Bool

    var body: some View {
        VStack {
            Spacer()

            if isShowing {
                Text(message)
                    .font(.system(size: 14, weight: .medium))
                    .foregroundColor(.white)
                    .padding(.horizontal, 20)
                    .padding(.vertical, 12)
                    .background(Color.black.opacity(0.8))
                    .cornerRadius(8)
                    .transition(.move(edge: .bottom).combined(with: .opacity))
                    .padding(.bottom, 50)
            }
        }
        .animation(.easeInOut(duration: 0.3), value: isShowing)
        .onChange(of: isShowing) { newValue in
            if newValue {
                DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) {
                    isShowing = false
                }
            }
        }
    }
}

#Preview {
    ToastView(message: "Shared", isShowing: .constant(true))
}
