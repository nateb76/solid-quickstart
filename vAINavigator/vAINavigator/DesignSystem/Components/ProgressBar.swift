import SwiftUI

/// Rounded progress bar with a warm-to-primary gradient fill.
///
/// Animates its fill on appear using a spring. Pass a `progress` in [0, 1];
/// values outside the range are clamped.
struct ProgressBar: View {
    var progress: Double
    var height: CGFloat = 10

    @State private var animatedProgress: Double = 0

    var body: some View {
        GeometryReader { proxy in
            ZStack(alignment: .leading) {
                Capsule()
                    .fill(AppColor.divider)

                Capsule()
                    .fill(
                        LinearGradient(
                            colors: [AppColor.accentWarm, AppColor.primary],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .frame(width: proxy.size.width * clamped(animatedProgress))
            }
        }
        .frame(height: height)
        .onAppear {
            withAnimation(.spring(response: 0.6, dampingFraction: 0.8)) {
                animatedProgress = progress
            }
        }
        .onChange(of: progress) { _, newValue in
            withAnimation(.spring(response: 0.4, dampingFraction: 0.8)) {
                animatedProgress = newValue
            }
        }
        .accessibilityElement()
        .accessibilityValue("\(Int(clamped(progress) * 100)) percent complete")
    }

    private func clamped(_ value: Double) -> Double {
        max(0, min(1, value))
    }
}

#Preview {
    VStack(spacing: 20) {
        ProgressBar(progress: 0.0)
        ProgressBar(progress: 0.21)
        ProgressBar(progress: 0.5)
        ProgressBar(progress: 0.92)
        ProgressBar(progress: 1.0)
    }
    .padding()
}
