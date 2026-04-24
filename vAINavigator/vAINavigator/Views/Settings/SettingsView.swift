import SwiftUI

/// Placeholder Settings screen. Session 1 scope: sheet shell + dismissal.
/// Full controls (auto-assign, elevation divisor, sync now, reset data) ship
/// in a subsequent session.
struct SettingsView: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            List {
                Section("Coming soon") {
                    Label("Auto-assign workouts", systemImage: "arrow.triangle.branch")
                    Label("Elevation adjustment divisor", systemImage: "mountain.2")
                    Label("Default map view", systemImage: "map")
                    Label("Sync now", systemImage: "arrow.clockwise")
                }
                Section("About") {
                    HStack {
                        Text("Version")
                        Spacer()
                        Text(Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "—")
                            .foregroundStyle(AppColor.textSecondary)
                    }
                }
            }
            .navigationTitle("Settings")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }
}

#Preview {
    SettingsView()
}
