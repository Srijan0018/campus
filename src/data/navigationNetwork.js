/**
 * St Joseph Engineering College (SJEC), Vamanjoor
 * Pedestrian Walkway Navigation Network & Route Finder
 *
 * 100% Topological Network connecting all 20 verified buildings,
 * auditoriums, hostels, amenities, and sports complexes.
 */

export const NAV_NODES = {
  "node-highway-gate": {
    "id": "node-highway-gate",
    "name": "Main Entrance Gate (NH 169)",
    "coord": [
      74.897418,
      12.910577
    ],
    "type": "entrance",
    "buildingId": "bldg-main-gate"
  },
  "node-parking": {
    "id": "node-parking",
    "name": "Main Visitor Parking Lot",
    "coord": [
      74.897607,
      12.910583
    ],
    "type": "waypoint",
    "buildingId": "ground-parking-main"
  },
  "node-roundabout": {
    "id": "node-roundabout",
    "name": "SJEC Central Roundabout",
    "coord": [
      74.8981,
      12.91136
    ],
    "type": "waypoint",
    "buildingId": "ground-roundabout-island"
  },
  "node-mech-workshop": {
    "id": "node-mech-workshop",
    "name": "Central Mechanical Workshop (Green Bay)",
    "coord": [
      74.898353,
      12.910653
    ],
    "type": "entrance",
    "buildingId": "bldg-mech-workshop"
  },
  "node-admin": {
    "id": "node-admin",
    "name": "Administrative Block (Principal & Directorate)",
    "coord": [
      74.898694,
      12.910723
    ],
    "type": "entrance",
    "buildingId": "bldg-admin"
  },
  "node-ab1": {
    "id": "node-ab1",
    "name": "Academic Block I Entrance (Fr Fred Hall / EEE)",
    "coord": [
      74.898513,
      12.9102
    ],
    "type": "entrance",
    "buildingId": "bldg-ab1"
  },
  "node-student-square": {
    "id": "node-student-square",
    "name": "Student Square & Mary's Garden",
    "coord": [
      74.898955,
      12.9107
    ],
    "type": "waypoint",
    "buildingId": "ground-student-square"
  },
  "node-basketball": {
    "id": "node-basketball",
    "name": "Synthetic Basketball Hardcourt",
    "coord": [
      74.898981,
      12.910442
    ],
    "type": "entrance",
    "buildingId": "ground-basketball-court"
  },
  "node-ab2": {
    "id": "node-ab2",
    "name": "Academic Block II Entrance (Kalam Auditorium / CCC / Library)",
    "coord": [
      74.899322,
      12.910799
    ],
    "type": "entrance",
    "buildingId": "bldg-ab2"
  },
  "node-ab3": {
    "id": "node-ab3",
    "name": "Academic Block III Entrance (Spoorthi Hall / AI&DS)",
    "coord": [
      74.89952,
      12.910363
    ],
    "type": "entrance",
    "buildingId": "bldg-ab3"
  },
  "node-ab4": {
    "id": "node-ab4",
    "name": "Academic Block IV (Department of Civil Engineering)",
    "coord": [
      74.899621,
      12.910861
    ],
    "type": "entrance",
    "buildingId": "bldg-ab4"
  },
  "node-mech-complex": {
    "id": "node-mech-complex",
    "name": "Mechanical Department & Faculty Complex",
    "coord": [
      74.900192,
      12.910823
    ],
    "type": "entrance",
    "buildingId": "bldg-mech-complex"
  },
  "node-chapel": {
    "id": "node-chapel",
    "name": "Saint Pio Chapel",
    "coord": [
      74.899132,
      12.911096
    ],
    "type": "entrance",
    "buildingId": "bldg-chapel"
  },
  "node-josarena": {
    "id": "node-josarena",
    "name": "Josarena Open-Air Amphitheatre",
    "coord": [
      74.899356,
      12.911357
    ],
    "type": "entrance",
    "buildingId": "ground-josarena-amphi"
  },
  "node-canteen": {
    "id": "node-canteen",
    "name": "Central Canteen & Food Court (The Lassi Corner)",
    "coord": [
      74.899913,
      12.910627
    ],
    "type": "entrance",
    "buildingId": "bldg-canteen"
  },
  "node-bethania": {
    "id": "node-bethania",
    "name": "Bethania House & Guest House",
    "coord": [
      74.898984,
      12.911506
    ],
    "type": "entrance",
    "buildingId": "bldg-bethania"
  },
  "node-volleyball": {
    "id": "node-volleyball",
    "name": "SJEC Volleyball Clay Court",
    "coord": [
      74.899647,
      12.910018
    ],
    "type": "entrance",
    "buildingId": "ground-volleyball-court"
  },
  "node-girls-hostel": {
    "id": "node-girls-hostel",
    "name": "Saint Joseph Girls Hostel",
    "coord": [
      74.899554,
      12.909317
    ],
    "type": "entrance",
    "buildingId": "bldg-girls-hostel"
  },
  "node-gents-hostel": {
    "id": "node-gents-hostel",
    "name": "Saint Joseph Gents Hostel",
    "coord": [
      74.900562,
      12.91153
    ],
    "type": "entrance",
    "buildingId": "bldg-gents-hostel"
  },
  "node-stadium": {
    "id": "node-stadium",
    "name": "Saint Joseph College Ground (Main Stadium)",
    "coord": [
      74.900765,
      12.909653
    ],
    "type": "entrance",
    "buildingId": "ground-main-stadium-track"
  }
};

