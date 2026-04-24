import SwiftUI
import SwiftData
import GoogleMaps
import GooglePlaces

@main
struct vAINavigatorApp: App {

    /// Shared SwiftData container for the app's persistent models.
    let modelContainer: ModelContainer

    init() {
        Self.configureGoogleServices()
        do {
            modelContainer = try ModelContainer(
                for: Project.self, Workout.self,
                configurations: ModelConfiguration(isStoredInMemoryOnly: false)
            )
        } catch {
            fatalError("Failed to initialize SwiftData container: \(error)")
        }
    }

    var body: some Scene {
        WindowGroup {
            RootView()
                .environment(HealthKitService.shared)
        }
        .modelContainer(modelContainer)
    }

    /// Registers the Google Maps + Places SDKs with the shared API key.
    ///
    /// If the API key is still the placeholder, we log a loud developer-facing
    /// warning but continue — this lets the project compile and run for UI work
    /// without map-related features.
    private static func configureGoogleServices() {
        let key = Secrets.googleMapsAPIKey
        guard !key.isEmpty, key != "YOUR_KEY_HERE" else {
            assertionFailure(
                """
                Google Maps API key is not configured.
                Copy Secrets.swift.template to Secrets.swift and paste your key.
                See README.md "Setup" for full instructions.
                """
            )
            return
        }
        GMSServices.provideAPIKey(key)
        GMSPlacesClient.provideAPIKey(key)
    }
}
