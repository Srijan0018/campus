import xml.etree.ElementTree as ET
import json
import math

tree = ET.parse('sjec_real_osm.osm')
root = tree.getroot()

nodes = {n.attrib['id']: [float(n.attrib['lon']), float(n.attrib['lat'])] for n in root.findall('node')}
ways = {}
for w in root.findall('way'):
    nd_refs = [nd.attrib['ref'] for nd in w.findall('nd')]
    coords = [nodes[ref] for ref in nd_refs if ref in nodes]
    ways[w.attrib['id']] = coords

def close_ring(ring):
    if ring and ring[0] != ring[-1]:
        ring.append(ring[0])
    return ring

grounds_features = []
details_features = []

# 1. Main College Ground / Stadium (Way 1537946636)
stadium_coords = close_ring(ways['1537946636'])
cx = sum(p[0] for p in stadium_coords[:-1]) / (len(stadium_coords)-1)
cy = sum(p[1] for p in stadium_coords[:-1]) / (len(stadium_coords)-1)

# Outer stadium running track
grounds_features.append({
    'type': 'Feature',
    'id': 'ground-main-stadium-track',
    'properties': {
        'id': 'ground-main-stadium-track',
        'name': 'Saint Joseph College Ground (Athletic Track)',
        'category': 'sports',
        'type': 'running_track',
        'color': '#991b1b', # Terracotta athletic running track
        'opacity': 0.85
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [stadium_coords]
    }
})

# Inner turf field (scaled by ~0.82 towards centroid)
inner_turf_coords = []
for p in stadium_coords:
    nx = cx + (p[0] - cx) * 0.82
    ny = cy + (p[1] - cy) * 0.82
    inner_turf_coords.append([nx, ny])

grounds_features.append({
    'type': 'Feature',
    'id': 'ground-main-stadium-turf',
    'properties': {
        'id': 'ground-main-stadium-turf',
        'name': 'Saint Joseph College Ground (Football & Cricket Pitch)',
        'category': 'sports',
        'type': 'grass_pitch',
        'color': '#15803d', # Vibrant stadium turf
        'opacity': 0.95
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [inner_turf_coords]
    }
})

# Stadium Running Track Lane Lines (Lines)
for scale in [0.95, 0.90, 0.85]:
    lane_coords = [[cx + (p[0] - cx) * scale, cy + (p[1] - cy) * scale] for p in stadium_coords]
    details_features.append({
        'type': 'Feature',
        'properties': {
            'type': 'track_lane',
            'color': '#f8fafc',
            'width': 1.2,
            'dash': [4, 4]
        },
        'geometry': {
            'type': 'LineString',
            'coordinates': lane_coords
        }
    })

# Football field pitch lines on inner turf
# center of field cx, cy
# Field box: width ~ 0.0006 lon, height ~ 0.0005 lat
fw = 0.00045
fh = 0.00035
pitch_box = [
    [cx - fw, cy - fh],
    [cx + fw, cy - fh],
    [cx + fw, cy + fh],
    [cx - fw, cy + fh],
    [cx - fw, cy - fh]
]
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'pitch_marking', 'color': '#ffffff', 'width': 2 },
    'geometry': { 'type': 'LineString', 'coordinates': pitch_box }
})
# Halfway line
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'pitch_marking', 'color': '#ffffff', 'width': 2 },
    'geometry': { 'type': 'LineString', 'coordinates': [[cx - fw, cy], [cx + fw, cy]] }
})
# Center circle
circle_pts = []
for deg in range(0, 361, 15):
    rad = math.radians(deg)
    rx = cx + math.cos(rad) * 0.00008
    ry = cy + math.sin(rad) * 0.00008
    circle_pts.append([rx, ry])
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'pitch_marking', 'color': '#ffffff', 'width': 2 },
    'geometry': { 'type': 'LineString', 'coordinates': circle_pts }
})

# 2. Basketball Court (Way 1537952627)
bb_coords = close_ring(ways['1537952627'])
grounds_features.append({
    'type': 'Feature',
    'id': 'ground-basketball-court',
    'properties': {
        'id': 'ground-basketball-court',
        'name': 'Synthetic Basketball Court',
        'category': 'sports',
        'type': 'court_synthetic',
        'color': '#0284c7', # Vivid Blue acrylic court
        'opacity': 0.95
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [bb_coords]
    }
})
# Basketball court lines
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'court_line', 'color': '#ffffff', 'width': 1.8 },
    'geometry': { 'type': 'LineString', 'coordinates': bb_coords }
})
# Basketball center line & circle
bcx = sum(p[0] for p in bb_coords[:-1]) / (len(bb_coords)-1)
bcy = sum(p[1] for p in bb_coords[:-1]) / (len(bb_coords)-1)
bb_circle = []
for deg in range(0, 361, 20):
    rad = math.radians(deg)
    bb_circle.append([bcx + math.cos(rad) * 0.00003, bcy + math.sin(rad) * 0.00003])
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'court_line', 'color': '#ffffff', 'width': 1.5 },
    'geometry': { 'type': 'LineString', 'coordinates': bb_circle }
})