export const NAV_EDGES = [
  {
    "from": "node-highway-gate",
    "to": "node-parking",
    "distance": 20.5,
    "name": "Main Entrance Boulevard (Dual Paved Lane)",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-parking",
    "to": "node-roundabout",
    "distance": 101.6,
    "name": "Entrance Avenue towards Central Roundabout",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-roundabout",
    "to": "node-admin",
    "distance": 95.7,
    "name": "South Boulevard to Administrative Portico",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-roundabout",
    "to": "node-chapel",
    "distance": 115.6,
    "name": "Chapel Prayer Walkway",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-roundabout",
    "to": "node-bethania",
    "distance": 97.2,
    "name": "North Promenade to Bethania House",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-admin",
    "to": "node-mech-workshop",
    "distance": 37.8,
    "name": "West Workshop Corridor",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-admin",
    "to": "node-ab1",
    "distance": 61.4,
    "name": "Administrative South Walkway to AB 1",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-admin",
    "to": "node-student-square",
    "distance": 28.4,
    "name": "Central Tree-Lined Pedestrian Mall",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-ab1",
    "to": "node-basketball",
    "distance": 57.4,
    "name": "Student Quadrangle to Basketball Court",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-student-square",
    "to": "node-basketball",
    "distance": 28.8,
    "name": "South Promenade to Basketball Court",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-student-square",
    "to": "node-ab2",
    "distance": 41.3,
    "name": "Academic Link Corridor to AB 2",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-student-square",
    "to": "node-chapel",
    "distance": 48.0,
    "name": "North Chapel Garden Walk",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-ab2",
    "to": "node-ab3",
    "distance": 53.0,
    "name": "Covered Academic Walkway between AB 2 & AB 3",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-ab2",
    "to": "node-ab4",
    "distance": 33.1,
    "name": "Northeast Link to Civil Engineering (AB 4)",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-ab2",
    "to": "node-canteen",
    "distance": 66.8,
    "name": "Central Canteen Promenade",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-ab3",
    "to": "node-volleyball",
    "distance": 40.8,
    "name": "Southern Steps to Volleyball Court",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-ab3",
    "to": "node-canteen",
    "distance": 51.7,
    "name": "East Walkway to Canteen",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-ab4",
    "to": "node-mech-complex",
    "distance": 62.0,
    "name": "Engineering Quad Walkway to Mech Complex",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-ab4",
    "to": "node-josarena",
    "distance": 62.2,
    "name": "North Footpath to Josarena Amphitheatre",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-chapel",
    "to": "node-josarena",
    "distance": 37.8,
    "name": "Amphitheatre Garden Promenade",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-josarena",
    "to": "node-gents-hostel",
    "distance": 132.1,
    "name": "Uphill Paved Drive to Gents Hostel",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-canteen",
    "to": "node-gents-hostel",
    "distance": 122.6,
    "name": "Northeast Residential Road to Gents Hostel",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-canteen",
    "to": "node-stadium",
    "distance": 142.3,
    "name": "Stadium East Access Walkway",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-volleyball",
    "to": "node-girls-hostel",
    "distance": 78.6,
    "name": "South Residential Path to Girls Hostel",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-volleyball",
    "to": "node-stadium",
    "distance": 127.8,
    "name": "Athletic Field West Entry",
    "surface": "paved_walkway",
    "accessible": true
  },
  {
    "from": "node-girls-hostel",
    "to": "node-stadium",
    "distance": 136.5,
    "name": "Stadium Perimeter Track Road",
    "surface": "paved_walkway",
    "accessible": true
  }
];

