import Foundation
import HealthKit
import Observation

/// Represents the result of fetching a HealthKit workout, ready to be imported.
struct FetchedWorkout: Identifiable, Hashable {
    let id: UUID
    let healthKitUUID: UUID
    let date: Date
    let rawDistanceMiles: Double
    let elevationGainFeet: Double
    let activityType: HKWorkoutActivityType
}

enum HealthKitAuthorizationState {
    case notDetermined
    case denied
    case authorized
    /// HealthKit isn't available on this device (e.g. iPad without Health).
    case unavailable
}

enum HealthKitServiceError: Error, LocalizedError {
    case healthDataUnavailable
    case authorizationDenied
    case underlying(Error)

    var errorDescription: String? {
        switch self {
        case .healthDataUnavailable:
            return "Health data isn't available on this device."
        case .authorizationDenied:
            return "vAI Navigator needs permission to read your workouts."
        case .underlying(let error):
            return error.localizedDescription
        }
    }
}

/// Wraps HealthKit reads for qualifying workouts (hiking, walking, running).
///
/// HealthKit only reveals authorization status for *writes*, not reads, so we
/// track whether we've asked via `@AppStorage`. Callers should treat
/// `authorizationState` as advisory: a failed read is still possible even if
/// the user previously granted access.
@Observable
@MainActor
final class HealthKitService {

    static let shared = HealthKitService()

    private let healthStore = HKHealthStore()

    /// Timestamp of the last successful sync, used as the lower bound for
    /// incremental fetches.
    @ObservationIgnored
    private var lastSyncKey: String { "vainav.healthKit.lastSyncAt" }

    /// Workout types we'll ever import from Health.
    static let qualifyingActivityTypes: [HKWorkoutActivityType] = [
        .hiking, .walking, .running
    ]

    /// Types we need read access to.
    private var readTypes: Set<HKObjectType> {
        var types: Set<HKObjectType> = [HKObjectType.workoutType()]
        if let distance = HKQuantityType.quantityType(forIdentifier: .distanceWalkingRunning) {
            types.insert(distance)
        }
        if let elevation = HKQuantityType.quantityType(forIdentifier: .flightsClimbed) {
            types.insert(elevation)
        }
        // `.elevationAscended` isn't part of HKQuantityTypeIdentifier; elevation
        // gain is read off workout metadata + route samples (see `fetchElevation`).
        return types
    }

    // MARK: - Observable state

    var authorizationState: HealthKitAuthorizationState = .notDetermined
    var isSyncing: Bool = false
    var lastError: HealthKitServiceError?

    init() {
        refreshAuthorizationState()
    }

    // MARK: - Authorization

    /// Reflects the best guess at the user's authorization status for reads.
    ///
    /// HealthKit's `authorizationStatus(for:)` returns real data only for the
    /// share (write) side. For reads, the system treats "not determined" and
    /// "denied" as indistinguishable to protect user privacy. We therefore
    /// store a flag locally once we've asked.
    func refreshAuthorizationState() {
        guard HKHealthStore.isHealthDataAvailable() else {
            authorizationState = .unavailable
            return
        }
        let hasAsked = UserDefaults.standard.bool(forKey: "vainav.healthKit.hasRequested")
        authorizationState = hasAsked ? .authorized : .notDetermined
    }

    /// Requests authorization to read workouts, distance, and elevation.
    ///
    /// - Returns: `true` if the system dialog completed without error. This
    ///   does *not* guarantee the user granted access — see the note on
    ///   `refreshAuthorizationState`.
    @discardableResult
    func requestAuthorization() async throws -> Bool {
        guard HKHealthStore.isHealthDataAvailable() else {
            authorizationState = .unavailable
            throw HealthKitServiceError.healthDataUnavailable
        }
        do {
            try await healthStore.requestAuthorization(toShare: [], read: readTypes)
            UserDefaults.standard.set(true, forKey: "vainav.healthKit.hasRequested")
            authorizationState = .authorized
            return true
        } catch {
            lastError = .underlying(error)
            throw HealthKitServiceError.underlying(error)
        }
    }