# 3. Volleyball Court (Way 1537945385)
vb_coords = close_ring(ways['1537945385'])
grounds_features.append({
    'type': 'Feature',
    'id': 'ground-volleyball-court',
    'properties': {
        'id': 'ground-volleyball-court',
        'name': 'SJEC Volleyball Court',
        'category': 'sports',
        'type': 'court_clay',
        'color': '#d97706', # Clay amber court
        'opacity': 0.95
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [vb_coords]
    }
})
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'court_line', 'color': '#fef08a', 'width': 2 },
    'geometry': { 'type': 'LineString', 'coordinates': vb_coords }
})

# 4. Badminton Courts (Ways 1538919065 & 1538919073)
for idx, wid in enumerate(['1538919065', '1538919073']):
    bm_coords = close_ring(ways[wid])
    grounds_features.append({
        'type': 'Feature',
        'id': f'ground-badminton-{idx+1}',
        'properties': {
            'id': f'ground-badminton-{idx+1}',
            'name': f'Outdoor Badminton Court {idx+1}',
            'category': 'sports',
            'type': 'court_synthetic',
            'color': '#059669', # Emerald green
            'opacity': 0.9
        },
        'geometry': {
            'type': 'Polygon',
            'coordinates': [bm_coords]
        }
    })
    details_features.append({
        'type': 'Feature',
        'properties': { 'type': 'court_line', 'color': '#ffffff', 'width': 1.5 },
        'geometry': { 'type': 'LineString', 'coordinates': bm_coords }
    })

# 5. Josarena Amphitheatre (Way 1533207277)
amphi_coords = close_ring(ways['1533207277'])
grounds_features.append({
    'type': 'Feature',
    'id': 'ground-josarena-amphi',
    'properties': {
        'id': 'ground-josarena-amphi',
        'name': 'Josarena Open-Air Amphitheatre',
        'category': 'landmark',
        'type': 'amphitheatre',
        'color': '#334155', # Slate stone steps
        'opacity': 0.95
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [amphi_coords]
    }
})
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'amphi_step', 'color': '#38bdf8', 'width': 2 },
    'geometry': { 'type': 'LineString', 'coordinates': amphi_coords }
})

# 6. Student Square (Way 1538932918)
sq_coords = close_ring(ways['1538932918'])
grounds_features.append({
    'type': 'Feature',
    'id': 'ground-student-square',
    'properties': {
        'id': 'ground-student-square',
        'name': 'Student Square (Central Plaza)',
        'category': 'amenity',
        'type': 'plaza',
        'color': '#1e293b',
        'opacity': 0.95
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [sq_coords]
    }
})

# 7. Mary's Garden (Way 1538919029)
mg_coords = close_ring(ways['1538919029'])
grounds_features.append({
    'type': 'Feature',
    'id': 'ground-marys-garden',
    'properties': {
        'id': 'ground-marys-garden',
        'name': "Mary's Garden",
        'category': 'amenity',
        'type': 'garden',
        'color': '#166534', # Deep green garden lawn
        'opacity': 0.95
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [mg_coords]
    }
})

# 8. Parking Lots (Ways 1537948853 & 1537956248)
pk1_coords = close_ring(ways['1537948853'])
grounds_features.append({
    'type': 'Feature',
    'id': 'ground-parking-main',
    'properties': {
        'id': 'ground-parking-main',
        'name': 'Main Entrance Visitor Parking',
        'category': 'amenity',
        'type': 'parking',
        'color': '#1e293b',
        'opacity': 0.8
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [pk1_coords]
    }
})

pk2_coords = close_ring(ways['1537956248'])
grounds_features.append({
    'type': 'Feature',
    'id': 'ground-parking-stadium',
    'properties': {
        'id': 'ground-parking-stadium',
        'name': 'Stadium North Parking Area',
        'category': 'amenity',
        'type': 'parking',
        'color': '#1e293b',
        'opacity': 0.8
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [pk2_coords]
    }
})

# 9. SJEC Central Roundabout Island
# Centered around (74.8981, 12.91136)
rcx, rcy = 74.89810, 12.91136
roundabout_island = []
for deg in range(0, 361, 15):
    rad = math.radians(deg)
    roundabout_island.append([rcx + math.cos(rad) * 0.00007, rcy + math.sin(rad) * 0.00007])

grounds_features.append({
    'type': 'Feature',
    'id': 'ground-roundabout-island',
    'properties': {
        'id': 'ground-roundabout-island',
        'name': 'SJEC Central Roundabout & Monument Garden',
        'category': 'landmark',
        'type': 'garden_island',
        'color': '#15803d', # Green island
        'opacity': 0.95
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [roundabout_island]
    }
})
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'island_curb', 'color': '#f8fafc', 'width': 2 },
    'geometry': { 'type': 'LineString', 'coordinates': roundabout_island }
})

print(f"Generated {len(grounds_features)} ground polygons and {len(details_features)} pitch/court detail lines.")

# Save sjec_real_grounds.json
grounds_fc = {
    'type': 'FeatureCollection',
    'features': grounds_features
}
with open('src/data/sjec_real_grounds.json', 'w') as f:
    json.dump(grounds_fc, f, indent=2)

# Save sports pitch details
with open('src/data/sjec_real_court_markings.json', 'w') as f:
    json.dump({'type': 'FeatureCollection', 'features': details_features}, f, indent=2)

print("Saved grounds & court markings!")
