import React, { useEffect, useRef, useState } from 'react';
import maplibregl from 'maplibre-gl';
import {
  SJEC_CENTER,
  SJEC_DEFAULT_ZOOM,
  SJEC_DEFAULT_PITCH,
  SJEC_DEFAULT_BEARING,
  SJEC_MAX_BOUNDS,
  campusBoundaryGeoJSON,
  outsideMaskGeoJSON
} from '../data/sjecBoundary.js';
import {
  sjecBuildingsGeoJSON,
  sjecRoofPartsGeoJSON
} from '../data/sjecBuildings.js';
import { sjecRoadsWalkwaysGeoJSON } from '../data/sjecRoadsWalkways.js';
import {
  sjecGreeneryGroundsGeoJSON,
  sjecCourtMarkingsGeoJSON,
  campusTreesGeoJSON
} from '../data/sjecGreeneryGrounds.js';
import { sjecPOIsGeoJSON } from '../data/sjecPOIs.js';

export default function MapComponent({
  is3DMode,
  selectedBuildingId,
  onSelectBuilding,
  activeRouteGeoJSON,
  userLocation,
  activeCategory,
  lightingTheme = 'cyberpunk', // 'cyberpunk' | 'sunset' | 'daylight'
  isDroneOrbiting = false,
  showTrees = true,
  showPOIs = true,
  showWalkways = true,
  mapInstanceRef
}) {
  const mapContainerRef = useRef(null);
  const mapRef = useRef(null);
  const userMarkerRef = useRef(null);
  const animationFrameRef = useRef(null);
  const [hoveredBuilding, setHoveredBuilding] = useState(null);
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });

  // Natural architectural lighting parameters
  const getLightConfig = (theme) => {
    switch (theme) {
      case 'sunset':
        return {
          anchor: 'viewport',
          color: '#fed7aa', // Warm golden Mangaluru twilight
          intensity: 0.70,
          position: [1.8, 130, 24]
        };
      case 'night':
      case 'cyberpunk':
        return {
          anchor: 'viewport',
          color: '#cbd5e1',
          intensity: 0.45,
          position: [1.5, 210, 38]
        };
      case 'daylight':
      default:
        return {
          anchor: 'viewport',
          color: '#ffffff', // Crisp natural midday sunlight
          intensity: 0.85,
          position: [1.4, 65, 55] // 55° sun elevation, 65° azimuth: realistic architectural cast shadows
        };
    }
  };

  // Base theme palette - Photorealistic ground materials and architectural backdrop
  const getThemePalette = (theme) => {
    switch (theme) {
      case 'sunset':
        return {
          bg: '#0f0c1b',
          ground: '#2a4422',
          boundaryLine: '#475569',
          roadCasing: '#475569',
          roadCore: '#334155',
          walkwayCasing: '#64748b',
          walkwayCore: '#e2e8f0'
        };
      case 'night':
      case 'cyberpunk':
        return {
          bg: '#080d1a',
          ground: '#152b19',
          boundaryLine: '#334155',
          roadCasing: '#1e293b',
          roadCore: '#0f172a',
          walkwayCasing: '#334155',
          walkwayCore: '#94a3b8'
        };
      case 'daylight':
      default:
        return {
          bg: '#0f172a', // Clean, premium dark slate backdrop masking outside Vamanjoor
          ground: '#2e5824', // Lush, authentic coastal Karnataka natural grass turf
          boundaryLine: '#475569', // Subtle, clean architectural campus boundary line
          roadCasing: '#64748b', // Concrete curbs
          roadCore: '#334155', // Authentic asphalt driveway surface
          walkwayCasing: '#94a3b8', // Paver stone curbs
          walkwayCore: '#f1f5f9' // Light sandstone/concrete paver walkway
        };
    }
  };

  useEffect(() => {
    if (!mapContainerRef.current) return;

    const palette = getThemePalette(lightingTheme);

    const darkCampusStyle = {
      version: 8,
      name: "SJEC 2.5D Digital Twin Architectural",
      glyphs: "https://demotiles.maplibre.org/font/{fontstack}/{range}.pbf",
      sources: {
        "outside-mask": {
          type: "geojson",
          data: outsideMaskGeoJSON
        },
        "campus-boundary": {
          type: "geojson",
          data: campusBoundaryGeoJSON
        },
        "campus-greenery": {
          type: "geojson",
          data: sjecGreeneryGroundsGeoJSON
        },
        "campus-court-markings": {
          type: "geojson",
          data: sjecCourtMarkingsGeoJSON
        },
        "campus-trees": {
          type: "geojson",
          data: campusTreesGeoJSON
        },
        "campus-roads": {
          type: "geojson",
          data: sjecRoadsWalkwaysGeoJSON
        },
        "campus-buildings": {
          type: "geojson",
          data: sjecBuildingsGeoJSON,
          generateId: true
        },
        "campus-roof-parts": {
          type: "geojson",
          data: sjecRoofPartsGeoJSON,
          generateId: true
        },
        "campus-pois": {
          type: "geojson",
          data: sjecPOIsGeoJSON
        },
        "navigation-route": {
          type: "geojson",
          data: {
            type: "FeatureCollection",
            features: []
          }
        }
      },
      layers: [
        // 1. Base void background
        {
          id: "background",
          type: "background",
          paint: {
            "background-color": palette.bg
          }
        },

        // 2. Verified Campus Grounds Base (Natural tropical turf undertone)
        {
          id: "campus-ground-fill",
          source: "campus-boundary",
          type: "fill",
          paint: {
            "fill-color": palette.ground,
            "fill-opacity": 0.98
          }
        },

        // 3. Greenery, Lawns, Stadium Turf, Sports Courts, Gardens
        {
          id: "greenery-fill",
          source: "campus-greenery",
          type: "fill",
          paint: {
            "fill-color": ["coalesce", ["get", "color"], "#15803d"],
            "fill-opacity": ["coalesce", ["get", "opacity"], 0.95]
          }
        },
        {
          id: "greenery-outline",
          source: "campus-greenery",
          type: "line",
          paint: {
            "line-color": "#0d3319",
            "line-width": 1.2,
            "line-opacity": 0.7
          }
        },

        // 3b. Sports Pitch, Athletic Track Lanes & Court Markings (Crisp white regulation lines)
        {
          id: "court-markings-line",
          source: "campus-court-markings",
          type: "line",
          paint: {
            "line-color": ["coalesce", ["get", "color"], "#ffffff"],
            "line-width": ["coalesce", ["get", "width"], 1.5],
            "line-opacity": 0.95
          }
        },

        // 4. Roads Casing (Paved asphalt edge / concrete curbs)
        {
          id: "roads-casing",
          source: "campus-roads",
          type: "line",
          filter: ["==", ["get", "is_primary"], true],
          paint: {
            "line-color": palette.roadCasing || "#64748b",
            "line-width": 7.0,
            "line-opacity": 0.95
          }
        },

        // 5. Roads Core Surface (Authentic asphalt roadbed)
        {
          id: "roads-core",
          source: "campus-roads",
          type: "line",
          filter: ["==", ["get", "is_primary"], true],
          paint: {
            "line-color": palette.roadCore || "#334155",
            "line-width": 4.8,
            "line-opacity": 0.98
          }
        },
        // Road Centerline Dash (Highway & Main Avenue)
        {
          id: "roads-dash",
          source: "campus-roads",
          type: "line",
          filter: ["==", ["get", "is_primary"], true],
          paint: {
            "line-color": "#f8fafc",
            "line-width": 1.0,
            "line-dasharray": [4, 4],
            "line-opacity": 0.8
          }
        },

        // 6. Pedestrian Walkways (Realistic sandstone/concrete paver promenade)
        {
          id: "roads-pedestrian-casing",
          source: "campus-roads",
          type: "line",
          filter: ["==", ["get", "is_pedestrian"], true],
          layout: {
            "visibility": showWalkways ? "visible" : "none"
          },
          paint: {
            "line-color": palette.walkwayCasing || "#94a3b8",
            "line-width": 4.5,
            "line-opacity": 0.85
          }
        },
        {
          id: "roads-pedestrian",
          source: "campus-roads",
          type: "line",
          filter: ["==", ["get", "is_pedestrian"], true],
          layout: {
            "visibility": showWalkways ? "visible" : "none"
          },
          paint: {
            "line-color": palette.walkwayCore || "#f1f5f9",
            "line-width": 2.8,
            "line-opacity": 0.98
          }
        },

        // 7. Outside Area Mask (Inverted hole covering non-campus Vamanjoor terrain)
        {
          id: "outside-area-mask",
          source: "outside-mask",
          type: "fill",
          paint: {
            "fill-color": palette.bg,
            "fill-opacity": 1.0
          }
        },
        // Campus Perimeter Subtle Boundary Line
        {
          id: "campus-boundary-line",
          source: "campus-boundary",
          type: "line",
          paint: {
            "line-color": palette.boundaryLine,
            "line-width": 1.6,
            "line-opacity": 0.65
          }
        },

        // ====================================================================
        // 8. ARCHITECTURAL 3D BUILDING EXTRUSIONS & FACADES
        // ====================================================================

        // Tier 1: Foundation Plinth (Dressed laterite / granite base)
        {
          id: "buildings-plinth",
          source: "campus-buildings",
          type: "fill-extrusion",
          paint: {
            "fill-extrusion-color": ["coalesce", ["get", "plinth_color"], "#334155"],
            "fill-extrusion-height": [
              "interpolate",
              ["linear"],
              ["zoom"],
              15, 0,
              16, 1.4
            ],
            "fill-extrusion-base": 0,
            "fill-extrusion-opacity": 0.98
          }
        },

        // Tier 2: Main Facade Body (Full architectural height with sunlight gradient)
        {
          id: "buildings-extrusion",
          source: "campus-buildings",
          type: "fill-extrusion",
          paint: {
            "fill-extrusion-color": [
              "case",
              ["==", ["get", "id"], selectedBuildingId || ""],
              "#fed7aa",
              ["==", ["get", "id"], hoveredBuilding?.id || ""],
              "#ffffff",
              ["coalesce", ["get", "wall_color"], "#e2e8f0"]
            ],
            "fill-extrusion-height": [
              "interpolate",
              ["linear"],
              ["zoom"],
              15, 0,
              16, ["coalesce", ["get", "height"], 15]
            ],
            "fill-extrusion-base": [
              "interpolate",
              ["linear"],
              ["zoom"],
              15, 0,
              16, 1.4
            ],
            "fill-extrusion-opacity": 0.98,
            "fill-extrusion-vertical-gradient": true
          }
        },

        // Tier 3: Parapet Coping Trim (Architectural stone coping edge)
        {
          id: "buildings-roof-cap",
          source: "campus-buildings",
          type: "fill-extrusion",
          paint: {
            "fill-extrusion-color": [
              "case",
              ["==", ["get", "id"], selectedBuildingId || ""],
              "#fef08a",
              ["coalesce", ["get", "parapet_color"], "#f1f5f9"]
            ],
            "fill-extrusion-height": [
              "interpolate",
              ["linear"],
              ["zoom"],
              15, 0,
              16, ["coalesce", ["get", "height"], 15]
            ],
            "fill-extrusion-base": [
              "interpolate",
              ["linear"],
              ["zoom"],
              15, 0,
              16, ["-", ["coalesce", ["get", "height"], 15], 0.35]
            ],
            "fill-extrusion-opacity": 0.98,
            "fill-extrusion-vertical-gradient": true
          }
        },

        // Tier 4: Real 3D Pitched Roofs, Gables, & AB-III Rooftop Solar Grid
        {
          id: "buildings-pitched-roofs",
          source: "campus-roof-parts",
          type: "fill-extrusion",
          paint: {
            "fill-extrusion-color": ["coalesce", ["get", "roof_color"], "#852b1b"],
            "fill-extrusion-height": [
              "interpolate",
              ["linear"],
              ["zoom"],
              15, 0,
              16, ["coalesce", ["get", "height"], 16]
            ],
            "fill-extrusion-base": [
              "interpolate",
              ["linear"],
              ["zoom"],
              15, 0,
              16, ["coalesce", ["get", "base_height"], 14]
            ],
            "fill-extrusion-opacity": 0.98,
            "fill-extrusion-vertical-gradient": true
          }
        },

        // 9. Realistic Tree Canopies (3D Green spheres positioned across gardens)
        {
          id: "campus-trees-circles",
          source: "campus-trees",
          type: "circle",
          layout: {
            "visibility": showTrees ? "visible" : "none"
          },
          paint: {
            "circle-radius": [
              "interpolate",
              ["linear"],
              ["zoom"],
              15, 3,
              18, ["get", "radius"]
            ],
            "circle-color": "#15803d",
            "circle-opacity": 0.85,
            "circle-stroke-width": 1.5,
            "circle-stroke-color": "#0d3319"
          }
        },

        // 10. Navigation Walking Route
        {
          id: "navigation-route-glow",
          source: "navigation-route",
          type: "line",
          layout: {
            "line-cap": "round",
            "line-join": "round"
          },
          paint: {
            "line-color": "#06b6d4",
            "line-width": 9,
            "line-blur": 4,
            "line-opacity": 0.75
          }
        },
        {
          id: "navigation-route-core",
          source: "navigation-route",
          type: "line",
          layout: {
            "line-cap": "round",
            "line-join": "round"
          },
          paint: {
            "line-color": "#ffffff",
            "line-width": 4,
            "line-opacity": 0.98
          }
        },

        // 11. Landmark POI Badges (Revealed on close zoom to prevent visual clutter)
        {
          id: "pois-circles",
          source: "campus-pois",
          type: "circle",
          minzoom: 17.6,
          layout: {
            "visibility": showPOIs ? "visible" : "none"
          },
          paint: {
            "circle-radius": [
              "interpolate",
              ["linear"],
              ["zoom"],
              17.6, 4.0,
              19, 6.5
            ],
            "circle-color": ["get", "color"],
            "circle-stroke-width": 1.5,
            "circle-stroke-color": "#ffffff",
            "circle-opacity": 0.88
          }
        }
      ]
    };

    const map = new maplibregl.Map({
      container: mapContainerRef.current,
      style: darkCampusStyle,
      center: SJEC_CENTER,
      zoom: SJEC_DEFAULT_ZOOM,
      pitch: is3DMode ? SJEC_DEFAULT_PITCH : 0,
      bearing: is3DMode ? SJEC_DEFAULT_BEARING : 0,
      maxBounds: SJEC_MAX_BOUNDS,
      minZoom: 15.6,
      maxZoom: 19.8,
      attributionControl: false
    });

    map.addControl(new maplibregl.AttributionControl({
      compact: true,
      customAttribution: 'St Joseph Engineering College (SJEC) | CampusFlow Digital Twin'
    }), 'bottom-right');

    map.on('load', () => {
      try {
        map.setLight(getLightConfig(lightingTheme));
      } catch (e) {
        console.warn(e);
      }
    });

    const handleBuildingClick = (e) => {
      if (e.features && e.features.length > 0) {
        const feature = e.features[0];
        const buildingId = feature.properties.id;
        onSelectBuilding(buildingId);

        const geom = feature.geometry;
        if (geom && geom.coordinates) {
          let ring = geom.coordinates[0];
          if (Array.isArray(ring[0]) && Array.isArray(ring[0][0])) {
            ring = ring[0];
          }
          if (ring && ring.length > 0) {
            const centerLng = ring.reduce((sum, c) => sum + c[0], 0) / ring.length;
            const centerLat = ring.reduce((sum, c) => sum + c[1], 0) / ring.length;
            map.easeTo({
              center: [centerLng, centerLat],
              zoom: Math.max(map.getZoom(), 17.8),
              duration: 800
            });
          }
        }
      }
    };

    map.on('click', 'buildings-extrusion', handleBuildingClick);
    map.on('click', 'buildings-roof-cap', handleBuildingClick);
    map.on('click', 'buildings-plinth', handleBuildingClick);

    map.on('click', 'pois-circles', (e) => {
      if (e.features && e.features.length > 0) {
        const feature = e.features[0];
        const bId = feature.properties.buildingId;
        if (bId) {
          onSelectBuilding(bId);
        }
      }
    });

    map.on('mousemove', 'buildings-extrusion', (e) => {
      if (e.features && e.features.length > 0) {
        map.getCanvas().style.cursor = 'pointer';
        const props = e.features[0].properties;
        setHoveredBuilding(props);
        setTooltipPos({ x: e.point.x, y: e.point.y });
      }
    });

    map.on('mouseleave', 'buildings-extrusion', () => {
      map.getCanvas().style.cursor = '';
      setHoveredBuilding(null);
    });

    mapRef.current = map;
    if (mapInstanceRef) {
      mapInstanceRef.current = map;
    }

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      map.remove();
      mapRef.current = null;
    };
  }, []);

  // Update lighting theme dynamically
  useEffect(() => {
    if (!mapRef.current || !mapRef.current.isStyleLoaded()) return;
    try {
      mapRef.current.setLight(getLightConfig(lightingTheme));

      const palette = getThemePalette(lightingTheme);
      if (mapRef.current.getLayer('background')) {
        mapRef.current.setPaintProperty('background', 'background-color', palette.bg);
      }
      if (mapRef.current.getLayer('campus-ground-fill')) {
        mapRef.current.setPaintProperty('campus-ground-fill', 'fill-color', palette.ground);
      }
      if (mapRef.current.getLayer('outside-area-mask')) {
        mapRef.current.setPaintProperty('outside-area-mask', 'fill-color', palette.bg);
      }
      if (mapRef.current.getLayer('campus-boundary-line')) {
        mapRef.current.setPaintProperty('campus-boundary-line', 'line-color', palette.boundaryLine);
      }
    } catch (e) {
      console.warn("Could not set lighting property:", e);
    }
  }, [lightingTheme]);

  // Smooth continuous 3D Drone Orbit Mode
  useEffect(() => {
    if (!mapRef.current) return;

    if (isDroneOrbiting) {
      const orbit = () => {
        if (!mapRef.current) return;
        const currentBearing = mapRef.current.getBearing();
        mapRef.current.setBearing(currentBearing + 0.18);
        animationFrameRef.current = requestAnimationFrame(orbit);
      };
      animationFrameRef.current = requestAnimationFrame(orbit);
    } else {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
        animationFrameRef.current = null;
      }
    }

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
        animationFrameRef.current = null;
      }
    };
  }, [isDroneOrbiting]);

  // Sync 2D vs 2.5D Mode
  useEffect(() => {
    if (!mapRef.current) return;
    mapRef.current.easeTo({
      pitch: is3DMode ? SJEC_DEFAULT_PITCH : 0,
      bearing: is3DMode ? SJEC_DEFAULT_BEARING : 0,
      duration: 1000
    });
  }, [is3DMode]);

  // Sync selected building highlight
  useEffect(() => {
    if (!mapRef.current || !mapRef.current.isStyleLoaded()) return;
    try {
      if (mapRef.current.getLayer('buildings-extrusion')) {
        mapRef.current.setPaintProperty('buildings-extrusion', 'fill-extrusion-color', [
          "case",
          ["==", ["get", "id"], selectedBuildingId || ""],
          "#38bdf8",
          ["==", ["get", "id"], hoveredBuilding?.id || ""],
          "#67e8f9",
          ["coalesce", ["get", "wall_color"], ["get", "color"], "#e2e8f0"]
        ]);
      }
      if (mapRef.current.getLayer('buildings-roof-cap')) {
        mapRef.current.setPaintProperty('buildings-roof-cap', 'fill-extrusion-color', [
          "case",
          ["==", ["get", "id"], selectedBuildingId || ""],
          "#f0f9ff",
          ["coalesce", ["get", "roof_color"], "#852b1b"]
        ]);
      }
    } catch (e) {
      console.warn("Could not sync highlight:", e);
    }
  }, [selectedBuildingId, hoveredBuilding]);

  // Sync Active Route
  useEffect(() => {
    if (!mapRef.current || !mapRef.current.isStyleLoaded()) return;
    try {
      const routeSource = mapRef.current.getSource('navigation-route');
      if (routeSource) {
        routeSource.setData(activeRouteGeoJSON || {
          type: "FeatureCollection",
          features: []
        });
      }
    } catch (e) {
      console.warn("Could not sync route:", e);
    }
  }, [activeRouteGeoJSON]);

  // Sync Overlays
  useEffect(() => {
    if (!mapRef.current || !mapRef.current.isStyleLoaded()) return;
    try {
      if (mapRef.current.getLayer('roads-pedestrian')) {
        mapRef.current.setLayoutProperty('roads-pedestrian', 'visibility', showWalkways ? 'visible' : 'none');
      }
    } catch (e) {
      console.warn(e);
    }
  }, [showWalkways]);

  useEffect(() => {
    if (!mapRef.current || !mapRef.current.isStyleLoaded()) return;
    try {
      if (mapRef.current.getLayer('campus-trees-circles')) {
        mapRef.current.setLayoutProperty('campus-trees-circles', 'visibility', showTrees ? 'visible' : 'none');
      }
    } catch (e) {
      console.warn(e);
    }
  }, [showTrees]);

  useEffect(() => {
    if (!mapRef.current || !mapRef.current.isStyleLoaded()) return;
    try {
      if (mapRef.current.getLayer('pois-circles')) {
        mapRef.current.setLayoutProperty('pois-circles', 'visibility', showPOIs ? 'visible' : 'none');
      }
    } catch (e) {
      console.warn(e);
    }
  }, [showPOIs]);

  // Sync GPS Marker
  useEffect(() => {
    if (!mapRef.current) return;
    if (userLocation && userLocation.coord) {
      if (!userMarkerRef.current) {
        const el = document.createElement('div');
        el.className = 'user-gps-marker';
        el.innerHTML = '<div class="user-gps-pulse"></div><div class="user-gps-dot"></div>';
        userMarkerRef.current = new maplibregl.Marker({ element: el })
          .setLngLat(userLocation.coord)
          .addTo(mapRef.current);
      } else {
        userMarkerRef.current.setLngLat(userLocation.coord);
      }
    } else {
      if (userMarkerRef.current) {
        userMarkerRef.current.remove();
        userMarkerRef.current = null;
      }
    }
  }, [userLocation]);

  return (
    <div className="relative w-full h-full overflow-hidden select-none">
      <div ref={mapContainerRef} className="w-full h-full" />

      {hoveredBuilding && (
        <div
          className="absolute pointer-events-none z-30 px-3.5 py-2.5 rounded-xl bg-slate-900/95 backdrop-blur-md border border-cyan-500/50 text-xs shadow-glow-cyan transform -translate-x-1/2 -translate-y-full mb-3"
          style={{ left: `${tooltipPos.x}px`, top: `${tooltipPos.y}px` }}
        >
          <div className="font-bold text-white flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
            {hoveredBuilding.name}
          </div>
          <div className="text-[11px] text-cyan-300 font-mono mt-0.5">
            {hoveredBuilding.short_code ? `${hoveredBuilding.short_code} • ` : ''}
            {hoveredBuilding.levels || hoveredBuilding.floors} Floors • {hoveredBuilding.height}m Height
          </div>
        </div>
      )}
    </div>
  );
}
