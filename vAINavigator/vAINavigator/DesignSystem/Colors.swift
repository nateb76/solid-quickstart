import SwiftUI

/// vAI Navigator palette — "Arc'teryx meets Linear".
///
/// All colors are defined programmatically (no asset catalog dependencies) so
/// the design system travels with the source, and so previews stay honest.
enum AppColor {

    // MARK: - Brand

    /// Deep forest green. Brand anchor.
    static let primary = Color(hex: 0x2D6A4F)
    /// Warm terracotta. Progress, pins, accents.
    static let accentWarm = Color(hex: 0xE07A3C)
    /// Slate blue. Secondary actions.
    static let accentCool = Color(hex: 0x4A7B9D)

    // MARK: - Surfaces

    static let background = Color(
        light: Color(hex: 0xFAFAF7),
        dark: Color(hex: 0x0E1412)
    )
    static let surface = Color(
        light: Color(hex: 0xFFFFFF),
        dark: Color(hex: 0x1A201E)
    )

    // MARK: - Text

    static let textPrimary = Color(
        light: Color(hex: 0x1A201E),
        dark: Color(hex: 0xF5F2EC)
    )
    static let textSecondary = Color(
        light: Color(hex: 0x6B7570),
        dark: Color(hex: 0xA8B0AA)
    )

    // MARK: - Divider

    static let divider = Color(
        light: Color(hex: 0xE5E3DC),
        dark: Color(hex: 0x2A312D)
    )

    // MARK: - Route overlays

    static let routeUntraveled = Color(hex: 0xA8B0AA).opacity(0.5)
    static let routeTraveledStart = Color(hex: 0xE07A3C)
    static let routeTraveledEnd = Color(hex: 0x2D6A4F)
}

// MARK: - Color helpers

extension Color {
    /// Builds a `Color` from a 24-bit RGB hex literal, e.g. `0x2D6A4F`.
    init(hex: UInt32, opacity: Double = 1.0) {
        let r = Double((hex >> 16) & 0xFF) / 255
        let g = Double((hex >> 8) & 0xFF) / 255
        let b = Double(hex & 0xFF) / 255
        self.init(.sRGB, red: r, green: g, blue: b, opacity: opacity)
    }

    /// Convenience for light/dark pairs without an asset catalog entry.
    init(light: Color, dark: Color) {
        self = Color(UIColor { trait in
            trait.userInterfaceStyle == .dark
                ? UIColor(dark)
                : UIColor(light)
        })
    }
}