// Adjacency graph for Dijkstra Shortest Path calculation
export const ADJACENCY_GRAPH = Object.keys(NAV_NODES).reduce((graph, nodeId) => {
  graph[nodeId] = [];
  return graph;
}, {});

NAV_EDGES.forEach(edge => {
  ADJACENCY_GRAPH[edge.from].push({
    node: edge.to,
    weight: edge.distance,
    name: edge.name,
    surface: edge.surface
  });
  ADJACENCY_GRAPH[edge.to].push({
    node: edge.from,
    weight: edge.distance,
    name: edge.name,
    surface: edge.surface
  });
});

export function findShortestPath(startNodeId, endNodeId) {
  if (!NAV_NODES[startNodeId] || !NAV_NODES[endNodeId]) return null;
  if (startNodeId === endNodeId) {
    return {
      path: [startNodeId],
      totalDistance: 0,
      estimatedMinutes: 0,
      coordinates: [NAV_NODES[startNodeId].coord],
      directions: []
    };
  }

  const distances = {};
  const previous = {};
  const edgeUsed = {};
  const unvisited = new Set(Object.keys(NAV_NODES));

  Object.keys(NAV_NODES).forEach(nodeId => {
    distances[nodeId] = Infinity;
    previous[nodeId] = null;
  });
  distances[startNodeId] = 0;

  while (unvisited.size > 0) {
    let closestNode = null;
    let shortestDist = Infinity;
    for (const nodeId of unvisited) {
      if (distances[nodeId] < shortestDist) {
        shortestDist = distances[nodeId];
        closestNode = nodeId;
      }
    }

    if (!closestNode || distances[closestNode] === Infinity) break;
    if (closestNode === endNodeId) break;

    unvisited.delete(closestNode);

    for (const neighbor of ADJACENCY_GRAPH[closestNode]) {
      if (!unvisited.has(neighbor.node)) continue;
      const alt = distances[closestNode] + neighbor.weight;
      if (alt < distances[neighbor.node]) {
        distances[neighbor.node] = alt;
        previous[neighbor.node] = closestNode;
        edgeUsed[neighbor.node] = neighbor;
      }
    }
  }

  if (distances[endNodeId] === Infinity) return null;

  const path = [];
  const coordinates = [];
  const directions = [];
  let curr = endNodeId;

  while (curr) {
    path.unshift(curr);
    coordinates.unshift(NAV_NODES[curr].coord);
    curr = previous[curr];
  }

  for (let i = 0; i < path.length - 1; i++) {
    const fromId = path[i];
    const toId = path[i + 1];
    const edge = ADJACENCY_GRAPH[fromId].find(e => e.node === toId);
    directions.push({
      fromName: NAV_NODES[fromId].name,
      toName: NAV_NODES[toId].name,
      pathName: edge ? edge.name : "Walkway",
      segmentDistance: edge ? Math.round(edge.weight) : 0
    });
  }

  const totalDist = Math.round(distances[endNodeId]);
  const estimatedMin = Math.max(1, Math.round(totalDist / 75));

  return {
    path,
    totalDistance: totalDist,
    estimatedMinutes: estimatedMin,
    coordinates,
    directions
  };
}

