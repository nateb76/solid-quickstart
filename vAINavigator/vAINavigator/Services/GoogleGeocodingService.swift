import Foundation
import CoreLocation

enum GeocodingError: Error, LocalizedError {
    case missingAPIKey
    case invalidResponse
    case noResult
    case http(status: Int)
    case underlying(Error)

    var errorDescription: String? {
        switch self {
        case .missingAPIKey: return "Google Maps API key is not configured."
        case .invalidResponse: return "We couldn't understand the Geocoding API response."
        case .noResult: return "No geocoding result was returned."
        case .http(let status): return "Geocoding request failed (\(status))."
        case .underlying(let error): return error.localizedDescription
        }
    }
}

/// Forward + reverse geocoding via the Google Geocoding REST API.
struct GoogleGeocodingService {

    let apiKey: String
    let session: URLSession

    init(apiKey: String = Secrets.googleMapsAPIKey, session: URLSession = .shared) {
        self.apiKey = apiKey
        self.session = session
    }

    /// Forward geocodes a human-readable address to a coordinate.
    func geocode(address: String) async throws -> CLLocationCoordinate2D {
        guard !apiKey.isEmpty, apiKey != "YOUR_KEY_HERE" else {
            throw GeocodingError.missingAPIKey
        }
        var components = URLComponents(string: "https://maps.googleapis.com/maps/api/geocode/json")
        components?.queryItems = [
            URLQueryItem(name: "address", value: address),
            URLQueryItem(name: "key", value: apiKey)
        ]
        guard let url = components?.url else { throw GeocodingError.invalidResponse }
        return try await requestCoordinate(from: url)
    }

    /// Reverse-geocodes a coordinate to a short human-readable label, e.g.
    /// `"Rock Springs, WY"`. Returns `nil` if no sensible label was produced.
    func reverseGeocodeCityLabel(
        for coordinate: CLLocationCoordinate2D
    ) async throws -> String? {
        guard !apiKey.isEmpty, apiKey != "YOUR_KEY_HERE" else {
            throw GeocodingError.missingAPIKey
        }
        var components = URLComponents(string: "https://maps.googleapis.com/maps/api/geocode/json")
        components?.queryItems = [
            URLQueryItem(
                name: "latlng",
                value: "\(coordinate.latitude),\(coordinate.longitude)"
            ),
            URLQueryItem(name: "result_type", value: "locality|administrative_area_level_3"),
            URLQueryItem(name: "key", value: apiKey)
        ]
        guard let url = components?.url else { throw GeocodingError.invalidResponse }

        let (data, response) = try await session.data(from: url)
        if let http = response as? HTTPURLResponse, !(200...299).contains(http.statusCode) {
            throw GeocodingError.http(status: http.statusCode)
        }

        let decoded: GeocodeRootDTO
        do {
            decoded = try JSONDecoder().decode(GeocodeRootDTO.self, from: data)
        } catch {
            throw GeocodingError.invalidResponse
        }

        guard decoded.status == "OK", let first = decoded.results.first else { return nil }
        return Self.shortCityLabel(from: first)
    }

    // MARK: - Helpers

    private func requestCoordinate(from url: URL) async throws -> CLLocationCoordinate2D {
        let (data, response): (Data, URLResponse)
        do {
            (data, response) = try await session.data(from: url)
        } catch {
            throw GeocodingError.underlying(error)
        }
        if let http = response as? HTTPURLResponse, !(200...299).contains(http.statusCode) {
            throw GeocodingError.http(status: http.statusCode)
        }
        let decoded: GeocodeRootDTO
        do {
            decoded = try JSONDecoder().decode(GeocodeRootDTO.self, from: data)
        } catch {
            throw GeocodingError.invalidResponse
        }
        guard decoded.status == "OK", let first = decoded.results.first else {
            throw GeocodingError.noResult
        }
        return CLLocationCoordinate2D(
            latitude: first.geometry.location.lat,
            longitude: first.geometry.location.lng
        )
    }

    /// Reduces a Geocoding result to a "City, State" style label when possible.
    private static func shortCityLabel(from result: GeocodeResultDTO) -> String? {
        let city = result.addressComponents.first { $0.types.contains("locality") }?.shortName
            ?? result.addressComponents.first { $0.types.contains("administrative_area_level_3") }?.shortName
        let region = result.addressComponents.first { $0.types.contains("administrative_area_level_1") }?.shortName
        switch (city, region) {
        case let (city?, region?): return "\(city), \(region)"
        case let (city?, nil): return city
        case let (nil, region?): return region
        default: return result.formattedAddress
        }
    }
}

// MARK: - DTOs

private struct GeocodeRootDTO: Decodable {
    let status: String
    let results: [GeocodeResultDTO]
}

private struct GeocodeResultDTO: Decodable {
    let geometry: GeometryDTO
    let formattedAddress: String?
    let addressComponents: [AddressComponentDTO]

    enum CodingKeys: String, CodingKey {
        case geometry
        case formattedAddress = "formatted_address"
        case addressComponents = "address_components"
    }
}

private struct GeometryDTO: Decodable {
    let location: LocationDTO
}

private struct LocationDTO: Decodable {
    let lat: Double
    let lng: Double
}

private struct AddressComponentDTO: Decodable {
    let shortName: String
    let types: [String]

    enum CodingKeys: String, CodingKey {
        case shortName = "short_name"
        case types
    }
}
