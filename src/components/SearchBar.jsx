import React, { useState, useRef, useEffect } from 'react';
import {
  Search,
  X,
  Building,
  Home,
  Trophy,
  Coffee,
  Landmark,
  Compass,
  MapPin
} from 'lucide-react';
import { allSearchableLocations } from '../data/sjecPOIs.js';
import { sjecBuildingsGeoJSON } from '../data/sjecBuildings.js';

export default function SearchBar({
  onSelectResult,
  activeCategory,
  onCategoryChange
}) {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef(null);

  // Combine buildings and POIs into searchable array
  const allLocations = [
    ...sjecBuildingsGeoJSON.features.map(f => {
      const p = f.properties;
      const code = p.short_code || p.shortName || '';
      const lvls = p.levels || p.floors || '';
      const sub = `${code ? code + ' • ' : ''}${lvls ? lvls + ' Floors • ' : ''}${p.height}m`;
      let centroid = p.entranceCoord;
      if (!centroid && f.geometry?.coordinates) {
        const ring = f.geometry.type === 'Polygon' ? f.geometry.coordinates[0] : f.geometry.coordinates[0][0];
        if (ring && ring.length > 0) {
          centroid = [
            ring.reduce((s, c) => s + c[0], 0) / ring.length,
            ring.reduce((s, c) => s + c[1], 0) / ring.length
          ];
        }
      }
      return {
        id: p.id,
        name: p.name,
        subtext: sub,
        category: p.category,
        buildingId: p.id,
        coord: centroid,
        icon: p.icon,
        type: 'building'
      };
    }),
    ...allSearchableLocations
  ];

  // Filter based on query and category
  const filtered = allLocations.filter(loc => {
    const matchesCategory =
      !activeCategory || activeCategory === 'all' || loc.category === activeCategory;
    if (!matchesCategory) return false;

    if (!query.trim()) return true;

    const q = query.toLowerCase();
    const nameMatch = loc.name.toLowerCase().includes(q);
    const subtextMatch = loc.subtext && loc.subtext.toLowerCase().includes(q);
    const idMatch = loc.id.toLowerCase().includes(q);
    return nameMatch || subtextMatch || idMatch;
  });

  // Handle outside click
  useEffect(() => {
    function handleClickOutside(e) {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const categories = [
    { id: 'all', label: 'All Places', icon: Compass },
    { id: 'academic', label: 'Academic', icon: Building },
    { id: 'hostel', label: 'Hostels', icon: Home },
    { id: 'sports', label: 'Sports', icon: Trophy },
    { id: 'amenity', label: 'Dining & ATM', icon: Coffee },
    { id: 'administrative', label: 'Admin', icon: Landmark }
  ];

  const handleSelect = (item) => {
    setQuery(item.name);
    setIsOpen(false);
    onSelectResult(item);
  };

  return (
    <div ref={containerRef} className="relative z-30 w-full max-w-md">
      {/* Search Input Bar */}
      <div className="relative flex items-center">
        <Search className="w-4 h-4 text-slate-400 absolute left-3.5 pointer-events-none" />
        <input
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          placeholder="Search SJEC blocks, auditoriums, labs, hostels..."
          className="w-full pl-10 pr-9 py-2.5 rounded-2xl bg-slate-900/85 backdrop-blur-xl border border-slate-700/80 text-xs text-white placeholder-slate-400 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 shadow-card-dark transition-all"
        />
        {query && (
          <button
            onClick={() => {
              setQuery('');
              setIsOpen(false);
            }}
            className="absolute right-3 p-1 rounded-full text-slate-400 hover:text-white"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        )}
      </div>

      {/* Category Pills Bar */}
      <div className="flex items-center gap-1.5 mt-2 overflow-x-auto pb-1 scrollbar-none">
        {categories.map(cat => {
          const Icon = cat.icon;
          const isActive = (activeCategory || 'all') === cat.id;
          return (
            <button
              key={cat.id}
              onClick={() => onCategoryChange(cat.id)}
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded-xl text-[11px] font-medium whitespace-nowrap transition-all border ${
                isActive
                  ? 'bg-cyan-500/20 text-cyan-300 border-cyan-500/50 shadow-glow-cyan'
                  : 'bg-slate-900/70 backdrop-blur-md text-slate-400 border-slate-800/80 hover:text-slate-200 hover:border-slate-700'
              }`}
            >
              <Icon className="w-3 h-3" />
              {cat.label}
            </button>
          );
        })}
      </div>

      {/* Results Autocomplete Dropdown */}
      {isOpen && (
        <div className="absolute top-full left-0 right-0 mt-2 max-h-72 bg-slate-900/95 backdrop-blur-2xl border border-slate-700/80 rounded-2xl shadow-card-dark overflow-y-auto overflow-x-hidden p-1.5 space-y-1">
          {filtered.length > 0 ? (
            filtered.map(item => (
              <button
                key={item.id}
                onClick={() => handleSelect(item)}
                className="w-full text-left px-3 py-2 rounded-xl hover:bg-slate-800/80 text-xs text-slate-200 flex items-center gap-2.5 transition-colors group"
              >
                <div className="p-1.5 rounded-lg bg-slate-800 group-hover:bg-cyan-500/20 text-slate-400 group-hover:text-cyan-400 transition-colors shrink-0">
                  <MapPin className="w-3.5 h-3.5" />
                </div>
                <div className="flex-1 truncate">
                  <div className="font-semibold text-white group-hover:text-cyan-300 transition-colors truncate">
                    {item.name}
                  </div>
                  {item.subtext && (
                    <div className="text-[10px] text-slate-400 truncate">
                      {item.subtext}
                    </div>
                  )}
                </div>
              </button>
            ))
          ) : (
            <div className="py-6 text-center text-xs text-slate-400">
              No matching campus locations found for "{query}"
            </div>
          )}
        </div>
      )}
    </div>
  );
}
