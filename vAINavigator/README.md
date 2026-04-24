# vAI Navigator — iOS

A native iOS app in the Vayla AI family that turns real hikes, walks, and runs
into visual progress along a virtual route between any two points on Earth.

This is the **Session 1** scaffold. It delivers the project structure,
SwiftData models, HealthKit integration, design-system foundation, and the
project list UI. Map rendering, route creation, and Street View follow in
subsequent sessions.

---

## Requirements

- Xcode 15.3 or newer
- iOS 17.0+ deployment target
- A physical device (recommended) for HealthKit testing — the simulator has
  limited Health data.
- Swift 5.9+
- [XcodeGen](https://github.com/yonaskolb/XcodeGen) to materialize
  `vAINavigator.xcodeproj` from `project.yml`. (This repo intentionally does
  not commit the generated Xcode project.)

Install XcodeGen with Homebrew:

```sh
brew install xcodegen
```

## Setup

### 1. Generate the Xcode project

```sh
cd vAINavigator
xcodegen generate
open vAINavigator.xcodeproj
```

The first time Xcode opens the project it will resolve the Swift Package
dependencies (Google Maps + Google Places). This can take a minute.

### 2. Create a Google Cloud API key

1. In the [Google Cloud console](https://console.cloud.google.com/), create a
   new project (or select an existing one).
2. Enable the following APIs for that project:
   - **Maps SDK for iOS**
   - **Places SDK for iOS**
   - **Directions API**
   - **Geocoding API**
   - **Street View Static API** (for panorama fallbacks)
3. Create an API key under **APIs & Services → Credentials → Create credentials
   → API key**.
4. Restrict the key:
   - **Application restrictions → iOS apps**: add bundle ID
     `com.vaylaai.vAINavigator`.
   - **API restrictions**: limit to the five APIs above.

### 3. Add the key to the app

```sh
cp vAINavigator/Secrets.swift.template vAINavigator/Secrets.swift
```

Open `vAINavigator/Secrets.swift` and replace `YOUR_KEY_HERE` with your key.
`Secrets.swift` is gitignored — commit only `Secrets.swift.template`.

### 4. Build and run

Select the **vAINavigator** scheme and run on an iOS 17+ simulator or device.
On first launch:

- The onboarding flow requests HealthKit read access. Grant it on the
  Health dialog.
- From the project list, the `+` button launches the New Project flow
  (placeholder until the next session).

---

## Dependencies

Swift Package Manager only — no CocoaPods.

| Package | Purpose |
| --- | --- |
| [googlemaps/ios-maps-sdk](https://github.com/googlemaps/ios-maps-sdk) | `GMSMapView`, polyline rendering, markers |
| [googlemaps/ios-places-sdk](https://github.com/googlemaps/ios-places-sdk) | Places autocomplete for route endpoints |

Both are declared in `project.yml` and materialized into the generated
`.xcodeproj`.

---

## Folder structure

```
vAINavigator/
├── project.yml                       XcodeGen spec (source of truth)
├── README.md                         this file
└── vAINavigator/
    ├── App/                          SwiftUI lifecycle + RootView
    ├── Models/                       SwiftData @Model types
    ├── Services/                     HealthKit + Google API clients, math
    ├── ViewModels/                   @Observable VMs
    ├── Views/
    │   ├── Onboarding/
    │   ├── ProjectList/
    │   ├── ProjectDetail/            (shipped in a later session)
    │   ├── NewProject/               (stub)
    │   └── Settings/                 (stub)
    ├── DesignSystem/
    │   ├── Colors.swift
    │   ├── Typography.swift
    │   ├── Components/               StatCard, ProgressBar, ProjectCard
    │   └── MapStyles/                light.json + dark.json
    ├── Resources/
    │   ├── Assets.xcassets
    │   ├── Info.plist
    │   └── vAINavigator.entitlements
    ├── Secrets.swift.template
    └── Secrets.swift                 (gitignored; you create this locally)
```

---

## Session 1 scope

Delivered in this session:

- [x] Xcode project scaffold via `project.yml` (SwiftUI app lifecycle, iOS 17+)
- [x] SPM dependencies: `GoogleMaps`, `GooglePlaces`
- [x] `Secrets.swift.template` committed; `Secrets.swift` gitignored
- [x] `GMSServices.provideAPIKey()` + `GMSPlacesClient.provideAPIKey()` wired
      into `vAINavigatorApp.init()`
- [x] SwiftData `Project` and `Workout` models, with cascade deletion
- [x] `HealthKitService` — permission request, qualifying-activity filter,
      dedup via `healthKitUUID`, elevation extraction
- [x] `PolylineDecoder` and `DistanceCalculator` (haversine, pin interpolation)
- [x] `GoogleDirectionsService` and `GoogleGeocodingService`
      (async/await, typed errors)
- [x] Design system — palette, typography ramp, `ProgressBar`, `StatCard`,
      `ProjectCard`
- [x] `ProjectListView` with scope picker, empty state, floating "+" button,
      pull-to-refresh
- [x] `OnboardingView`, `NewProjectView`, `SettingsView` shells
- [x] Map style JSONs (light + dark)
- [x] Info.plist with HealthKit + location usage strings, entitlements file

Deferred to later sessions:

- [ ] `GoogleMapViewRepresentable` + route/pin rendering
- [ ] New project flow (Places autocomplete, route preview, save)
- [ ] Street View panorama detail sheet
- [ ] Milestones, pace projection, streak logic UI
- [ ] Settings controls (auto-assign, elevation divisor, reset data)
- [ ] Workout review/assignment sheet after sync

---

## Conventions

- SwiftUI + `@Observable` view models (no `ObservableObject`).
- `async/await` throughout; completion handlers only where Apple APIs require.
- MVVM with environment-based dependency injection.
- No force unwraps; errors surface as typed enums with `LocalizedError`
  descriptions.
- Keep views under 150 lines — extract subviews liberally.
