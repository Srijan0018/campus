import React, { useState, useEffect } from 'react';
import {
  X,
  Navigation,
  Footprints,
  Clock,
  ArrowRight,
  RotateCcw,
  Play,
  Pause,
  MapPin,
  CheckCircle,
  CornerDownRight
} from 'lucide-react';
import { NAV_NODES, calculateShortestPath, getEntranceNodeForBuilding, createRouteGeoJSON } from '../data/navigationNetwork.js';
import { buildingsById } from '../data/sjecBuildings.js';

export default function NavigationPanel({
  initialDestinationId,
  userLocation,
  onClose,
  onRouteCalculated,
  onSimulateUserStep
}) {
  const [startNodeId, setStartNodeId] = useState("node-gate1"); // Default: Main Gate 1
  const [destNodeId, setDestNodeId] = useState(() => {
    if (initialDestinationId) {
      return getEntranceNodeForBuilding(initialDestinationId) || "node-ab2-front";
    }
    return "node-ab2-front"; // Default to Academic Block II (Kalam Auditorium / CCC)
  });

  const [routeResult, setRouteResult] = useState(null);
  const [isSimulating, setIsSimulating] = useState(false);
  const [simulationStep, setSimulationStep] = useState(0);

  // Re-calculate route when start or destination changes
  useEffect(() => {
    if (startNodeId && destNodeId) {
      const res = calculateShortestPath(startNodeId, destNodeId);
      setRouteResult(res);
      if (res) {
        onRouteCalculated(createRouteGeoJSON(res.path));
      } else {
        onRouteCalculated(null);
      }
    }
  }, [startNodeId, destNodeId]);

  // Sync if initialDestinationId changes
  useEffect(() => {
    if (initialDestinationId) {
      const node = getEntranceNodeForBuilding(initialDestinationId);
      if (node) {
        setDestNodeId(node);
      }
    }
  }, [initialDestinationId]);

  // Simulation runner
  useEffect(() => {
    let interval = null;
    if (isSimulating && routeResult && routeResult.path.length > 0) {
      interval = setInterval(() => {
        setSimulationStep(prev => {
          const next = prev + 1;
          if (next >= routeResult.path.length) {
            setIsSimulating(false);
            return prev;
          }
          if (onSimulateUserStep) {
            onSimulateUserStep(routeResult.path[next]);
          }
          return next;
        });
      }, 1200);
    }
    return () => clearInterval(interval);
  }, [isSimulating, routeResult, simulationStep]);

  const handleStartSimulation = () => {
    if (!routeResult) return;
    setSimulationStep(0);
    setIsSimulating(true);
    if (onSimulateUserStep) {
      onSimulateUserStep(routeResult.path[0]);
    }
  };

  const handlePauseSimulation = () => {
    setIsSimulating(false);
  };

  const handleResetSimulation = () => {
    setIsSimulating(false);
    setSimulationStep(0);
    if (onSimulateUserStep && routeResult) {
      onSimulateUserStep(routeResult.path[0]);
    }
  };

  // Navigable destinations (buildings that have entrance nodes)
  const availableDestinations = Object.values(NAV_NODES).filter(n => n.type === 'entrance');

  return (
    <div className="absolute top-20 left-4 w-96 max-w-[calc(100vw-32px)] max-h-[calc(100vh-100px)] z-40 bg-slate-900/90 backdrop-blur-xl border border-slate-700/80 rounded-2xl shadow-card-dark flex flex-col overflow-hidden animate-in fade-in slide-in-from-left-4">
      {/* Header */}
      <div className="p-4 border-b border-slate-800/80 bg-gradient-to-b from-slate-800/40 to-transparent flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="p-2 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
            <Footprints className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-bold text-white text-base">Campus Walking Guide</h3>
            <p className="text-[11px] text-slate-400">Paved pedestrian walkway navigation</p>
          </div>
        </div>
        <button
          onClick={onClose}
          className="p-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors border border-slate-700/50"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Selectors */}
      <div className="p-4 border-b border-slate-800/80 space-y-3 bg-slate-950/40">
        {/* Origin */}
        <div>
          <label className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1 block">
            Start Location
          </label>
          <div className="relative">
            <MapPin className="w-3.5 h-3.5 text-emerald-400 absolute left-3 top-3 pointer-events-none" />
            <select
              value={startNodeId}
              onChange={(e) => setStartNodeId(e.target.value)}
              className="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-800/80 border border-slate-700/60 text-xs text-white focus:outline-none focus:border-cyan-500"
            >
              {availableDestinations.map(node => (
                <option key={node.id} value={node.id}>
                  {node.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Destination */}
        <div>
          <label className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-1 block">
            Destination
          </label>
          <div className="relative">
            <Navigation className="w-3.5 h-3.5 text-cyan-400 absolute left-3 top-3 pointer-events-none fill-current" />
            <select
              value={destNodeId}
              onChange={(e) => setDestNodeId(e.target.value)}
              className="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-800/80 border border-slate-700/60 text-xs text-white focus:outline-none focus:border-cyan-500"
            >
              {availableDestinations.map(node => (
                <option key={node.id} value={node.id}>
                  {node.name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Route Metrics Summary */}
      {routeResult && (
        <div className="p-4 border-b border-slate-800/80 bg-cyan-950/20 grid grid-cols-3 gap-2 text-center">
          <div className="p-2.5 rounded-xl bg-slate-800/40 border border-slate-700/30">
            <div className="text-[11px] text-slate-400 flex items-center justify-center gap-1 mb-1">
              <Footprints className="w-3 h-3 text-cyan-400" />
              Distance
            </div>
            <div className="text-sm font-bold text-white">
              {routeResult.totalDistanceMeters}m
            </div>
          </div>
          <div className="p-2.5 rounded-xl bg-slate-800/40 border border-slate-700/30">
            <div className="text-[11px] text-slate-400 flex items-center justify-center gap-1 mb-1">
              <Clock className="w-3 h-3 text-sky-400" />
              Est. Time
            </div>
            <div className="text-sm font-bold text-white">
              {routeResult.walkingTimeMinutes} min
            </div>
          </div>
          <div className="p-2.5 rounded-xl bg-slate-800/40 border border-slate-700/30">
            <div className="text-[11px] text-slate-400 flex items-center justify-center gap-1 mb-1">
              <CheckCircle className="w-3 h-3 text-emerald-400" />
              Surface
            </div>
            <div className="text-[11px] font-semibold text-emerald-400 mt-0.5">
              Paved
            </div>
          </div>
        </div>
      )}

      {/* Turn-by-Turn Directions List */}
      <div className="p-4 space-y-2 overflow-y-auto max-h-[calc(100vh-380px)] text-xs">
        <h4 className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-2">
          Turn-by-Turn Guidance
        </h4>
        {routeResult && routeResult.directions.map((dir, idx) => (
          <div
            key={idx}
            className={`p-2.5 rounded-xl border text-xs flex items-start gap-2.5 transition-colors ${
              idx === simulationStep
                ? 'bg-cyan-500/15 border-cyan-500/50 text-cyan-200'
                : 'bg-slate-800/40 border-slate-700/30 text-slate-300'
            }`}
          >
            <div className={`w-5 h-5 rounded-full flex items-center justify-center shrink-0 mt-0.5 text-[10px] font-bold ${
              idx === simulationStep
                ? 'bg-cyan-400 text-slate-950 font-bold'
                : 'bg-slate-700 text-slate-300'
            }`}>
              {idx + 1}
            </div>
            <div className="leading-relaxed">
              {dir}
            </div>
          </div>
        ))}
      </div>

      {/* Simulation Controls Footer */}
      <div className="p-3 border-t border-slate-800/80 bg-slate-900/95 flex items-center gap-2">
        {!isSimulating ? (
          <button
            onClick={handleStartSimulation}
            className="flex-1 py-2 px-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-slate-950 font-semibold text-xs flex items-center justify-center gap-1.5 shadow-glow-emerald transition-all"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            Simulate Walk
          </button>
        ) : (
          <button
            onClick={handlePauseSimulation}
            className="flex-1 py-2 px-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold text-xs flex items-center justify-center gap-1.5 transition-all"
          >
            <Pause className="w-3.5 h-3.5 fill-current" />
            Pause Walk
          </button>
        )}
        <button
          onClick={handleResetSimulation}
          className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700/50 transition-colors"
          title="Reset Simulation"
        >
          <RotateCcw className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}
