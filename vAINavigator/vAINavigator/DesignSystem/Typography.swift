import SwiftUI

/// Typography ramp for vAI Navigator. System font (SF Pro) throughout so the
/// app feels native; rounded variant is reserved for numeric stat emphasis.
enum AppFont {

    // MARK: - Headers

    static let largeTitle: Font = .largeTitle.weight(.semibold)
    static let title: Font = .title.weight(.semibold)
    static let title2: Font = .title2.weight(.semibold)
    static let title3: Font = .title3.weight(.medium)
    static let headline: Font = .headline

    // MARK: - Body

    static let body: Font = .body
    static let bodyEmphasized: Font = .body.weight(.medium)
    static let callout: Font = .callout
    static let footnote: Font = .footnote
    static let caption: Font = .caption.weight(.medium)

    // MARK: - Numeric / stat

    /// Rounded numerics used for stat readouts. Works best for percentages,
    /// mile totals, and streak counters.
    static let statLarge: Font = .system(.largeTitle, design: .rounded, weight: .bold)
    static let stat: Font = .system(.title, design: .rounded, weight: .semibold)
    static let statSmall: Font = .system(.title3, design: .rounded, weight: .semibold)
}

extension View {
    /// Applies the app's secondary text color and the small caption face.
    func captionStyle() -> some View {
        self.font(AppFont.caption)
            .foregroundStyle(AppColor.textSecondary)
    }
}
