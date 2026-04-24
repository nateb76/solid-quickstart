import SwiftUI

/// Card used in the project list. Shows name, endpoints, and progress.
struct ProjectCard: View {
    let project: Project

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            VStack(alignment: .leading, spacing: 6) {
                Text(project.name)
                    .font(AppFont.title2)
                    .foregroundStyle(AppColor.textPrimary)
                    .lineLimit(1)

                HStack(spacing: 6) {
                    Image(systemName: "mappin.circle.fill")
                        .foregroundStyle(AppColor.accentWarm)
                    Text(project.startLabel)
                        .lineLimit(1)
                    Image(systemName: "arrow.right")
                        .font(.caption.weight(.semibold))
                        .foregroundStyle(AppColor.textSecondary)
                    Image(systemName: "flag.checkered.circle.fill")
                        .foregroundStyle(AppColor.primary)
                    Text(project.endLabel)
                        .lineLimit(1)
                }
                .font(AppFont.footnote)
                .foregroundStyle(AppColor.textSecondary)
            }

            ProgressBar(progress: project.progressFraction)

            HStack(spacing: 4) {
                Text(Self.formatted(project.traveledMiles))
                    .font(AppFont.bodyEmphasized)
                    .foregroundStyle(AppColor.textPrimary)
                Text("of")
                    .foregroundStyle(AppColor.textSecondary)
                Text("\(Self.formatted(project.totalRouteMiles)) mi")
                    .font(AppFont.bodyEmphasized)
                    .foregroundStyle(AppColor.textPrimary)
                Text("·")
                    .foregroundStyle(AppColor.textSecondary)
                Text("\(Int((project.progressFraction * 100).rounded()))%")
                    .font(AppFont.bodyEmphasized)
                    .foregroundStyle(AppColor.primary)
                Spacer()
                if project.isCompleted {
                    Label("Completed", systemImage: "checkmark.seal.fill")
                        .font(AppFont.caption)
                        .foregroundStyle(AppColor.primary)
                }
            }
            .font(AppFont.footnote)
        }
        .padding(18)
        .background(AppColor.surface)
        .clipShape(RoundedRectangle(cornerRadius: 20, style: .continuous))
        .shadow(color: .black.opacity(0.08), radius: 12, y: 4)
    }

    private static func formatted(_ miles: Double) -> String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        formatter.maximumFractionDigits = miles < 10 ? 1 : 0
        formatter.minimumFractionDigits = 0
        return formatter.string(from: NSNumber(value: miles)) ?? "\(miles)"
    }
}

#Preview {
    let project = Project(
        name: "Sandpoint → Denver",
        startLabel: "Sandpoint, ID",
        endLabel: "Denver, CO",
        startCoordinate: .init(latitude: 48.27, longitude: -116.55),
        endCoordinate: .init(latitude: 39.74, longitude: -104.99),
        encodedPolyline: "",
        totalRouteMiles: 1150
    )
    return ProjectCard(project: project)
        .padding()
        .background(AppColor.background)
}
