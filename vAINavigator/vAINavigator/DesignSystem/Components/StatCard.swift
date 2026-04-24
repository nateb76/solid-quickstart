import SwiftUI

/// A small card that presents a single stat — a rounded number with an
/// optional caption and SF Symbol icon.
struct StatCard: View {
    var title: String
    var value: String
    var symbol: String? = nil

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack(spacing: 6) {
                if let symbol {
                    Image(systemName: symbol)
                        .font(.caption)
                        .foregroundStyle(AppColor.accentWarm)
                }
                Text(title)
                    .captionStyle()
            }
            Text(value)
                .font(AppFont.stat)
                .foregroundStyle(AppColor.textPrimary)
                .minimumScaleFactor(0.6)
                .lineLimit(1)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(.horizontal, 14)
        .padding(.vertical, 12)
        .background(AppColor.surface)
        .clipShape(RoundedRectangle(cornerRadius: 16, style: .continuous))
        .shadow(color: .black.opacity(0.05), radius: 8, y: 2)
    }
}

#Preview {
    HStack {
        StatCard(title: "Traveled", value: "247 mi", symbol: "figure.hiking")
        StatCard(title: "Progress", value: "21%", symbol: "chart.line.uptrend.xyaxis")
    }
    .padding()
    .background(AppColor.background)
}
