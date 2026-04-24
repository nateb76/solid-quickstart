import Foundation
import SwiftData
import Observation

enum ProjectListScope: String, CaseIterable, Identifiable {
    case active
    case archived

    var id: String { rawValue }
    var label: String {
        switch self {
        case .active: return "Active"
        case .archived: return "Archived"
        }
    }
}

/// Drives the project list: filters by scope and triggers a pull-to-refresh
/// sync against HealthKit.
///
/// Session 1 scope: scope filtering + sync hook. Reassignment of newly
/// imported workouts lives in a subsequent session.
@Observable
@MainActor
final class ProjectListViewModel {
    var scope: ProjectListScope = .active
    var isSyncing: Bool = false
    var syncError: String?

    private let healthKit: HealthKitService

    init(healthKit: HealthKitService = .shared) {
        self.healthKit = healthKit
    }

    /// Filters projects according to the current scope.
    func filter(_ projects: [Project]) -> [Project] {
        switch scope {
        case .active:
            return projects.filter { !$0.isArchived }
        case .archived:
            return projects.filter { $0.isArchived }
        }
    }

    /// Triggered by pull-to-refresh. Fetches new workouts from HealthKit.
    ///
    /// This does not yet persist workouts to SwiftData (deferred to the
    /// review/assignment flow in a later session) — it merely confirms
    /// permission + connectivity and surfaces any errors.
    func refresh() async {
        isSyncing = true
        defer { isSyncing = false }
        do {
            if healthKit.authorizationState == .notDetermined {
                try await healthKit.requestAuthorization()
            }
            _ = try await healthKit.fetchWorkouts()
            syncError = nil
        } catch let error as HealthKitServiceError {
            syncError = error.localizedDescription
        } catch {
            syncError = error.localizedDescription
        }
    }
}
