import realBuildingsData from './sjec_real_buildings.json';
import realRoofPartsData from './sjec_real_roof_parts.json';

export const sjecBuildingsGeoJSON = realBuildingsData;
export const sjecRoofPartsGeoJSON = realRoofPartsData;

// Quick lookup map by building ID (supports clean ID, Feature ID, and OSM ID)
export const buildingsById = sjecBuildingsGeoJSON.features.reduce((acc, feat) => {
  if (feat.properties?.id) acc[feat.properties.id] = feat.properties;
  if (feat.id) acc[feat.id] = feat.properties;
  if (feat.properties?.osm_id) acc[feat.properties.osm_id] = feat.properties;
  return acc;
}, {});
