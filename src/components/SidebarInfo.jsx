import React, { useState } from 'react';
import {
  X,
  Navigation,
  Layers,
  Building2,
  CheckCircle2,
  Users,
  MapPin,
  Sparkles,
  Camera,
  ExternalLink
} from 'lucide-react';
import { buildingsById } from '../data/sjecBuildings.js';

export default function SidebarInfo({
  selectedBuildingId,
  onClose,
  onStartNavigation
}) {
  if (!selectedBuildingId) return null;

  const building = buildingsById[selectedBuildingId];
  if (!building) return null;

  const [showPhotoModal, setShowPhotoModal] = useState(false);

  const getCategoryBadge = (cat) => {
    switch (cat) {
      case 'academic':
        return { label: 'Academic & Research', bg: 'bg-blue-500/15 text-blue-400 border-blue-500/30' };
      case 'administrative':
        return { label: 'Administration', bg: 'bg-teal-500/15 text-teal-400 border-teal-500/30' };
      case 'hostel':
        return { label: 'Residential Hostel', bg: 'bg-purple-500/15 text-purple-400 border-purple-500/30' };
      case 'sports':
        return { label: 'Sports & Athletics', bg: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30' };
      case 'amenity':
        return { label: 'Campus Amenity', bg: 'bg-amber-500/15 text-amber-400 border-amber-500/30' };
      case 'landmark':
        return { label: 'Campus Landmark', bg: 'bg-rose-500/15 text-rose-400 border-rose-500/30' };
      default:
        return { label: 'Campus Facility', bg: 'bg-slate-500/15 text-slate-400 border-slate-500/30' };
    }
  };

  const badge = getCategoryBadge(building.category);

  return (
    <>
      <div className="absolute top-20 right-4 w-96 max-w-[calc(100vw-32px)] max-h-[calc(100vh-100px)] z-40 bg-slate-900/95 backdrop-blur-2xl border border-slate-700/80 rounded-2xl shadow-card-dark flex flex-col overflow-hidden transition-all duration-300 animate-in fade-in slide-in-from-right-4">
        {/* Photo Header (from verified SJEC campus photography) */}
        {building.photo && (
          <div
            onClick={() => setShowPhotoModal(true)}
            className="relative h-44 w-full overflow-hidden bg-slate-950 cursor-pointer group"
            title="Click to view full-resolution authentic photo"
          >
            <img
              src={building.photo}
              alt={building.name}
              className="w-full h-full object-cover opacity-90 group-hover:scale-105 group-hover:opacity-100 transition-all duration-500"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-transparent to-black/40"></div>
            <div className="absolute top-3 left-3 px-2.5 py-1 rounded-lg bg-black/70 backdrop-blur-md text-[10px] text-cyan-300 flex items-center gap-1.5 border border-cyan-500/40 shadow-glow-cyan">
              <Camera className="w-3.5 h-3.5" />
              <span className="font-semibold">Verified Campus Photo</span>
            </div>
            <div className="absolute bottom-2 right-3 px-2 py-0.5 rounded-md bg-black/60 text-[10px] text-slate-300 opacity-0 group-hover:opacity-100 transition-opacity">
              Tap to Expand ↗
            </div>
          </div>
        )}

        {/* Top Header Card */}
        <div className="relative p-5 pb-3 border-b border-slate-800/80 bg-gradient-to-b from-slate-800/40 to-transparent">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 p-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors border border-slate-700/50"
            title="Close details"
          >
            <X className="w-4 h-4" />
          </button>

          <div className="flex items-center gap-2 mb-2">
            <span className={`text-[11px] font-semibold tracking-wider uppercase px-2.5 py-0.5 rounded-full border ${badge.bg}`}>
              {badge.label}
            </span>
            <span className="text-[11px] font-mono text-slate-300 bg-slate-800/90 px-2 py-0.5 rounded-full border border-slate-700/60">
              {building.short_code || building.shortName || 'SJEC'}
            </span>
          </div>

          <h2 className="text-xl font-bold text-white tracking-tight leading-snug">
            {building.name}
          </h2>

          {/* Quick Metrics Bar */}
          <div className="flex items-center gap-3 mt-3 pt-3 border-t border-slate-800/60 text-xs text-slate-300">
            <div className="flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5 text-cyan-400" />
              <span><strong className="text-white font-semibold">{building.levels || building.floors || 4}</strong> Floors</span>
            </div>
            <span className="text-slate-600">•</span>
            <div className="flex items-center gap-1.5">
              <Building2 className="w-3.5 h-3.5 text-sky-400" />
              <span><strong className="text-white font-semibold">{building.height}m</strong> Height</span>
            </div>
            <span className="text-slate-600">•</span>
            <div className="flex items-center gap-1.5">
              <MapPin className="w-3.5 h-3.5 text-emerald-400" />
              <span className="text-emerald-400 font-medium">Verified OSM</span>
            </div>
          </div>
        </div>

        {/* Scrollable Content Body */}
        <div className="p-5 space-y-4 overflow-y-auto max-h-[calc(100vh-340px)] text-sm">
          {/* Summary / Description */}
          <div>
            <p className="text-slate-300 text-xs leading-relaxed">
              {building.summary || building.description}
            </p>
          </div>

        {/* Departments List */}
        {building.departments && building.departments.length > 0 && (
          <div>
            <h4 className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
              <Users className="w-3.5 h-3.5 text-cyan-400" />
              Departments & Units
            </h4>
            <div className="space-y-1.5">
              {building.departments.map((dept, idx) => (
                <div
                  key={idx}
                  className="px-3 py-2 rounded-xl bg-slate-800/60 border border-slate-700/40 text-xs text-slate-200 flex items-start gap-2"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 mt-1.5 shrink-0"></span>
                  <span>{dept}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Key Facilities */}
        {building.facilities && building.facilities.length > 0 && (
          <div>
            <h4 className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              Key Facilities & Halls
            </h4>
            <div className="space-y-1.5">
              {building.facilities.map((fac, idx) => (
                <div
                  key={idx}
                  className="px-3 py-2 rounded-xl bg-slate-800/40 border border-slate-700/30 text-xs text-slate-300 flex items-start gap-2"
                >
                  <Sparkles className="w-3.5 h-3.5 text-amber-400 mt-0.5 shrink-0" />
                  <span>{fac}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Action Footer */}
      <div className="p-4 border-t border-slate-800/80 bg-slate-900/95 flex gap-2.5">
        <button
          onClick={() => onStartNavigation(building.id)}
          className="flex-1 py-2.5 px-4 rounded-xl bg-gradient-to-r from-cyan-500 to-sky-600 hover:from-cyan-400 hover:to-sky-500 text-slate-950 font-bold text-xs flex items-center justify-center gap-2 shadow-glow-cyan transition-all"
        >
          <Navigation className="w-4 h-4 fill-current" />
          Navigate Here (Walkway)
        </button>
      </div>
    </div>

    {/* Fullscreen Photo Lightbox Modal */}
    {showPhotoModal && building.photo && (
      <div
        className="fixed inset-0 z-50 bg-black/85 backdrop-blur-xl flex items-center justify-center p-4 animate-in fade-in duration-200"
        onClick={() => setShowPhotoModal(false)}
      >
        <div className="relative max-w-4xl max-h-[90vh] bg-slate-900 border border-slate-700/80 rounded-2xl overflow-hidden shadow-2xl" onClick={e => e.stopPropagation()}>
          <button
            onClick={() => setShowPhotoModal(false)}
            className="absolute top-4 right-4 z-10 p-2 rounded-full bg-black/60 hover:bg-black/80 text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
          <img
            src={building.photo}
            alt={building.name}
            className="max-h-[75vh] w-auto object-contain mx-auto"
          />
          <div className="p-4 bg-slate-900 border-t border-slate-800 text-left">
            <div className="flex items-center gap-2 mb-1">
              <Camera className="w-4 h-4 text-cyan-400" />
              <span className="text-xs font-semibold text-cyan-300">Verified SJEC Campus Photography</span>
            </div>
            <h3 className="text-base font-bold text-white">{building.name}</h3>
            <p className="text-xs text-slate-400 mt-1">{building.summary}</p>
          </div>
        </div>
      </div>
    )}
  </>
  );
}
