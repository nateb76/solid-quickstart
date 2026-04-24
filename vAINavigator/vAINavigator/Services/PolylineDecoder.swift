import Foundation
import CoreLocation

/// Decoder for Google's encoded polyline algorithm format.
///
/// Reference: https://developers.google.com/maps/documentation/utilities/polylinealgorithm
enum PolylineDecoder {

    /// Decodes a Google-encoded polyline into an array of coordinates.
    ///
    /// Returns an empty array for a malformed or empty input.
    static func decode(_ encoded: String) -> [CLLocationCoordinate2D] {
        var coordinates: [CLLocationCoordinate2D] = []
        var index = encoded.startIndex
        let end = encoded.endIndex

        var latitude = 0
        var longitude = 0

        while index < end {
            guard let latDelta = decodeValue(encoded, index: &index, end: end) else { break }
            latitude += latDelta
            guard let lngDelta = decodeValue(encoded, index: &index, end: end) else { break }
            longitude += lngDelta

            coordinates.append(
                CLLocationCoordinate2D(
                    latitude: Double(latitude) / 1e5,
                    longitude: Double(longitude) / 1e5
                )
            )
        }

        return coordinates
    }

    /// Decodes a single variable-length signed value from the encoded string,
    /// advancing `index` past it. Returns `nil` on truncation.
    private static func decodeValue(
        _ encoded: String,
        index: inout String.Index,
        end: String.Index
    ) -> Int? {
        var shift = 0
        var result = 0

        while index < end {
            let byte = Int(encoded[index].asciiValue ?? 0) - 63
            index = encoded.index(after: index)
            result |= (byte & 0x1F) << shift
            shift += 5
            if byte < 0x20 { break }
            if shift >= 32 { return nil } // overflow guard
        }

        // Sign extension: LSB is the sign bit.
        let delta = (result & 1) != 0 ? ~(result >> 1) : (result >> 1)
        return delta
    }
}
