import Foundation
import CoreLocation

/// Great-circle + route-walk math used to place pins along an encoded polyline.
enum DistanceCalculator {

    /// Earth's mean radius in miles, per the standard haversine convention.
    static let earthRadiusMiles: Double = 3958.8

    /// Haversine distance in miles between two points on Earth.
    static func haversineMiles(
        from a: CLLocationCoordinate2D,
        to b: CLLocationCoordinate2D
    ) -> Double {
        let lat1 = a.latitude.toRadians
        let lat2 = b.latitude.toRadians
        let dLat = (b.latitude - a.latitude).toRadians
        let dLng = (b.longitude - a.longitude).toRadians

        let h = sin(dLat / 2) * sin(dLat / 2)
            + cos(lat1) * cos(lat2)
            * sin(dLng / 2) * sin(dLng / 2)
        let c = 2 * atan2(sqrt(h), sqrt(1 - h))
        return earthRadiusMiles * c
    }

    /// Returns the coordinate that lies `targetMiles` along a polyline,
    /// walking segments and linearly interpolating the final fractional segment.
    ///
    /// - If `targetMiles <= 0`, returns the first coordinate.
    /// - If `targetMiles` exceeds the polyline length, returns the last coordinate.
    /// - Returns `nil` only for an empty coordinate array.
    static func coordinate(
        at targetMiles: Double,
        along coordinates: [CLLocationCoordinate2D]
    ) -> CLLocationCoordinate2D? {
        guard let first = coordinates.first else { return nil }
        guard coordinates.count > 1, targetMiles > 0 else { return first }

        var accumulated = 0.0
        for i in 0..<(coordinates.count - 1) {
            let segStart = coordinates[i]
            let segEnd = coordinates[i + 1]
            let segLength = haversineMiles(from: segStart, to: segEnd)
            if segLength == 0 { continue }

            if accumulated + segLength >= targetMiles {
                let remaining = targetMiles - accumulated
                let t = remaining / segLength
                return interpolate(from: segStart, to: segEnd, t: t)
            }
            accumulated += segLength
        }
        return coordinates.last
    }

    /// Linearly interpolates between two coordinates in lat/lng space.
    ///
    /// This is a pragmatic approximation — for short segments (which polyline
    /// legs typically are) the error vs. great-circle interpolation is
    /// negligible for pin placement.
    static func interpolate(
        from a: CLLocationCoordinate2D,
        to b: CLLocationCoordinate2D,
        t: Double
    ) -> CLLocationCoordinate2D {
        let clamped = max(0, min(1, t))
        return CLLocationCoordinate2D(
            latitude: a.latitude + (b.latitude - a.latitude) * clamped,
            longitude: a.longitude + (b.longitude - a.longitude) * clamped
        )
    }

    /// Total length of a polyline (sum of haversine segment distances).
    static func totalMiles(of coordinates: [CLLocationCoordinate2D]) -> Double {
        guard coordinates.count > 1 else { return 0 }
        var total = 0.0
        for i in 0..<(coordinates.count - 1) {
            total += haversineMiles(from: coordinates[i], to: coordinates[i + 1])
        }
        return total
    }
}

private extension Double {
    var toRadians: Double { self * .pi / 180 }
}
