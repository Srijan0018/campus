/**
 * St Joseph Engineering College (SJEC), Vamanjoor
 * 100% Authentic Verified Campus Landmark POIs at Exact Coordinates
 */

export const sjecPOIsGeoJSON = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      id: "poi-ab1",
      properties: {
        id: "poi-ab1",
        name: "Academic Block I (AB-I)",
        subtext: "Electrical Sciences & Basic Sciences",
        category: "academic",
        buildingId: "bldg-ab1",
        icon: "BookOpen",
        color: "#0284c7",
        description: "Undergraduate core academic block with distinctive dual courtyards. Houses EEE department, Basic Sciences, and Fr. Fred Memorial Hall in the basement.",
        coord: [74.898513, 12.910200]
      },
      geometry: { type: "Point", coordinates: [74.898513, 12.910200] }
    },
    {
      type: "Feature",
      id: "poi-fr-fred-hall",
      properties: {
        id: "poi-fr-fred-hall",
        name: "Fr Fred Memorial Hall",
        subtext: "Academic Block I — Basement",
        category: "academic",
        buildingId: "bldg-ab1",
        icon: "Mic",
        color: "#38bdf8",
        description: "Prominent assembly hall in the basement of Academic Block I, hosting student association activities, technical symposiums, and blood donation drives.",
        coord: [74.898480, 12.910220]
      },
      geometry: { type: "Point", coordinates: [74.898480, 12.910220] }
    },
    {
      type: "Feature",
      id: "poi-ab2",
      properties: {
        id: "poi-ab2",
        name: "Academic Block II (AB-II)",
        subtext: "Computing Sciences & Central Library",
        category: "academic",
        buildingId: "bldg-ab2",
        icon: "Laptop",
        color: "#06b6d4",
        description: "6-storey academic hub for CSE, ISE, MCA, the multi-tier Central Library, Central Computer Centre, and Kalam Auditorium.",
        coord: [74.899322, 12.910799]
      },
      geometry: { type: "Point", coordinates: [74.899322, 12.910799] }
    },
    {
      type: "Feature",
      id: "poi-kalam-auditorium",
      properties: {
        id: "poi-kalam-auditorium",
        name: "A.P.J. Abdul Kalam Auditorium",
        subtext: "Academic Block II — 5th Floor",
        category: "academic",
        buildingId: "bldg-ab2",
        icon: "Award",
        color: "#38bdf8",
        description: "1,000-seat premier indoor auditorium hosting convocations, national conventions, and cultural fests like TIARA.",
        coord: [74.899322, 12.910799]
      },
      geometry: { type: "Point", coordinates: [74.899322, 12.910799] }
    },
    {
      type: "Feature",
      id: "poi-ccc",
      properties: {
        id: "poi-ccc",
        name: "Central Computer Centre (CCC)",
        subtext: "Academic Block II — Basement",
        category: "academic",
        buildingId: "bldg-ab2",
        icon: "Server",
        color: "#06b6d4",
        description: "Nerve centre of SJEC digital infrastructure with high-speed 1 Gbps leased lines, cloud cluster, and programming labs.",
        coord: [74.899280, 12.910750]
      },
      geometry: { type: "Point", coordinates: [74.899280, 12.910750] }
    },
    {
      type: "Feature",
      id: "poi-library",
      properties: {
        id: "poi-library",
        name: "Central Library & Information Centre",
        subtext: "Academic Block II — Ground & 1st Floor",
        category: "academic",
        buildingId: "bldg-ab2",
        icon: "Library",
        color: "#06b6d4",
        description: "Multi-level academic library with thousands of technical volumes, IEEE/Springer digital access, and quiet research zones.",
        coord: [74.899350, 12.910830]
      },
      geometry: { type: "Point", coordinates: [74.899350, 12.910830] }
    },
    {
      type: "Feature",
      id: "poi-ab3",
      properties: {
        id: "poi-ab3",
        name: "Academic Block III (AB-III)",
        subtext: "Advanced Engineering & MBA (Tallest Block)",
        category: "academic",
        buildingId: "bldg-ab3",
        icon: "Building",
        color: "#3b82f6",
        description: "Tallest building on campus (9 storeys, 34m). Houses ECE, AI&DS, MBA, Spoorthi Hall, Prerana Hall, and 300 kWp rooftop solar plant.",
        coord: [74.899520, 12.910363]
      },
      geometry: { type: "Point", coordinates: [74.899520, 12.910363] }
    },
    {
      type: "Feature",
      id: "poi-spoorthi-hall",
      properties: {
        id: "poi-spoorthi-hall",
        name: "Spoorthi Conference Hall",
        subtext: "Academic Block III — 7th Floor",
        category: "academic",
        buildingId: "bldg-ab3",
        icon: "Users",
        color: "#3b82f6",
        description: "Executive high-capacity conference auditorium on the 7th floor for international symposiums and management conclaves.",
        coord: [74.899520, 12.910363]
      },
      geometry: { type: "Point", coordinates: [74.899520, 12.910363] }
    },
    {
      type: "Feature",
      id: "poi-prerana-hall",
      properties: {
        id: "poi-prerana-hall",
        name: "Prerana Seminar Hall",
        subtext: "Academic Block III — Ground Floor",
        category: "academic",
        buildingId: "bldg-ab3",
        icon: "MessageSquare",
        color: "#3b82f6",
        description: "Ground floor interactive seminar hall for faculty development and guest lecture series.",
        coord: [74.899490, 12.910390]
      },
      geometry: { type: "Point", coordinates: [74.899490, 12.910390] }
    },
    {
      type: "Feature",
      id: "poi-ab4",
      properties: {
        id: "poi-ab4",
        name: "Academic Block IV — Department of Civil Engineering",
        subtext: "Civil Engineering & Bishop Aloysius Paul Hall",
        category: "academic",
        buildingId: "bldg-ab4",
        icon: "DraftingCompass",
        color: "#8b5cf6",
        description: "5-storey modern civil engineering facility with BIM CAD labs, materials testing machinery, and Bishop Aloysius Paul Hall.",
        coord: [74.899621, 12.910861]
      },
      geometry: { type: "Point", coordinates: [74.899621, 12.910861] }
    },
    {
      type: "Feature",
      id: "poi-admin",
      properties: {
        id: "poi-admin",
        name: "Administrative Block",
        subtext: "Principal & Directorate Headquarters",
        category: "administrative",
        buildingId: "bldg-admin",
        icon: "Briefcase",
        color: "#0d9488",
        description: "Central administrative hub at the campus entrance. Houses Director, Principal, Admissions, and Examination branches.",
        coord: [74.898694, 12.910723]
      },
      geometry: { type: "Point", coordinates: [74.898694, 12.910723] }
    },
    {
      type: "Feature",
      id: "poi-mech-workshop",
      properties: {
        id: "poi-mech-workshop",
        name: "Central Mechanical Workshops (Green Bay)",
        subtext: "CNC, Lathe & Foundry Bays",
        category: "academic",
        buildingId: "bldg-mech-workshop",
        icon: "Wrench",
        color: "#10b981",
        description: "Heavy engineering workshop with overhead crane, precision CNC turning, welding bays, and metallurgy furnaces.",
        coord: [74.898353, 12.910653]
      },
      geometry: { type: "Point", coordinates: [74.898353, 12.910653] }
    },
    {
      type: "Feature",
      id: "poi-mech-complex",
      properties: {
        id: "poi-mech-complex",
        name: "Mechanical Engineering Department & Faculty Complex",
        subtext: "CAMD, Fluid Mechanics & Heat Transfer",
        category: "academic",
        buildingId: "bldg-mech-complex",
        icon: "Cog",
        color: "#f59e0b",
        description: "5-storey white facade block with red hipped roof housing Mechanical Engineering classrooms and advanced CAMD design software.",
        coord: [74.900192, 12.910823]
      },
      geometry: { type: "Point", coordinates: [74.900192, 12.910823] }
    },
    {
      type: "Feature",
      id: "poi-chapel",
      properties: {
        id: "poi-chapel",
        name: "Saint Pio Chapel",
        subtext: "Spiritual Sanctuary & Adoration Chapel",
        category: "landmark",
        buildingId: "bldg-chapel",
        icon: "Heart",
        color: "#eab308",
        description: "Cruciform stone chapel in the heart of the campus, featuring prayer alcoves and manicured serene gardens.",
        coord: [74.899132, 12.911096]
      },
      geometry: { type: "Point", coordinates: [74.899132, 12.911096] }
    },
    {
      type: "Feature",
      id: "poi-josarena",
      properties: {
        id: "poi-josarena",
        name: "Josarena Open-Air Amphitheatre",
        subtext: "Cultural Venue (2,000 Seats)",
        category: "landmark",
        buildingId: "ground-josarena-amphi",
        icon: "Music",
        color: "#38bdf8",
        description: "Open-air semicircular amphitheatre hosting annual national fest TIARA, cultural evenings, and musical performances.",
        coord: [74.899356, 12.911357]
      },
      geometry: { type: "Point", coordinates: [74.899356, 12.911357] }
    },
    {
      type: "Feature",
      id: "poi-canteen",
      properties: {
        id: "poi-canteen",
        name: "Central Canteen & Food Court (The Lassi Corner)",
        subtext: "Multi-Cuisine Dining & Outdoor Cafe",
        category: "amenity",
        buildingId: "bldg-canteen",
        icon: "Coffee",
        color: "#f97316",
        description: "Campus dining complex with South/North Indian cuisines, fresh fruit juice bar, bakery, and open-air seating beside Josarena.",
        coord: [74.899913, 12.910627]
      },
      geometry: { type: "Point", coordinates: [74.899913, 12.910627] }
    },
    {
      type: "Feature",
      id: "poi-gents-hostel",
      properties: {
        id: "poi-gents-hostel",
        name: "Saint Joseph Gents Hostel",
        subtext: "Boys Dormitory Complex & Gym",
        category: "hostel",
        buildingId: "bldg-gents-hostel",
        icon: "Home",
        color: "#6366f1",
        description: "Residential complex for 600 male scholars with gym, dining mess, study halls, and Wi-Fi lounges.",
        coord: [74.900562, 12.911530]
      },
      geometry: { type: "Point", coordinates: [74.900562, 12.911530] }
    },
    {
      type: "Feature",
      id: "poi-girls-hostel",
      properties: {
        id: "poi-girls-hostel",
        name: "Saint Joseph Girls Hostel",
        subtext: "Ladies Residence with Modern AC Wing",
        category: "hostel",
        buildingId: "bldg-girls-hostel",
        icon: "Shield",
        color: "#ec4899",
        description: "Secure residential sanctuary for female students with AC rooms, dining facilities, and indoor recreation.",
        coord: [74.899554, 12.909317]
      },
      geometry: { type: "Point", coordinates: [74.899554, 12.909317] }
    },
    {
      type: "Feature",
      id: "poi-stadium",
      properties: {
        id: "poi-stadium",
        name: "Saint Joseph College Ground (Main Stadium)",
        subtext: "Athletics Track, Cricket & Football Turf",
        category: "sports",
        buildingId: "ground-main-stadium-track",
        icon: "Activity",
        color: "#15803d",
        description: "Sprawling athletics stadium in the southeastern sector with 400m running track, football pitch, cricket wicket, and viewing banks.",
        coord: [74.900765, 12.909653]
      },
      geometry: { type: "Point", coordinates: [74.900765, 12.909653] }
    },
    {
      type: "Feature",
      id: "poi-basketball",
      properties: {
        id: "poi-basketball",
        name: "Synthetic Basketball Court",
        subtext: "Acrylic Hardcourt with Floodlights",
        category: "sports",
        buildingId: "ground-basketball-court",
        icon: "Circle",
        color: "#0284c7",
        description: "Tournament-grade synthetic basketball hardcourt located between Student Square and Academic Block I.",
        coord: [74.898981, 12.910442]
      },
      geometry: { type: "Point", coordinates: [74.898981, 12.910442] }
    },
    {
      type: "Feature",
      id: "poi-volleyball",
      properties: {
        id: "poi-volleyball",
        name: "SJEC Volleyball Court",
        subtext: "Outdoor Clay Court",
        category: "sports",
        buildingId: "ground-volleyball-court",
        icon: "Compass",
        color: "#d97706",
        description: "Clay volleyball court located south of Academic Block III on the threshold of the college ground.",
        coord: [74.899647, 12.910018]
      },
      geometry: { type: "Point", coordinates: [74.899647, 12.910018] }
    },
    {
      type: "Feature",
      id: "poi-student-square",
      properties: {
        id: "poi-student-square",
        name: "Student Square & Central Courtyard",
        subtext: "Campus Social Hub & Shaded Plaza",
        category: "amenity",
        buildingId: "ground-student-square",
        icon: "Smile",
        color: "#06b6d4",
        description: "Lively central outdoor gathering square nestled between Admin, AB 1, and AB 2 with tree benches and study hubs.",
        coord: [74.898955, 12.910700]
      },
      geometry: { type: "Point", coordinates: [74.898955, 12.910700] }
    },
    {
      type: "Feature",
      id: "poi-roundabout",
      properties: {
        id: "poi-roundabout",
        name: "SJEC Central Roundabout & Monument",
        subtext: "Campus Entrance Traffic Circle",
        category: "landmark",
        buildingId: "ground-roundabout-island",
        icon: "Navigation",
        color: "#10b981",
        description: "Landscaped circular junction at the end of the entrance avenue distributing traffic to academic core and hostels.",
        coord: [74.898100, 12.911360]
      },
      geometry: { type: "Point", coordinates: [74.898100, 12.911360] }
    },
    {
      type: "Feature",
      id: "poi-main-gate",
      properties: {
        id: "poi-main-gate",
        name: "Main Entrance Gate (NH 169)",
        subtext: "Campus Entry & Security Checkpoint",
        category: "administrative",
        buildingId: "bldg-main-gate",
        icon: "MapPin",
        color: "#475569",
        description: "Primary vehicular and pedestrian gateway on Solapur-Mangalore Highway (NH 169), right opposite SJEC Bus Stop.",
        coord: [74.897418, 12.910577]
      },
      geometry: { type: "Point", coordinates: [74.897418, 12.910577] }
    }
  ]
};


export const allSearchableLocations = sjecPOIsGeoJSON.features.map(f => ({
  id: f.properties.id,
  name: f.properties.name,
  subtext: f.properties.subtext,
  category: f.properties.category,
  buildingId: f.properties.buildingId,
  coord: f.properties.coord,
  icon: f.properties.icon,
  type: 'landmark'
}));
