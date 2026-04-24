import SwiftUI

/// Placeholder for the New Project flow.
///
/// Full implementation (Google Places autocomplete, route preview, Directions
/// call, save) ships in a subsequent session. Session 1 scope: sheet wiring
/// from the project list, visual skeleton, dismissal.
struct NewProjectView: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            ZStack {
                AppColor.background.ignoresSafeArea()
                VStack(spacing: 20) {
                    Spacer()
                    Image(systemName: "point.topleft.down.to.point.bottomright.curvepath")
                        .font(.system(size: 72, weight: .ultraLight))
                        .foregroundStyle(AppColor.primary)
                    Text("Create a new route")
                        .font(AppFont.title2)
                        .foregroundStyle(AppColor.textPrimary)
                    Text("Places autocomplete and Directions integration ship in the next session.")
                        .font(AppFont.body)
                        .foregroundStyle(AppColor.textSecondary)
                        .multilineTextAlignment(.center)
                        .padding(.horizontal, 32)
                    Spacer()
                    Spacer()
                }
            }
            .navigationTitle("New project")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
            }
        }
    }
}

#Preview {
    NewProjectView()
}
