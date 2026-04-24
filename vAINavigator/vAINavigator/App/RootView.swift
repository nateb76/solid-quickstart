import SwiftUI
import SwiftData

/// Top-level view that selects between onboarding and the main experience.
///
/// Session 1 scope: routes to `ProjectListView` unconditionally. Onboarding flow
/// will be wired once `HealthKitService` permission state is observable and the
/// onboarding screens are fleshed out.
struct RootView: View {
    @AppStorage("hasCompletedOnboarding") private var hasCompletedOnboarding: Bool = false

    var body: some View {
        if hasCompletedOnboarding {
            ProjectListView()
        } else {
            OnboardingView(onComplete: { hasCompletedOnboarding = true })
        }
    }
}

#Preview {
    RootView()
        .modelContainer(for: [Project.self, Workout.self], inMemory: true)
        .environment(HealthKitService.shared)
}
