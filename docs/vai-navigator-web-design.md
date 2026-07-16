# vAI Navigator — Web App Design Brief

Part of the **Vayla AI** product family. Cross-platform web app (runs in any
modern browser on Linux, macOS, Windows, iOS, Android). This document is
self-contained and can be handed to Claude Code as the single source of truth.

---

## 1. Concept

A beautifully designed hiking/walking progress tracker that turns real
workouts into visual progress along virtual destination routes.

The user sets a virtual route between any two points on Earth
(e.g. "Sandpoint, ID → Denver, CO"). Every workout they log advances a
traveler marker along a real driving route and drops a pin at the precise
geographic location. Users can tap any pin to open an embedded Google
Street View panorama. Multiple concurrent projects, each with independent
progress.

**Key elevation-weighted equivalence:**

```
adjustedMiles = rawMiles + (elevationGainFeet / divisor)
```

Default `divisor = 500`. Display both raw and adjusted; never hide raw.

---

## 2. Non-goals

- No native mobile app in this document (see `vAINavigator/README.md` for the
  parallel iOS scaffold, currently paused).
- No account system, no cloud sync in v1 — data lives in the browser via
  IndexedDB.
- No push notifications in v1.
- No live GPS tracking — this is a *log-and-visualize* tool, not a workout
  recorder.

---

## 3. Tech stack

- **Framework:** SolidStart (already scaffolded in this repo — Solid.js + Vite)
- **Language:** TypeScript (strict mode)
- **Styling:** CSS Modules + CSS custom properties (no Tailwind — keeps the
  bundle lean and matches the existing repo). Design tokens live in
  `src/styles/tokens.css`.
