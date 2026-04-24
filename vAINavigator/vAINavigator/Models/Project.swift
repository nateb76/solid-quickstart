import Foundation
import SwiftData
import CoreLocation

/// A virtual route between two geographic endpoints that a user is progressing along.
///
/// Progress is computed from the sum of `adjustedMiles` across all associated
/// `Workout` records.
@Model
final class Project {
    @Attribute(.unique) var id: UUID
    var name: String

    /// Human-readable label for the start location, e.g. `"Sandpoint, ID"`.
    var startLabel: String
    /// Human-readable label for the end location, e.g. `"Denver, CO"`.
    var endLabel: String

    var startLatitude: Double
    var startLongitude: Double
    var endLatitude: Double
    var endLongitude: Double

    /// Google's encoded polyline for the full route. Decoded on demand.
    var encodedPolyline: String

    /// Total route length in miles, derived from the Directions API response.
    var totalRouteMiles: Double

    var createdAt: Date

    /// Exactly one project should be `isActive` at a time for a given user.
    /// Enforced by the service layer, not by schema.
    var isActive: Bool
    var isArchived: Bool
    var completedAt: Date?

    @Relationship(deleteRule: .cascade, inverse: \Workout.project)
    var workouts: [Workout] = []

    init(
        id: UUID = UUID(),
        name: String,
        startLabel: String,
        endLabel: String,
        startCoordinate: CLLocationCoordinate2D,
        endCoordinate: CLLocationCoordinate2D,
        encodedPolyline: String,
        totalRouteMiles: Double,
        createdAt: Date = .now,
        isActive: Bool = true,
        isArchived: Bool = false,
        completedAt: Date? = nil
    ) {
        self.id = id
        self.name = name
        self.startLabel = startLabel
        self.endLabel = endLabel
        self.startLatitude = startCoordinate.latitude
        self.startLongitude = startCoordinate.longitude
        self.endLatitude = endCoordinate.latitude
        self.endLongitude = endCoordinate.longitude
        self.encodedPolyline = encodedPolyline
        self.totalRouteMiles = totalRouteMiles
        self.createdAt = createdAt
        self.isActive = isActive
        self.isArchived = isArchived
        self.completedAt = completedAt
    }
}

extension Project {
    var startCoordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(latitude: startLatitude, longitude: startLongitude)
    }

    var endCoordinate: CLLocationCoordinate2D {
        CLLocationCoordinate2D(latitude: endLatitude, longitude: endLongitude)
    }

    /// Sum of `adjustedMiles` across all workouts, clamped to the total route length.
    var traveledMiles: Double {
        min(workouts.reduce(0) { $0 + $1.adjustedMiles }, totalRouteMiles)
    }

    /// Fraction complete in [0, 1].
    var progressFraction: Double {
        guard totalRouteMiles > 0 else { return 0 }
        return min(traveledMiles / totalRouteMiles, 1.0)
    }

    var isCompleted: Bool {
        traveledMiles >= totalRouteMiles
    }
}
