import React, { useState, useRef, useCallback, useEffect } from 'react';
import MapComponent from './components/MapComponent.jsx';
import SidebarInfo from './components/SidebarInfo.jsx';
import NavigationPanel from './components/NavigationPanel.jsx';
import SearchBar from './components/SearchBar.jsx';
import MapControls from './components/MapControls.jsx';
import {
  Layers,
  Compass,
  Footprints,
  Sparkles,
  MapPin,
  CheckCircle2,
  Box,
  RotateCw,
  Sun,
  Moon,
  CloudSun,
  Clock,
  Radio
} from 'lucide-react';
import { SJEC_CENTER, SJEC_DEFAULT_ZOOM, SJEC_DEFAULT_PITCH, SJEC_DEFAULT_BEARING, CAMERA_PRESETS } from './data/sjecBoundary.js';
import { getHaversineDistance } from './data/navigationNetwork.js';

export default function App() {
  const mapInstanceRef = useRef(null);

  // Core App State
  const [is3DMode, setIs3DMode] = useState(true);
  const [selectedBuildingId, setSelectedBuildingId] = useState(null);
  const [activeCategory, setActiveCategory] = useState('all');
  const [activeRouteGeoJSON, setActiveRouteGeoJSON] = useState(null);
  const [isNavigating, setIsNavigating] = useState(false);
  const [navDestinationId, setNavDestinationId] = useState(null);

  // Realism & Atmosphere Controls
  const [lightingTheme, setLightingTheme] = useState('daylight'); // 'daylight' (Google Maps style) | 'sunset' | 'night'
  const [isDroneOrbiting, setIsDroneOrbiting] = useState(false);

  // Overlay Visibility Toggles
  const [showTrees, setShowTrees] = useState(true);
  const [showPOIs, setShowPOIs] = useState(true);
  const [showWalkways, setShowWalkways] = useState(true);

  // User Geolocation State
  const [userLocation, setUserLocation] = useState(null);
  const [locationNotice, setLocationNotice] = useState(null);

  // Live Mangaluru Local Clock
  const [localTime, setLocalTime] = useState('');
  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setLocalTime(now.toLocaleTimeString('en-IN', {
        timeZone: 'Asia/Kolkata',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      }));
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  // Cycle lighting themes
  const handleCycleLighting = () => {
    setLightingTheme(prev => {
      if (prev === 'daylight') return 'sunset';
      if (prev === 'sunset') return 'night';
      return 'daylight';
    });
  };

  // Handle building selection
  const handleSelectBuilding = useCallback((buildingId) => {
    setSelectedBuildingId(buildingId);
    setIsNavigating(false);
  }, []);

  // Handle search item selection
  const handleSelectSearchResult = useCallback((item) => {
    if (item.buildingId) {
      setSelectedBuildingId(item.buildingId);
      setIsNavigating(false);
    }
    if (mapInstanceRef.current && item.coord) {
      mapInstanceRef.current.flyTo({
        center: item.coord,
        zoom: 18.2,
        pitch: is3DMode ? SJEC_DEFAULT_PITCH : 0,
        bearing: is3DMode ? SJEC_DEFAULT_BEARING : 0,
        duration: 1200
      });
    }
  }, [is3DMode]);

  // Start walking navigation to a building
  const handleStartNavigation = useCallback((destinationBuildingId) => {
    setNavDestinationId(destinationBuildingId);
    setSelectedBuildingId(null);
    setIsNavigating(true);
  }, []);

  // Handle GPS location query
  const handleLocateUser = () => {
    if (!navigator.geolocation) {
      setLocationNotice({
        type: 'warning',
        text: 'Geolocation is not supported by your browser.'
      });
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const userCoord = [pos.coords.longitude, pos.coords.latitude];
        const distToSJEC = getHaversineDistance(userCoord, SJEC_CENTER);

        if (distToSJEC < 3000) {
          setUserLocation({ coord: userCoord, isSimulated: false });
          setLocationNotice({
            type: 'success',
            text: `Located on SJEC campus! (${Math.round(distToSJEC)}m from center)`
          });
          if (mapInstanceRef.current) {
            mapInstanceRef.current.flyTo({
              center: userCoord,
              zoom: 18,
              duration: 1200
            });
          }
        } else {
          // Off-campus testing fallback: place marker at Main Highway Gate
          const simCoord = [74.897418, 12.910577];
          setUserLocation({ coord: simCoord, isSimulated: true });
          setLocationNotice({
            type: 'info',
            text: `You are ${(distToSJEC / 1000).toFixed(1)}km from SJEC. Simulating your position at Main Gate (NH 169).`
          });
          if (mapInstanceRef.current) {
            mapInstanceRef.current.flyTo({
              center: simCoord,
              zoom: 18,
              duration: 1200
            });
          }
        }
      },
      (err) => {
        const simCoord = [74.897418, 12.910577];
        setUserLocation({ coord: simCoord, isSimulated: true });
        setLocationNotice({
          type: 'info',
          text: 'Using simulated position at Main Highway Entrance (NH 169).'
        });
        if (mapInstanceRef.current) {
          mapInstanceRef.current.flyTo({
            center: simCoord,
            zoom: 18,
            duration: 1200
          });
        }
      },
      { enableHighAccuracy: true, timeout: 8000 }
    );
  };

  const handleSimulateUserStep = useCallback((coord) => {
    setUserLocation({ coord, isSimulated: true });
    if (mapInstanceRef.current) {
      mapInstanceRef.current.easeTo({
        center: coord,
        duration: 800
      });
    }
  }, []);

  return (
    <div className="relative w-screen h-screen overflow-hidden bg-[#070b14] select-none font-sans">
      {/* Top Header Navigation Bar */}
      <header className="absolute top-0 left-0 right-0 z-20 h-16 px-4 md:px-6 flex items-center justify-between pointer-events-none bg-gradient-to-b from-[#070b14]/95 via-[#070b14]/60 to-transparent backdrop-blur-md">
        {/* Left: Branding & Campus Status */}
        <div className="flex items-center gap-3.5 pointer-events-auto">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-cyan-400 via-sky-500 to-blue-600 flex items-center justify-center shadow-glow-cyan border border-cyan-400/30">
            <Box className="w-5 h-5 text-slate-950 font-bold" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-base font-extrabold text-white tracking-tight">
                SJEC <span className="text-cyan-400 font-mono">2.5D</span>
              </span>
              <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-cyan-500/15 text-cyan-300 border border-cyan-500/40 shadow-glow-cyan">
                REAL DIGITAL TWIN
              </span>
            </div>
            <div className="text-[11px] text-slate-300 flex items-center gap-1.5">
              <span>St Joseph Engineering College</span>
              <span className="text-slate-600">•</span>
              <span className="text-cyan-400/90 font-medium">Vamanjoor, Mangaluru</span>
            </div>
          </div>
        </div>

        {/* Center: Search Bar */}
        <div className="pointer-events-auto hidden md:block">
          <SearchBar
            onSelectResult={handleSelectSearchResult}
            activeCategory={activeCategory}
            onCategoryChange={setActiveCategory}
          />
        </div>

        {/* Right: Live Telemetry & Quick Action Buttons */}
        <div className="flex items-center gap-3 pointer-events-auto">
          {/* Live Mangaluru Weather & Local Time Badge */}
          <div className="hidden lg:flex items-center gap-3 px-3 py-1.5 rounded-2xl bg-slate-900/80 backdrop-blur-xl border border-slate-700/80 text-xs text-slate-300 shadow-card-dark">
            <div className="flex items-center gap-1 text-amber-300 font-medium">
              <CloudSun className="w-3.5 h-3.5" />
              <span>28°C Coastal</span>
            </div>
            <span className="text-slate-600">•</span>
            <div className="flex items-center gap-1 text-cyan-300 font-mono">
              <Clock className="w-3.5 h-3.5" />
              <span>{localTime || '10:00 PM IST'}</span>
            </div>
          </div>

          {/* AR Camera Landmark Presets */}
          <div className="relative hidden xl:block">
            <select
              onChange={(e) => {
                const key = e.target.value;
                if (CAMERA_PRESETS[key] && mapInstanceRef.current) {
                  const p = CAMERA_PRESETS[key];
                  mapInstanceRef.current.flyTo({
                    center: p.center,
                    zoom: p.zoom,
                    pitch: p.pitch,
                    bearing: p.bearing,
                    duration: 1400
                  });
                }
              }}
              defaultValue="north_up"
              className="bg-slate-900/90 text-slate-200 border border-slate-700/80 rounded-xl px-2.5 py-1.5 text-xs font-semibold focus:outline-none focus:border-cyan-400 cursor-pointer shadow-card-dark"
              title="Jump camera to authentic photo landmarks"
            >
              {Object.entries(CAMERA_PRESETS).map(([key, preset]) => (
                <option key={key} value={key} className="bg-slate-900 text-slate-200">
                  📷 {preset.name}
                </option>
              ))}
            </select>
          </div>

          {/* 3D Drone Orbit Tour Button */}
          <button
            onClick={() => setIsDroneOrbiting(!isDroneOrbiting)}
            className={`px-3 py-1.5 rounded-xl border text-xs font-bold flex items-center gap-1.5 transition-all shadow-card-dark ${
              isDroneOrbiting
                ? 'bg-cyan-500 text-slate-950 border-cyan-400 shadow-glow-cyan animate-pulse'
                : 'bg-slate-900/80 text-slate-200 border-slate-700/80 hover:bg-slate-800'
            }`}
            title="Start cinematic 360° drone camera tour around campus"
          >
            <RotateCw className={`w-3.5 h-3.5 ${isDroneOrbiting ? 'animate-spin' : ''}`} />
            <span className="hidden sm:inline">3D Drone Tour</span>
          </button>

          {/* Walking Guide Trigger */}
          <button
            onClick={() => {
              if (!isNavigating) {
                setSelectedBuildingId(null);
              }
              setIsNavigating(!isNavigating);
            }}
            className={`px-3 py-1.5 rounded-xl border text-xs font-bold flex items-center gap-1.5 transition-all shadow-card-dark ${
              isNavigating
                ? 'bg-cyan-500 text-slate-950 border-cyan-400 shadow-glow-cyan'
                : 'bg-slate-900/80 text-slate-200 border-slate-700/80 hover:bg-slate-800'
            }`}
          >
            <Footprints className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Walking Guide</span>
          </button>

          {/* 2D / 2.5D Mode Toggle */}
          <button
            onClick={() => setIs3DMode(!is3DMode)}
            className="px-3 py-1.5 rounded-xl bg-slate-900/80 text-slate-200 border border-slate-700/80 hover:bg-slate-800 text-xs font-semibold flex items-center gap-1.5 transition-all shadow-card-dark"
          >
            <Box className="w-3.5 h-3.5 text-cyan-400" />
            <span className="font-mono">{is3DMode ? '2.5D Isometric' : '2D Top-Down'}</span>
          </button>
        </div>
      </header>

      {/* Mobile Search Bar */}
      <div className="absolute top-16 left-4 right-4 z-20 md:hidden pointer-events-auto">
        <SearchBar
          onSelectResult={handleSelectSearchResult}
          activeCategory={activeCategory}
          onCategoryChange={setActiveCategory}
        />
      </div>

      {/* GPS Location Notification Banner */}
      {locationNotice && (
        <div className="absolute top-20 left-1/2 transform -translate-x-1/2 z-50 px-4 py-2 rounded-2xl bg-slate-900/95 backdrop-blur-xl border border-cyan-500/40 shadow-glow-cyan text-xs text-slate-200 flex items-center gap-2 animate-in fade-in slide-in-from-top-2">
          <CheckCircle2 className="w-4 h-4 text-cyan-400 shrink-0" />
          <span>{locationNotice.text}</span>
          <button
            onClick={() => setLocationNotice(null)}
            className="ml-2 text-slate-400 hover:text-white"
          >
            ✕
          </button>
        </div>
      )}

      {/* Main 2.5D WebGL Map Component */}
      <main className="w-full h-full">
        <MapComponent
          is3DMode={is3DMode}
          selectedBuildingId={selectedBuildingId}
          onSelectBuilding={handleSelectBuilding}
          activeRouteGeoJSON={activeRouteGeoJSON}
          userLocation={userLocation}
          activeCategory={activeCategory}
          lightingTheme={lightingTheme}
          isDroneOrbiting={isDroneOrbiting}
          showTrees={showTrees}
          showPOIs={showPOIs}
          showWalkways={showWalkways}
          mapInstanceRef={mapInstanceRef}
        />
      </main>

      {/* Floating Info Drawer for Selected Building */}
      {selectedBuildingId && (
        <SidebarInfo
          selectedBuildingId={selectedBuildingId}
          onClose={() => setSelectedBuildingId(null)}
          onStartNavigation={handleStartNavigation}
        />
      )}

      {/* Interactive Walking Navigation Planner */}
      {isNavigating && (
        <NavigationPanel
          initialDestinationId={navDestinationId}
          userLocation={userLocation}
          onClose={() => {
            setIsNavigating(false);
            setActiveRouteGeoJSON(null);
          }}
          onRouteCalculated={setActiveRouteGeoJSON}
          onSimulateUserStep={handleSimulateUserStep}
        />
      )}

      {/* Map Controls (Zoom, Tilt, Time of Day, Orbit, Reset) */}
      <MapControls
        is3DMode={is3DMode}
        onToggle3D={() => setIs3DMode(!is3DMode)}
        mapInstance={mapInstanceRef}
        userLocation={userLocation}
        onLocateUser={handleLocateUser}
        lightingTheme={lightingTheme}
        onCycleLighting={handleCycleLighting}
        isDroneOrbiting={isDroneOrbiting}
        onToggleDroneOrbit={() => setIsDroneOrbiting(!isDroneOrbiting)}
        showTrees={showTrees}
        onToggleTrees={() => setShowTrees(!showTrees)}
        showPOIs={showPOIs}
        onTogglePOIs={() => setShowPOIs(!showPOIs)}
        showWalkways={showWalkways}
        onToggleWalkways={() => setShowWalkways(!showWalkways)}
      />

      {/* Bottom Live Campus Telemetry Pill */}
      <footer className="absolute bottom-6 left-4 z-20 pointer-events-none hidden sm:flex items-center gap-2">
        <div className="px-3.5 py-1.5 rounded-full bg-slate-900/90 backdrop-blur-xl border border-slate-800 text-[11px] text-slate-300 flex items-center gap-2.5 shadow-card-dark">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <span className="font-semibold text-white">SJEC 25-Acre Verified Campus Bound</span>
          <span className="text-slate-600">•</span>
          <span className="text-cyan-400 font-mono">19 Verified Blocks</span>
          <span className="text-slate-600">•</span>
          <span className="text-emerald-400">Main Stadium Active</span>
        </div>
      </footer>
    </div>
  );
}