export function findNearestNavNode(coord) {
  let nearestId = null;
  let minDistance = Infinity;
  for (const [nodeId, data] of Object.entries(NAV_NODES)) {
    const d = Math.hypot(data.coord[0] - coord[0], data.coord[1] - coord[1]);
    if (d < minDistance) {
      minDistance = d;
      nearestId = nodeId;
    }
  }
  return nearestId;
}

export function findNodeForBuilding(buildingId) {
  if (!buildingId) return null;
  // Direct match
  for (const [nodeId, data] of Object.entries(NAV_NODES)) {
    if (data.buildingId === buildingId) return nodeId;
  }
  // Alias / sub-matches
  if (buildingId.includes("ab1")) return "node-ab1";
  if (buildingId.includes("ab2") || buildingId.includes("1537949013")) return "node-ab2";
  if (buildingId.includes("ab3") || buildingId.includes("1537942437")) return "node-ab3";
  if (buildingId.includes("ab4") || buildingId.includes("civil") || buildingId.includes("1537951217")) return "node-ab4";
  if (buildingId.includes("admin") || buildingId.includes("1537952351")) return "node-admin";
  if (buildingId.includes("chapel") || buildingId.includes("1537941341")) return "node-chapel";
  if (buildingId.includes("amphi") || buildingId.includes("josarena") || buildingId.includes("1533207277")) return "node-josarena";
  if (buildingId.includes("canteen") || buildingId.includes("1538919048")) return "node-canteen";
  if (buildingId.includes("gents") || buildingId.includes("1537940526")) return "node-gents-hostel";
  if (buildingId.includes("girls") || buildingId.includes("1537942615")) return "node-girls-hostel";
  if (buildingId.includes("stadium") || buildingId.includes("ground") || buildingId.includes("1537946636")) return "node-stadium";
  if (buildingId.includes("basketball") || buildingId.includes("1537952627")) return "node-basketball";
  if (buildingId.includes("volleyball") || buildingId.includes("1537945385")) return "node-volleyball";
  if (buildingId.includes("square") || buildingId.includes("1538932918")) return "node-student-square";
  if (buildingId.includes("gate") || buildingId.includes("1537948657")) return "node-highway-gate";
  if (buildingId.includes("workshop") || buildingId.includes("1538919037")) return "node-mech-workshop";
  return null;
}


export const calculateShortestPath = findShortestPath;
export const getEntranceNodeForBuilding = findNodeForBuilding;

export function createRouteGeoJSON(nodePathOrResult) {
  if (!nodePathOrResult) return null;
  const path = Array.isArray(nodePathOrResult) ? nodePathOrResult : nodePathOrResult.path;
  if (!path || path.length < 2) return null;

  const coordinates = path.map(id => NAV_NODES[id] ? NAV_NODES[id].coord : null).filter(Boolean);
  if (coordinates.length < 2) return null;

  return {
    type: "FeatureCollection",
    features: [
      {
        type: "Feature",
        properties: {
          name: "Campus Walking Route"
        },
        geometry: {
          type: "LineString",
          coordinates: coordinates
        }
      }
    ]
  };
}


export function getHaversineDistance(p1, p2) {
  const R = 6371000;
  const dLat = (p2[1] - p1[1]) * Math.PI / 180;
  const dLon = (p2[0] - p1[0]) * Math.PI / 180;
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(p1[1] * Math.PI / 180) * Math.cos(p2[1] * Math.PI / 180) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}
