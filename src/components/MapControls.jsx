import React, { useState } from 'react';
import {
  Layers,
  Compass,
  Crosshair,
  ZoomIn,
  ZoomOut,
  Maximize2,
  Box,
  Trees,
  Footprints,
  MapPin,
  Check,
  RotateCw,
  Sun,
  Moon,
  Sunrise,
  Radio
} from 'lucide-react';
import { SJEC_CENTER, SJEC_DEFAULT_ZOOM, SJEC_DEFAULT_PITCH, SJEC_DEFAULT_BEARING } from '../data/sjecBoundary.js';

export default function MapControls({
  is3DMode,
  onToggle3D,
  mapInstance,
  userLocation,
  onLocateUser,
  lightingTheme,
  onCycleLighting,
  isDroneOrbiting,
  onToggleDroneOrbit,
  showTrees,
  onToggleTrees,
  showPOIs,
  onTogglePOIs,
  showWalkways,
  onToggleWalkways
}) {
  const [showLayerMenu, setShowLayerMenu] = useState(false);

  const handleZoomIn = () => {
    if (mapInstance && mapInstance.current) {
      mapInstance.current.zoomIn({ duration: 300 });
    }
  };

  const handleZoomOut = () => {
    if (mapInstance && mapInstance.current) {
      mapInstance.current.zoomOut({ duration: 300 });
    }
  };

  const handleRecenter = () => {
    if (mapInstance && mapInstance.current) {
      mapInstance.current.flyTo({
        center: SJEC_CENTER,
        zoom: SJEC_DEFAULT_ZOOM,
        pitch: is3DMode ? SJEC_DEFAULT_PITCH : 0,
        bearing: is3DMode ? SJEC_DEFAULT_BEARING : 0,
        duration: 1200
      });
    }
  };

  const handleResetNorth = () => {
    if (mapInstance && mapInstance.current) {
      mapInstance.current.easeTo({
        bearing: 0,
        duration: 800
      });
    }
  };

  const getLightingIcon = () => {
    switch (lightingTheme) {
      case 'sunset':
        return <Sunrise className="w-5 h-5 text-amber-400" />;
      case 'daylight':
        return <Sun className="w-5 h-5 text-yellow-300" />;
      case 'cyberpunk':
      default:
        return <Moon className="w-5 h-5 text-cyan-400" />;
    }
  };

  return (
    <div className="absolute bottom-6 right-4 z-30 flex flex-col items-end gap-2.5">
      {/* Overlays Menu */}
      {showLayerMenu && (
        <div className="mb-1 p-2 rounded-2xl bg-slate-900/95 backdrop-blur-2xl border border-slate-700/80 shadow-card-dark text-xs space-y-1 w-48 animate-in fade-in slide-in-from-bottom-2">
          <div className="px-2 py-1 text-[10px] font-bold tracking-wider text-slate-400 uppercase">
            Map Overlays & Layers
          </div>
          <button
            onClick={onToggleWalkways}
            className="w-full flex items-center justify-between px-2.5 py-1.5 rounded-xl hover:bg-slate-800 text-slate-200 transition-colors"
          >
            <span className="flex items-center gap-2">
              <Footprints className="w-3.5 h-3.5 text-cyan-400" />
              Pedestrian Paths
            </span>
            {showWalkways && <Check className="w-3.5 h-3.5 text-cyan-400" />}
          </button>
          <button
            onClick={onToggleTrees}
            className="w-full flex items-center justify-between px-2.5 py-1.5 rounded-xl hover:bg-slate-800 text-slate-200 transition-colors"
          >
            <span className="flex items-center gap-2">
              <Trees className="w-3.5 h-3.5 text-emerald-400" />
              Gardens & Trees
            </span>
            {showTrees && <Check className="w-3.5 h-3.5 text-cyan-400" />}
          </button>
          <button
            onClick={onTogglePOIs}
            className="w-full flex items-center justify-between px-2.5 py-1.5 rounded-xl hover:bg-slate-800 text-slate-200 transition-colors"
          >
            <span className="flex items-center gap-2">
              <MapPin className="w-3.5 h-3.5 text-amber-400" />
              Landmark POIs
            </span>
            {showPOIs && <Check className="w-3.5 h-3.5 text-cyan-400" />}
          </button>
        </div>
      )}

      {/* Main Controls Panel */}
      <div className="flex flex-col bg-slate-900/95 backdrop-blur-2xl border border-slate-700/80 rounded-2xl shadow-card-dark overflow-hidden divide-y divide-slate-800/80">
        {/* 3D Drone Cinematic Orbit Tour */}
        <button
          onClick={onToggleDroneOrbit}
          className={`p-3 transition-colors flex items-center justify-center ${
            isDroneOrbiting
              ? 'text-cyan-400 bg-cyan-500/20'
              : 'text-slate-400 hover:text-white hover:bg-slate-800'
          }`}
          title={isDroneOrbiting ? "Stop 3D Drone Orbit" : "Start Cinematic 3D Drone Tour"}
        >
          <RotateCw className={`w-5 h-5 ${isDroneOrbiting ? 'animate-spin' : ''}`} />
        </button>

        {/* Time-of-Day / Lighting Preset Switcher */}
        <button
          onClick={onCycleLighting}
          className="p-3 text-slate-400 hover:text-white hover:bg-slate-800 transition-colors flex items-center justify-center"
          title={`Lighting Preset: ${lightingTheme.toUpperCase()} (Click to change)`}
        >
          {getLightingIcon()}
        </button>

        {/* 2D / 2.5D Mode Switch Button */}
        <button
          onClick={onToggle3D}
          className={`p-3 transition-colors flex items-center justify-center ${
            is3DMode
              ? 'text-cyan-400 bg-cyan-500/10 hover:bg-cyan-500/20'
              : 'text-slate-400 hover:text-white hover:bg-slate-800'
          }`}
          title={is3DMode ? "Switch to Top-Down 2D View" : "Switch to Isometric 2.5D Tilt View"}
        >
          <Box className={`w-5 h-5 ${is3DMode ? 'animate-pulse' : ''}`} />
        </button>

        {/* Locate User GPS */}
        <button
          onClick={onLocateUser}
          className={`p-3 transition-colors flex items-center justify-center ${
            userLocation
              ? 'text-emerald-400 bg-emerald-500/10 hover:bg-emerald-500/20'
              : 'text-slate-400 hover:text-white hover:bg-slate-800'
          }`}
          title="Locate my real GPS position on campus"
        >
          <Crosshair className="w-5 h-5" />
        </button>

        {/* Layer Toggle Menu Trigger */}
        <button
          onClick={() => setShowLayerMenu(!showLayerMenu)}
          className={`p-3 transition-colors flex items-center justify-center ${
            showLayerMenu
              ? 'text-cyan-400 bg-slate-800'
              : 'text-slate-400 hover:text-white hover:bg-slate-800'
          }`}
          title="Map Overlays & Layers"
        >
          <Layers className="w-5 h-5" />
        </button>

        {/* Re-center Campus */}
        <button
          onClick={handleRecenter}
          className="p-3 text-slate-400 hover:text-white hover:bg-slate-800 transition-colors flex items-center justify-center"
          title="Re-center SJEC Campus"
        >
          <Maximize2 className="w-5 h-5" />
        </button>

        {/* Reset North */}
        <button
          onClick={handleResetNorth}
          className="p-3 text-slate-400 hover:text-white hover:bg-slate-800 transition-colors flex items-center justify-center"
          title="Reset Orientation (North Up)"
        >
          <Compass className="w-5 h-5" />
        </button>

        {/* Zoom In */}
        <button
          onClick={handleZoomIn}
          className="p-3 text-slate-400 hover:text-white hover:bg-slate-800 transition-colors flex items-center justify-center"
          title="Zoom In"
        >
          <ZoomIn className="w-5 h-5" />
        </button>

        {/* Zoom Out */}
        <button
          onClick={handleZoomOut}
          className="p-3 text-slate-400 hover:text-white hover:bg-slate-800 transition-colors flex items-center justify-center"
          title="Zoom Out"
        >
          <ZoomOut className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}
