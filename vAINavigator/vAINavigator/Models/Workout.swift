import Foundation
import SwiftData
import CoreLocation
import HealthKit

/// A single qualifying HealthKit workout imported into a project.
///
/// The adjustment from raw distance to `adjustedMiles` folds elevation gain
/// into the distance budget via the rule:
///
///     adjustedMiles = rawMiles + (elevationGainFeet / divisor)
///
/// where `divisor` is a user preference (default 500; see `SettingsView`).
@Model
final class Workout {
    @Attribute(.unique) var id: UUID

    /// Dedup key — mirrors `HKWorkout.uuid`.
    var healthKitUUID: UUID

    var date: Date
    var rawDistanceMiles: Double
    var elevationGainFeet: Double
    var adjustedMiles: Double

    /// Cumulative adjusted miles at the moment this workout was recorded
    /// (i.e. this workout's end position along the route).
    var routePositionMiles: Double

    var coordinateLatitude: Double
    var coordinateLongitude: Double

    /// Raw value of `HKWorkoutActivityType`. Stored as Int for SwiftData
    /// compatibility without an explicit Codable bridge.
    var activityTypeRaw: Int

    var project: Project?

    init(
        id: UUID = UUID(),
        healthKitUUID: UUID,
        date: Date,
        rawDistanceMiles: Double,
        elevationGainFeet: Double,
        adjustedMiles: Double,
        routePositionMiles: Double,
        coordinate: CLLocationCoordinate2D,
        activityType: HKWorkoutActivityType,
        project: Project? = nil
    ) {
        self.id = id
        self.healthKitUUID = healthKitUUID
        self.date = date
        self.rawDistanceMiles = rawDistanceMiles
        self.elevationGainFeet = elevationGainFeet
        self.adjustedMiles = adjustedMiles
        self.routePositionMiles = routePositionMiles
        self.coordinateLatitude = coordinate.latitude
        self.coordinateLongitude = coordinate.longitude
        self.activityTypeRaw = Int(activityType.rawValue)
        self.project = project
    }
}

extension Workout {
    var coordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(latitude: coordinateLatitude, longitude: coordinateLongitude)
    }

    var activityType: HKWorkoutActivityType {
        HKWorkoutActivityType(rawValue: UInt(activityTypeRaw)) ?? .other
    }
}

/// Applies the elevation-weighted adjustment to a raw distance + elevation pair.
///
/// If `elevationGainFeet` is non-positive or `divisor` is non-positive, the
/// adjusted value equals the raw value.
func adjustedMiles(
    rawMiles: Double,
    elevationGainFeet: Double,
    divisor: Double = 500
) -> Double {
    guard elevationGainFeet > 0, divisor > 0 else { return rawMiles }
    return rawMiles + (elevationGainFeet / divisor)
}