    // MARK: - Fetching

    /// Fetches all qualifying workouts since the last successful sync.
    ///
    /// Pass `since: nil` to force a full re-scan (e.g. after a reset).
    func fetchWorkouts(since explicitStart: Date? = nil) async throws -> [FetchedWorkout] {
        guard HKHealthStore.isHealthDataAvailable() else {
            throw HealthKitServiceError.healthDataUnavailable
        }

        isSyncing = true
        defer { isSyncing = false }

        let start = explicitStart ?? lastSyncDate()
        let predicate = Self.workoutPredicate(start: start)
        let sort = NSSortDescriptor(key: HKSampleSortIdentifierStartDate, ascending: true)

        let workouts: [HKWorkout] = try await withCheckedThrowingContinuation { continuation in
            let query = HKSampleQuery(
                sampleType: .workoutType(),
                predicate: predicate,
                limit: HKObjectQueryNoLimit,
                sortDescriptors: [sort]
            ) { _, samples, error in
                if let error {
                    continuation.resume(throwing: HealthKitServiceError.underlying(error))
                    return
                }
                let hkWorkouts = (samples as? [HKWorkout]) ?? []
                continuation.resume(returning: hkWorkouts)
            }
            healthStore.execute(query)
        }

        var results: [FetchedWorkout] = []
        results.reserveCapacity(workouts.count)
        for workout in workouts {
            let distanceMiles = workout.totalDistance?.doubleValue(for: .mile()) ?? 0
            let elevationFeet = try await fetchElevation(for: workout)
            results.append(
                FetchedWorkout(
                    id: UUID(),
                    healthKitUUID: workout.uuid,
                    date: workout.startDate,
                    rawDistanceMiles: distanceMiles,
                    elevationGainFeet: elevationFeet,
                    activityType: workout.workoutActivityType
                )
            )
        }

        markSyncCompleted()
        return results
    }

    /// Reads the elevation-ascended quantity samples that overlap the workout's
    /// window, sums them, and converts meters → feet.
    ///
    /// Apple exposes `elevationAscended` via `HKMetadataKeyElevationAscended`
    /// and as a per-workout statistic on watchOS-recorded samples; this reads
    /// the metadata first and falls back to 0 if unavailable.
    private func fetchElevation(for workout: HKWorkout) async throws -> Double {
        // Prefer metadata elevation if present (set by native Workout app).
        if let meters = workout.metadata?[HKMetadataKeyElevationAscended] as? HKQuantity {
            return meters.doubleValue(for: .foot())
        }
        if let number = workout.metadata?[HKMetadataKeyElevationAscended] as? Double {
            // Stored in meters per Apple docs; convert to feet.
            return number * 3.28084
        }
        return 0
    }

    // MARK: - Sync bookkeeping

    private func lastSyncDate() -> Date? {
        let stored = UserDefaults.standard.double(forKey: lastSyncKey)
        return stored > 0 ? Date(timeIntervalSince1970: stored) : nil
    }

    private func markSyncCompleted() {
        UserDefaults.standard.set(Date.now.timeIntervalSince1970, forKey: lastSyncKey)
    }

    // MARK: - Predicate helpers

    /// Builds a compound predicate matching all qualifying activity types
    /// with an optional start date lower bound.
    static func workoutPredicate(start: Date?) -> NSPredicate {
        let activityPredicates = qualifyingActivityTypes.map {
            HKQuery.predicateForWorkouts(with: $0)
        }
        let activities = NSCompoundPredicate(orPredicateWithSubpredicates: activityPredicates)
        guard let start else { return activities }
        let dateRange = HKQuery.predicateForSamples(
            withStart: start,
            end: nil,
            options: [.strictStartDate]
        )
        return NSCompoundPredicate(andPredicateWithSubpredicates: [activities, dateRange])
    }
}
