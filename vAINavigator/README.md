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

The Xcode project (`vAINavigator.xcodeproj`) is committed. There's no
toolchain to install before opening it. `project.yml` is kept as a
secondary source of truth for anyone who prefers to regenerate via
[XcodeGen](https://github.com/yonaskolb/XcodeGen).

## Setup

### 1. Create your local Secrets file

The API key lives in `vAINavigator/Secrets.swift`, which is gitignored.
The project references that path, so create it **before** opening Xcode:

```sh
cd vAINavigator
cp vAINavigator/Secrets.swift.template vAINavigator/Secrets.swift
```

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

Open `vAINavigator/Secrets.swift` (you created it in step 1) and replace
`YOUR_KEY_HERE` with your key. `Secrets.swift` is gitignored — commit only
`Secrets.swift.template`.

### 4. Open, build, and run

```sh
open vAINavigator.xcodeproj
```

Xcode will resolve the Swift Package dependencies (Google Maps + Google Places)
on first open. This takes ~1 minute.

Signing: under **Target → Signing & Capabilities**, set the **Team** to your
Apple Developer team. If `com.vaylaai.vAINavigator` collides with an existing
provisioning profile, change the bundle identifier to something unique
(e.g. `com.yourname.vAINavigator`). HealthKit is already listed as a
capability via `vAINavigator.entitlements`.

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

Both are declared directly in `vAINavigator.xcodeproj` and also mirrored in
`project.yml` for anyone regenerating via XcodeGen.

---

## Folder structure

```
vAINavigator/
├── vAINavigator.xcodeproj/           Xcode project (committed)
├── project.yml                       XcodeGen spec (alternate/regeneration)
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
