import SwiftUI

/// Three-step onboarding flow. Session 1 delivers the shell + copy; per-screen
/// artwork and animations land in a later pass.
struct OnboardingView: View {
    var onComplete: () -> Void

    @Environment(HealthKitService.self) private var healthKit
    @State private var step: Int = 0
    @State private var isRequestingAuth = false

    var body: some View {
        ZStack {
            AppColor.background.ignoresSafeArea()
            VStack {
                TabView(selection: $step) {
                    heroScreen.tag(0)
                    permissionsScreen.tag(1)
                    firstProjectScreen.tag(2)
                }
                .tabViewStyle(.page(indexDisplayMode: .always))
                .indexViewStyle(.page(backgroundDisplayMode: .always))

                controls
                    .padding(.horizontal, 24)
                    .padding(.bottom, 32)
            }
        }
    }

    // MARK: - Screens

    private var heroScreen: some View {
        VStack(spacing: 20) {
            Spacer()
            Image(systemName: "map.circle.fill")
                .font(.system(size: 96, weight: .ultraLight))
                .foregroundStyle(AppColor.primary)
            Text("Walk your way somewhere meaningful.")
                .font(AppFont.largeTitle)
                .multilineTextAlignment(.center)
                .foregroundStyle(AppColor.textPrimary)
                .padding(.horizontal, 32)
            Text("Turn every hike, walk, and run into progress along a route you care about.")
                .font(AppFont.body)
                .foregroundStyle(AppColor.textSecondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal, 40)
            Spacer()
            Spacer()
        }
    }

    private var permissionsScreen: some View {
        VStack(spacing: 20) {
            Spacer()
            Image(systemName: "heart.text.square.fill")
                .font(.system(size: 96, weight: .ultraLight))
                .foregroundStyle(AppColor.accentWarm)
            Text("Connect your workouts")
                .font(AppFont.title)
                .foregroundStyle(AppColor.textPrimary)
            Text("vAI Navigator reads hikes, walks, and runs from Apple Health to carry you along your route. Nothing leaves your device.")
                .font(AppFont.body)
                .foregroundStyle(AppColor.textSecondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal, 36)

            Button {
                Task { await requestAuth() }
            } label: {
                HStack {
                    if isRequestingAuth { ProgressView().tint(.white) }
                    Text(healthKit.authorizationState == .authorized
                         ? "Connected"
                         : "Enable Health access")
                }
                .font(AppFont.bodyEmphasized)
                .foregroundStyle(.white)
                .padding(.horizontal, 28)
                .padding(.vertical, 14)
                .background(AppColor.primary)
                .clipShape(Capsule())
            }
            .disabled(isRequestingAuth || healthKit.authorizationState == .authorized)
            .padding(.top, 8)

            Spacer()
            Spacer()
        }
    }

    private var firstProjectScreen: some View {
        VStack(spacing: 20) {
            Spacer()
            Image(systemName: "flag.checkered.circle.fill")
                .font(.system(size: 96, weight: .ultraLight))
                .foregroundStyle(AppColor.primary)
            Text("Let's set your first destination.")
                .font(AppFont.title)
                .multilineTextAlignment(.center)
                .foregroundStyle(AppColor.textPrimary)
            Text("You can create as many routes as you like — they all run in parallel.")
                .font(AppFont.body)
                .foregroundStyle(AppColor.textSecondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal, 36)
            Spacer()
            Spacer()
        }
    }

    // MARK: - Controls

    @ViewBuilder
    private var controls: some View {
        HStack {
            if step > 0 && step != 1 {
                Button("Skip", action: onComplete)
                    .foregroundStyle(AppColor.textSecondary)
            }
            Spacer()
            Button(step == 2 ? "Get started" : "Next") {
                if step == 2 {
                    onComplete()
                } else {
                    withAnimation { step += 1 }
                }
            }
            .font(AppFont.bodyEmphasized)
            .foregroundStyle(AppColor.primary)
            .disabled(step == 1 && healthKit.authorizationState == .notDetermined)
        }
    }

    // MARK: - Actions

    private func requestAuth() async {
        isRequestingAuth = true
        defer { isRequestingAuth = false }
        try? await healthKit.requestAuthorization()
    }
}

#Preview {
    OnboardingView(onComplete: {})
        .environment(HealthKitService.shared)
}
