import Foundation
import CoreLocation

/// Result of a successful Google Directions API call.
struct DirectionsResult: Sendable {
    let encodedPolyline: String
    let totalMiles: Double
}

enum DirectionsError: Error, LocalizedError {
    case missingAPIKey
    case invalidResponse
    case noRoute
    case http(status: Int, body: String)
    case underlying(Error)

    var errorDescription: String? {
        switch self {
        case .missingAPIKey:
            return "Google Maps API key is not configured."
        case .invalidResponse:
            return "We couldn't understand the Directions API response."
        case .noRoute:
            return "We couldn't find a route between those locations."
        case .http(let status, _):
            return "Directions request failed (\(status))."
        case .underlying(let error):
            return error.localizedDescription
        }
    }
}

/// Thin async/await wrapper over the Google Directions REST API.
///
/// Kept stateless so it can be constructed cheaply from view models.
struct GoogleDirectionsService {

    let apiKey: String
    let session: URLSession

    init(apiKey: String = Secrets.googleMapsAPIKey, session: URLSession = .shared) {
        self.apiKey = apiKey
        self.session = session
    }

    /// Requests driving directions and returns the overview polyline + total
    /// distance in miles (summed across all legs).
    func fetchRoute(
        from origin: CLLocationCoordinate2D,
        to destination: CLLocationCoordinate2D
    ) async throws -> DirectionsResult {
        guard !apiKey.isEmpty, apiKey != "YOUR_KEY_HERE" else {
            throw DirectionsError.missingAPIKey
        }

        var components = URLComponents(string: "https://maps.googleapis.com/maps/api/directions/json")
        components?.queryItems = [
            URLQueryItem(name: "origin", value: "\(origin.latitude),\(origin.longitude)"),
            URLQueryItem(name: "destination", value: "\(destination.latitude),\(destination.longitude)"),
            URLQueryItem(name: "mode", value: "driving"),
            URLQueryItem(name: "key", value: apiKey)
        ]
        guard let url = components?.url else { throw DirectionsError.invalidResponse }

        let (data, response): (Data, URLResponse)
        do {
            (data, response) = try await session.data(from: url)
        } catch {
            throw DirectionsError.underlying(error)
        }

        if let http = response as? HTTPURLResponse, !(200...299).contains(http.statusCode) {
            throw DirectionsError.http(
                status: http.statusCode,
                body: String(data: data, encoding: .utf8) ?? ""
            )
        }

        let decoded: DirectionsRootDTO
        do {
            decoded = try JSONDecoder().decode(DirectionsRootDTO.self, from: data)
        } catch {
            throw DirectionsError.invalidResponse
        }

        guard decoded.status == "OK", let route = decoded.routes.first else {
            throw DirectionsError.noRoute
        }

        let meters = route.legs.reduce(0.0) { $0 + $1.distance.value }
        let miles = meters / 1609.344
        return DirectionsResult(
            encodedPolyline: route.overviewPolyline.points,
            totalMiles: miles
        )
    }
}

// MARK: - DTOs

private struct DirectionsRootDTO: Decodable {
    let status: String
    let routes: [RouteDTO]
}

private struct RouteDTO: Decodable {
    let overviewPolyline: PolylineDTO
    let legs: [LegDTO]

    enum CodingKeys: String, CodingKey {
        case overviewPolyline = "overview_polyline"
        case legs
    }
}

private struct PolylineDTO: Decodable {
    let points: String
}

private struct LegDTO: Decodable {
    let distance: DistanceDTO
}

private struct DistanceDTO: Decodable {
    /// Distance in meters.
    let value: Double
}
