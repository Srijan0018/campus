import realGroundsData from './sjec_real_grounds.json';
import realCourtMarkingsData from './sjec_real_court_markings.json';

export const sjecGreeneryGroundsGeoJSON = realGroundsData;
export const sjecCourtMarkingsGeoJSON = realCourtMarkingsData;

// Realistic 3D Tree Clusters positioned across actual SJEC campus gardens and perimeter
export const campusTreesGeoJSON = {
  type: "FeatureCollection",
  features: [
    // Mary's Garden & Quad Palms
    { type: "Feature", properties: { radius: 5.5, height: 9 }, geometry: { type: "Point", coordinates: [74.89855, 12.91105] } },
    { type: "Feature", properties: { radius: 6.0, height: 10 }, geometry: { type: "Point", coordinates: [74.89862, 12.91115] } },
    { type: "Feature", properties: { radius: 5.0, height: 8 }, geometry: { type: "Point", coordinates: [74.89850, 12.91095] } },
    // Student Square Green Canopies
    { type: "Feature", properties: { radius: 7.0, height: 11 }, geometry: { type: "Point", coordinates: [74.89895, 12.91065] } },
    { type: "Feature", properties: { radius: 6.5, height: 10 }, geometry: { type: "Point", coordinates: [74.89890, 12.91078] } },
    // Chapel Serenity Grotto Grove
    { type: "Feature", properties: { radius: 6.0, height: 10 }, geometry: { type: "Point", coordinates: [74.89905, 12.91112] } },
    { type: "Feature", properties: { radius: 6.5, height: 11 }, geometry: { type: "Point", coordinates: [74.89920, 12.91102] } },
    // Main Entrance Highway Avenue
    { type: "Feature", properties: { radius: 5.0, height: 8 }, geometry: { type: "Point", coordinates: [74.89750, 12.91050] } },
    { type: "Feature", properties: { radius: 5.5, height: 9 }, geometry: { type: "Point", coordinates: [74.89775, 12.91055] } },
    { type: "Feature", properties: { radius: 5.0, height: 8 }, geometry: { type: "Point", coordinates: [74.89800, 12.91060] } },
    { type: "Feature", properties: { radius: 6.0, height: 9 }, geometry: { type: "Point", coordinates: [74.89825, 12.91065] } },
    // Stadium & Athletic Field Perimeter Trees
    { type: "Feature", properties: { radius: 7.0, height: 12 }, geometry: { type: "Point", coordinates: [74.90020, 12.90940] } },
    { type: "Feature", properties: { radius: 7.5, height: 13 }, geometry: { type: "Point", coordinates: [74.90050, 12.90930] } },
    { type: "Feature", properties: { radius: 8.0, height: 13 }, geometry: { type: "Point", coordinates: [74.90100, 12.90935] } },
    { type: "Feature", properties: { radius: 7.0, height: 11 }, geometry: { type: "Point", coordinates: [74.90140, 12.90950] } },
    { type: "Feature", properties: { radius: 7.5, height: 12 }, geometry: { type: "Point", coordinates: [74.90145, 12.90990] } },
    // Gents Hostel & North Ridge Nature Buffers
    { type: "Feature", properties: { radius: 8.0, height: 14 }, geometry: { type: "Point", coordinates: [74.90020, 12.91180] } },
    { type: "Feature", properties: { radius: 8.5, height: 14 }, geometry: { type: "Point", coordinates: [74.90080, 12.91185] } },
    { type: "Feature", properties: { radius: 7.5, height: 12 }, geometry: { type: "Point", coordinates: [74.89950, 12.91220] } },
    { type: "Feature", properties: { radius: 8.0, height: 13 }, geometry: { type: "Point", coordinates: [74.89970, 12.91270] } }
  ]
};
