with open('src/data/navigationNetwork.js', 'r') as f:
    content = f.read()

append_code = """

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
"""

if 'export const calculateShortestPath' not in content:
    with open('src/data/navigationNetwork.js', 'a') as f:
        f.write(append_code)
    print('Added calculateShortestPath and createRouteGeoJSON')
else:
    print('Already present')
