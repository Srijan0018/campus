import realBoundaryData from './sjec_real_boundary.json';

// Exact Center of SJEC Campus from OSM Way 279811603
export const SJEC_CENTER = [74.89930, 12.91060]; // [lng, lat] - perfectly centered on academic core & quad
export const SJEC_DEFAULT_ZOOM = 17.4;
export const SJEC_DEFAULT_PITCH = 52;  // Natural isometric 2.5D tilt
export const SJEC_DEFAULT_BEARING = 0; // True North Up matching Google Maps standard

// Camera Angle Presets for iconic photo landmarks
export const CAMERA_PRESETS = {
  north_up: { center: [74.89930, 12.91060], zoom: 17.4, pitch: 52, bearing: 0, name: "Campus Overview (North Up)" },
  academic_core: { center: [74.89895, 12.91045], zoom: 18.0, pitch: 56, bearing: 25, name: "Student Square & Basketball Court" },
  josarena_view: { center: [74.89945, 12.91105], zoom: 18.4, pitch: 58, bearing: -35, name: "Josarena Open-Air Amphitheatre" },
  entrance_perspective: { center: [74.89760, 12.91055], zoom: 18.2, pitch: 60, bearing: 75, name: "Main Entrance Gate" },
  stadium_view: { center: [74.90070, 12.91020], zoom: 17.6, pitch: 54, bearing: -40, name: "Athletic Stadium & 400m Track" },
  top_down_2d: { center: [74.89930, 12.91060], zoom: 17.2, pitch: 0, bearing: 0, name: "2D Architectural Masterplan" }
};

// Exact boundary coordinates from OpenStreetMap Way 279811603
export const campusBoundaryCoordinates = realBoundaryData.features[0].geometry.coordinates[0];

// Bounding box for strict camera confinement
export const SJEC_MAX_BOUNDS = [
  [74.8950, 12.9070], // Southwest [lng, lat]
  [74.9045, 12.9145]  // Northeast [lng, lat]
];

// Inverted mask polygon: A large polygon covering the outside region
// with the exact SJEC 25-acre campus boundary as an interior hole.
export const outsideMaskGeoJSON = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: {
        name: "Outside Campus Mask",
        description: "Masks out all non-campus areas with clean dark backdrop"
      },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [74.8000, 12.8000],
            [75.0000, 12.8000],
            [75.0000, 13.0000],
            [74.8000, 13.0000],
            [74.8000, 12.8000]
          ],
          [...campusBoundaryCoordinates].reverse()
        ]
      }
    }
  ]
};

// Verified Campus Boundary Polygon
export const campusBoundaryGeoJSON = realBoundaryData;