- **Maps:** Google Maps JavaScript API (v3), loaded via
  [`@googlemaps/js-api-loader`](https://www.npmjs.com/package/@googlemaps/js-api-loader)
- **Places autocomplete:** Google Places Library (`libraries: ['places']`)
- **Directions:** Google Directions Service (client-side, via Maps JS)
- **Geocoding:** Google Geocoder (client-side, via Maps JS)
- **Street View:** Google `StreetViewPanorama` (embedded), fallback to Static
  Maps API image when no panorama is available within 50 km
- **Persistence:** IndexedDB via [`idb`](https://www.npmjs.com/package/idb)
  wrapped in a typed repository layer. No server database in v1.
- **State:** Solid signals + stores, no external state library
- **Icons:** [`lucide-solid`](https://lucide.dev/) — small, tree-shakeable
- **Testing:** Cypress (already in the repo) for happy-path E2E; Vitest for
  unit tests on distance math + polyline decoding
- **Deploy target:** Netlify (already configured in `netlify.toml`)

Node 20+, npm.

---

## 4. Workout data source

HealthKit is unavailable in browsers. Choose from any combination:

1. **Manual entry** (always available): date, activity type, distance,
   elevation gain, optional notes
2. **Strava OAuth import**: v1.1 — deferred behind a feature flag
3. **GPX / TCX file upload**: v1 — drag-and-drop `.gpx` → parse via
   `@mapbox/togeojson` (or a small custom parser), extract total distance and
   elevation gain

Qualifying activity types (mirrors the iOS brief):

- `hiking`
- `walking`
- `running`

Anything else is filtered out at import time.

---

## 5. Data model (IndexedDB)

Store definitions (keyed by `id: string` UUID unless noted):

### `projects` store
```ts
type Project = {
  id: string;                    // UUID v4
  name: string;
  startLabel: string;            // e.g. "Sandpoint, ID"
  endLabel: string;
  start: { lat: number; lng: number };
  end:   { lat: number; lng: number };
  encodedPolyline: string;       // Google's overview polyline
  totalRouteMiles: number;
  createdAt: number;             // epoch ms
  isActive: boolean;
  isArchived: boolean;
  completedAt: number | null;
  mapType: 'roadmap' | 'satellite' | 'hybrid' | 'terrain';
};
```

Indexes: `by-isActive`, `by-isArchived`, `by-createdAt`.

### `workouts` store
```ts
type Workout = {
  id: string;
  projectId: string;
  source: 'manual' | 'gpx' | 'strava';
  externalId?: string;           // dedup key when source !== 'manual'
  date: number;                  // epoch ms
  activityType: 'hiking' | 'walking' | 'running';
  rawDistanceMiles: number;
  elevationGainFeet: number;
  adjustedMiles: number;
  routePositionMiles: number;    // cumulative adjusted miles at end of workout
  coordinate: { lat: number; lng: number };
  notes?: string;
  createdAt: number;
};
```

Indexes: `by-projectId`, `by-date`, `by-externalId` (unique when present).

### `settings` store (single row, key = `'app'`)
```ts
type Settings = {
  key: 'app';
  elevationDivisor: number;      // default 500
  autoAssignActiveProject: boolean;
  defaultMapType: Project['mapType'];
  reverseGeocodeCache: Record<string, { label: string; expiresAt: number }>;
};
```

---

## 6. Core algorithms

Implement in `src/lib/` with matching Vitest coverage.

### 6.1 `adjustedMiles(rawMiles, elevationGainFeet, divisor)`
```ts
export function adjustedMiles(raw: number, gainFt: number, divisor = 500) {
  if (gainFt <= 0 || divisor <= 0) return raw;
  return raw + (gainFt / divisor);
}
```

### 6.2 Polyline decoding
Google's standard encoded polyline algorithm. Reference:
<https://developers.google.com/maps/documentation/utilities/polylinealgorithm>

```ts
export function decodePolyline(encoded: string): Array<[number, number]>;
```

Also available as `google.maps.geometry.encoding.decodePath` when the Maps JS
`geometry` library is loaded — prefer that at runtime, keep a pure-JS
implementation for tests + SSR.

### 6.3 Haversine distance
Earth radius **3958.8 miles**. Lat/lng in radians.

```ts
export function haversineMiles(a: LatLng, b: LatLng): number;
```

### 6.4 Pin coordinate at a given cumulative distance
Walk polyline segments, accumulate haversine distances, linearly interpolate
lat/lng inside the segment that straddles the target distance.

```ts
export function coordinateAt(
  targetMiles: number,
  polyline: Array<[number, number]>
): LatLng;
```

Edge cases: `targetMiles <= 0` returns first point; `targetMiles >= total`
returns last point; empty polyline returns `null`.

### 6.5 Incremental position updates
When a workout is added to a project:

1. Sort project workouts by `date` ascending
2. Recompute `routePositionMiles` as cumulative sum of `adjustedMiles`
3. Recompute `coordinate` via `coordinateAt` on the decoded polyline
4. Persist

When a workout is deleted or reassigned, re-run the same recompute on
**both** source and destination projects.

### 6.6 Route generation
1. Geocode `startLabel` and `endLabel` via `google.maps.Geocoder`
2. Request driving directions via `google.maps.DirectionsService`
3. Read `routes[0].overview_polyline` (already encoded) and sum
   `legs[].distance.value` for total meters → miles
4. Persist to the Project

### 6.7 Reverse-geocoding cache
Key by coordinate rounded to 2 decimal places (~1 km). TTL 30 days. Store in
the `settings.reverseGeocodeCache` map to avoid a burst of API calls on the
detail view.

---

## 7. Route map (file/folder structure)

```
src/
├── routes/
│   ├── index.tsx                     ProjectListPage (/)
│   ├── projects/
│   │   ├── new.tsx                   NewProjectPage (/projects/new)
│   │   └── [id].tsx                  ProjectDetailPage (/projects/:id)
│   ├── settings.tsx                  SettingsPage (/settings)
│   └── onboarding.tsx                OnboardingPage (/onboarding)
├── components/
│   ├── design-system/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── ProgressBar.tsx
│   │   ├── StatCard.tsx
│   │   ├── ProjectCard.tsx
│   │   ├── SegmentedControl.tsx
│   │   ├── Sheet.tsx                 draggable bottom sheet
│   │   └── EmptyState.tsx
│   ├── map/
│   │   ├── MapCanvas.tsx             wraps Google Maps JS init + refs
│   │   ├── RouteOverlay.tsx          untraveled polyline
│   │   ├── TraveledOverlay.tsx       gradient orange→green traveled portion
│   │   ├── WorkoutPin.tsx            single pin
│   │   ├── TravelerMarker.tsx        current position marker
│   │   ├── MapTypeMenu.tsx           roadmap/satellite/hybrid/terrain
│   │   └── StreetViewPanel.tsx       embedded panorama
│   ├── workout/
│   │   ├── ManualEntryForm.tsx
│   │   ├── GpxDropzone.tsx
│   │   └── WorkoutRow.tsx
│   └── onboarding/
│       └── OnboardingSlides.tsx
├── lib/
│   ├── db.ts                         IndexedDB open + typed repositories
│   ├── projects.ts                   repository for projects
│   ├── workouts.ts                   repository for workouts
│   ├── settings.ts                   repository for settings
│   ├── directions.ts                 Google Directions wrapper
│   ├── geocoding.ts                  Google Geocoder wrapper + cache
│   ├── distance.ts                   haversine, coordinateAt, adjustedMiles
│   ├── polyline.ts                   decodePolyline (fallback)
│   ├── gpx.ts                        GPX/TCX parser
│   ├── milestones.ts                 25/50/75/100% crossing detection
│   ├── streaks.ts                    consecutive-day counter
│   ├── pace.ts                       30-day pace + projection
│   └── mapsLoader.ts                 @googlemaps/js-api-loader singleton
├── stores/
│   ├── projects.ts                   Solid store + actions
│   ├── workouts.ts
│   └── ui.ts                         theme, active sheet, toasts
├── styles/
│   ├── tokens.css                    color + typography custom properties
│   ├── global.css
│   └── maps.css                      map style JSON handled in JS
├── config/
│   ├── mapStyles.ts                  light + dark map style JSON
│   └── env.ts                        VITE_GOOGLE_MAPS_API_KEY loader
├── root.tsx
├── entry-client.tsx
└── entry-server.tsx
```

Existing `src/components/Counter.*` and `src/routes/index.tsx`
(SolidStart demo) should be **deleted** — this rewrite replaces them.

---

## 8. Environment / secrets

Google Maps API key lives in a Vite env var:

```
# .env.local  (gitignored — already covered by /.env* patterns)
VITE_GOOGLE_MAPS_API_KEY=your_key_here
```

Committed template: `.env.example`:

```
VITE_GOOGLE_MAPS_API_KEY=
```

Loader (`src/config/env.ts`):

```ts
export const googleMapsApiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY;
if (!googleMapsApiKey) {
  console.warn(
    'Missing VITE_GOOGLE_MAPS_API_KEY. Copy .env.example to .env.local and paste your key.'
  );
}
```

Restrict the key in Google Cloud to **HTTP referrers**:
`http://localhost:3000/*`, plus your production origin (e.g.
`https://vai-navigator.netlify.app/*`). Enabled APIs:

- Maps JavaScript API
- Places API (JavaScript)
- Directions API
- Geocoding API
- Street View Static API (for panorama fallback image)

---

## 9. Views (feature spec)

### 9.1 OnboardingPage `/onboarding`
Three-slide flow, dismiss to `/`. Slides:
1. **Hero:** *"Walk your way somewhere meaningful."* Animated SVG map artwork.
2. **How it works:** three-step diagram (Pick a route → Log workouts →
   Watch yourself travel).
3. **First project:** CTA button routes to `/projects/new`.

Persist `hasCompletedOnboarding: true` in `settings` after last slide or
skip. First-run gate at `/` redirects to `/onboarding` if false.

### 9.2 ProjectListPage `/`
- Large title: `vAI Navigator`
- Segmented control: `Active` / `Archived`
- List of `ProjectCard`s (see Design System)
- Floating action button (`+`) → `/projects/new`
- Empty state with illustration + `Create your first route` CTA
- Header action (top right): gear icon → `/settings`

### 9.3 NewProjectPage `/projects/new`
- Text field: **Name**
- Google Places autocomplete: **Start**
- Google Places autocomplete: **End**
- Once both endpoints resolve, show a small map preview with the route
- Show total route distance
- If the user has ≥ 1 workout on any project, show projected completion at
  30-day pace
- `Save` button — disabled until route resolves. On save, persist Project and
  route to `/projects/:id`.
- Loading, no-route, and API-error states each surface a friendly message.

### 9.4 ProjectDetailPage `/projects/:id`
Full-screen `MapCanvas` with overlays:

**Map layers (z-order):**
- Full route polyline: `#A8B0AA` at 50% opacity, 4 px
- Traveled portion: gradient `#E07A3C` → `#2D6A4F`, 6 px, on top
- Traveler marker: circular avatar with hiker icon
- Workout pins: 8 px orange dots, tap opens `StreetViewPanel`

**Top overlay (translucent card):**
- Project name
- `247 / 1,150 mi · 21% complete`
- `Near Rock Springs, WY` (reverse-geocoded current position)
- `42 workouts logged`
- Close button → `/`

**Bottom draggable sheet** (three snap points):
- Small: stats (weekly adjusted mi, streak, projected completion date)
- Medium: workout list, chronological, newest first
- Large: full-screen workout list + add-workout entry point

**Workout list rows:** date, activity icon, raw mi, elevation, adjusted mi.
Row actions (swipe / kebab menu): Reassign project, Delete.

**Map type control (floating, top right):**
- Menu: `Normal` / `Satellite` / `Hybrid` / `Terrain`
- Persist last choice per project

**Add workout button (floating, bottom right):**
- Opens `ManualEntryForm` in a modal
- GPX drag-and-drop supported via `GpxDropzone` inside the modal

### 9.5 StreetViewPanel (modal from any workout pin)
- Date, activity icon, stats card (raw, elevation, adjusted)
- `"You reached this point in your journey"`
- Embedded `StreetViewPanorama` at the coordinate
  - First call `StreetViewService.getPanorama({ location, radius: 50000 })`
  - If none found, render a Static Maps satellite image at that coordinate
- Action menu: Reassign, Delete

### 9.6 SettingsPage `/settings`
- Elevation adjustment divisor (default 500; presets 333 / 500 / 1000 + custom)
- Auto-assign toggle
- Default map view
- `Reset all data` (double-confirmation, wipes IndexedDB)
- About: version from `import.meta.env.VITE_APP_VERSION`, link to privacy
  policy (`/privacy` static page)

---

## 10. Design system

### Palette (light / dark)
```
--color-primary:            #2D6A4F   (deep forest green — brand anchor)
--color-accent-warm:        #E07A3C   (terracotta — progress, pins)
--color-accent-cool:        #4A7B9D   (slate blue — secondary actions)
--color-bg:                 #FAFAF7   /  #0E1412
--color-surface:            #FFFFFF   /  #1A201E
--color-text-primary:       #1A201E   /  #F5F2EC
--color-text-secondary:     #6B7570   /  #A8B0AA
--color-divider:            #E5E3DC   /  #2A312D
```

Route overlays: same gradient in JS (`#E07A3C` → `#2D6A4F`), untraveled
`#A8B0AA` at 50% opacity.

### Typography
System font stack (`-apple-system, BlinkMacSystemFont, "SF Pro Text",
"Segoe UI", Roboto, sans-serif`), plus a rounded numeric face for stat
readouts:

```
--font-family-body:  system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
--font-family-num:   "SF Pro Rounded", ui-rounded, system-ui, sans-serif;

--font-size-caption: 12px;
--font-size-body:    16px;
--font-size-title:   22px;
--font-size-large:   34px;
--font-weight-semi:  600;
--font-weight-bold:  700;
```

### Components
- Cards: 16 px radius, `0 4px 12px rgba(0,0,0,0.08)` shadow
- Buttons: filled primary uses `--color-primary`, secondary uses outlined
- Progress bars: rounded, animated fill on mount (spring feel via
  CSS transition on `width`, 600 ms `cubic-bezier(0.34, 1.56, 0.64, 1)`)
- Bottom sheet: three snap points, swipe-to-dismiss, backdrop tap dismisses
- Map pins: small SVG rendered via `google.maps.Marker` with a custom icon

### Google Maps style JSON
Two style JSON files (light + dark) in `src/config/mapStyles.ts`. Roads
muted, landscape warm beige in light / deep green-black in dark, POIs
hidden except major parks. Switch based on `matchMedia('(prefers-color-scheme: dark)')`
and a manual override in Settings.

### Animation & haptics
- Spring transitions on card mount and progress fill
- Toasts for save/delete confirmations
- Web haptics not universal — skip unless the platform supports the
  Vibration API (Android). Do not attempt haptic feedback on desktop.

---

## 11. Special features

### 11.1 Milestones
Detect crossings of 25 / 50 / 75 / 100 %. On crossing, show a full-screen
celebration modal:
- Confetti animation (SVG particles, Solid)
- Reverse-geocoded nearest notable city name
- `You've reached Rock Springs, WY — halfway to Denver!`
- Optional `Share as image` → render the modal to canvas via
  `html-to-image`, offer a download

### 11.2 Streak tracking
Count consecutive UTC dates with at least one qualifying workout across all
projects. Displayed in the stats sheet. Reset visually if broken — no doom
copy.

### 11.3 Pace projection
Average adjusted miles per day across the last 30 days. Project completion
date on the current active project.

### 11.4 Reverse-geocoding cache
See §6.7.

---

## 12. Error handling

- All Google API calls wrap `try/catch`; typed error union propagates to the
  view layer, rendered via a shared `<Toast>` component.
- Missing API key → banner at the top of `/` linking to the README's setup
  section.
- Directions "no route" → inline error under the New Project form.
- Street View unavailable → static satellite image fallback (no error).
- IndexedDB unavailable (Safari private mode) → banner at boot, degraded to
  session-only in-memory store.

---

## 13. Testing

- **Unit (Vitest):** `distance.ts`, `polyline.ts`, `milestones.ts`,
  `streaks.ts`, `pace.ts`, `adjustedMiles`. Table-driven where possible.
- **E2E (Cypress, already in repo):** happy path — create a project, log
  three workouts, verify percentage + pin count.
- **Manual smoke:** Chrome desktop, Firefox desktop, Safari desktop, Safari
  iOS, Chrome Android.

---

## 14. Deployment

- `npm run build` produces the SolidStart bundle
- Netlify already configured via `netlify.toml`
- Add `VITE_GOOGLE_MAPS_API_KEY` in the Netlify dashboard (Build & Deploy →
  Environment)
- Ensure the production origin is added to the Google Cloud key's HTTP
  referrer allowlist

---

## 15. Session plan for Claude Code

Recommend splitting into three sessions to keep each PR reviewable:

### Session 1 — foundation
1. Delete the SolidStart demo (`Counter.*`, demo index)
2. Wire up `tokens.css`, base components (`Button`, `Card`, `ProgressBar`,
   `StatCard`, `ProjectCard`, `EmptyState`, `Sheet`)
3. IndexedDB layer + typed repositories (`db.ts`, `projects.ts`,
   `workouts.ts`, `settings.ts`)
4. `distance.ts`, `polyline.ts`, `adjustedMiles`, `coordinateAt` — with
   Vitest tests
5. `ProjectListPage` (empty state, cards, FAB) + `SettingsPage` (bones)
6. `OnboardingPage` (3 slides, gate on `/`)
7. `.env.example`, README setup section

### Session 2 — maps + routes
1. `mapsLoader.ts` (`@googlemaps/js-api-loader`)
2. `NewProjectPage` (Places autocomplete, Directions, preview map, save)
3. `MapCanvas` + `RouteOverlay` + `TraveledOverlay` + `TravelerMarker`
4. `ProjectDetailPage` (top card, bottom sheet skeleton, map type menu)
5. Reverse-geocoded "Near Rock Springs, WY" chip

### Session 3 — workouts + panorama + polish
1. `ManualEntryForm`, `GpxDropzone`, workout list, reassign/delete
2. Incremental position updates on add/delete/reassign
3. `StreetViewPanel` with Static Maps fallback
4. Milestones (crossing detection + celebration modal)
5. Streak + pace projection stats
6. Share-as-image
7. Cypress happy-path E2E

---

## 16. Tone & code quality

- TypeScript strict everywhere; no `any` without a `// eslint-disable-next-line`
  and a comment explaining why
- Small components — target under 150 lines; extract subviews liberally
- Signals + stores for state; avoid prop-drilling more than two levels
- No premature abstractions; three similar lines beats a bad hook
- Comments only for non-obvious *why*; identifiers do the *what* work
- No emojis in code

---

## Appendix A — Setup instructions (copy into README on first session)

```sh
# Prerequisites: Node 20+, npm
npm install
cp .env.example .env.local
# open .env.local and paste your Google Maps API key
npm run dev
```

Visit <http://localhost:3000>.

**Google Cloud key setup:**

1. Create/select a project in the Google Cloud console
2. Enable: Maps JavaScript API, Places API, Directions API, Geocoding API,
   Street View Static API
3. Create an API key
4. Restrict it to **HTTP referrers** with `http://localhost:3000/*` for
   development and your production origin for prod

---

## Appendix B — How to use this doc with Claude Code

Save this file at `docs/vai-navigator-web-design.md` in your repo. Then in a
Claude Code session:

```
Read docs/vai-navigator-web-design.md and complete Session 1. Commit each
substantive step. Ask me before making decisions that aren't specified in
the doc.
```

Claude Code will create all listed files, add the design tokens, wire the
IndexedDB layer, and hand you back a working `npm run dev` you can open in
any browser on any OS.
