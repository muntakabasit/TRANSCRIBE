//
//  DAWTDesign.swift
//  DAWT-Transcribe
//
//  Design system tokens following the DAWT Constitution
//

import SwiftUI

struct DAWTDesign {
    // MARK: - Colors

    struct Colors {
        static let background = Color(hex: "F9F7F4")        // Warm off-white
        static let cardBackground = Color.white             // Pure white
        static let accent = Color(hex: "E8B44C")            // Warm gold (buttons only)
        static let textPrimary = Color(hex: "1A1A1A")       // Near black
        static let textSecondary = Color(hex: "666666")     // Medium gray
        static let divider = Color(hex: "E0E0E0")           // Hairline divider
        static let timestampText = Color(hex: "888888")     // Timestamp gray
    }

    // MARK: - Typography

    struct Typography {
        // Headers: System, 20pt, semibold, tracking +1.5
        static func header(_ text: String) -> some View {
            Text(text)
                .font(.system(size: 20, weight: .semibold))
                .kerning(1.5)
                .foregroundColor(Colors.textPrimary)
        }

        // Metadata: System, 11pt, medium, tracking +1.2
        static func metadata(_ text: String) -> some View {
            Text(text)
                .font(.system(size: 11, weight: .medium))
                .kerning(1.2)
                .foregroundColor(Colors.textSecondary)
        }

        // Section labels: System, 13pt, semibold, tracking +2
        static func sectionLabel(_ text: String) -> some View {
            Text(text)
                .font(.system(size: 13, weight: .semibold))
                .kerning(2)
                .foregroundColor(Colors.textPrimary)
        }

        // Body text: System, 16pt, regular, line spacing +6
        static func body(_ text: String) -> some View {
            Text(text)
                .font(.system(size: 16, weight: .regular))
                .lineSpacing(6)
                .foregroundColor(Colors.textPrimary)
        }

        // Button text: System, 14pt, semibold, tracking +1.5
        static func button(_ text: String) -> some View {
            Text(text)
                .font(.system(size: 14, weight: .semibold))
                .kerning(1.5)
        }

        // Small link text: System, 13pt, regular
        static func link(_ text: String) -> some View {
            Text(text)
                .font(.system(size: 13, weight: .regular))
                .foregroundColor(Colors.textSecondary)
        }

        // Timestamp: 12pt, regular
        static func timestamp(_ text: String) -> some View {
            Text(text)
                .font(.system(size: 12, weight: .regular))
                .foregroundColor(Colors.timestampText)
        }

        // Subtext: 13pt, regular
        static func subtext(_ text: String) -> some View {
            Text(text)
                .font(.system(size: 13, weight: .regular))
                .foregroundColor(Colors.textSecondary)
        }
    }

    // MARK: - Spacing

    struct Spacing {
        static let screenHorizontal: CGFloat = 24
        static let screenVertical: CGFloat = 16
        static let betweenSections: CGFloat = 32
        static let betweenCards: CGFloat = 16
        static let cardPadding: CGFloat = 20
        static let buttonHeight: CGFloat = 56
    }

    // MARK: - Layout Modifiers

    struct Modifiers {
        // Standard screen padding
        static func screenPadding() -> some ViewModifier {
            ScreenPaddingModifier()
        }

        // Card style
        static func card() -> some ViewModifier {
            CardModifier()
        }

        // Primary button style
        static func primaryButton() -> some ViewModifier {
            PrimaryButtonModifier()
        }
    }
}

// MARK: - View Modifiers

struct ScreenPaddingModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding(.horizontal, DAWTDesign.Spacing.screenHorizontal)
            .padding(.vertical, DAWTDesign.Spacing.screenVertical)
    }
}

struct CardModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding(DAWTDesign.Spacing.cardPadding)
            .background(DAWTDesign.Colors.cardBackground)
            .cornerRadius(12)
            .shadow(color: Color.black.opacity(0.04), radius: 8, x: 0, y: 2)
    }
}

struct PrimaryButtonModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .frame(maxWidth: .infinity)
            .frame(height: DAWTDesign.Spacing.buttonHeight)
            .background(DAWTDesign.Colors.accent)
            .foregroundColor(.white)
            .cornerRadius(12)
    }
}

// MARK: - Convenience Extensions

extension View {
    func dawtScreenPadding() -> some View {
        modifier(ScreenPaddingModifier())
    }

    func dawtCard() -> some View {
        modifier(CardModifier())
    }

    func dawtPrimaryButton() -> some View {
        modifier(PrimaryButtonModifier())
    }
}

// MARK: - Color Extension for Hex Support

extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }

        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue:  Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}
