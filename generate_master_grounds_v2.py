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

# ==============================================================================
# 1. MAIN ATHLETICS STADIUM (Way 1537946636)
# ==============================================================================
stadium_coords = close_ring(ways['1537946636'])
cx = sum(p[0] for p in stadium_coords[:-1]) / (len(stadium_coords)-1)
cy = sum(p[1] for p in stadium_coords[:-1]) / (len(stadium_coords)-1)

# Outer 400m Running Track Surface (Terracotta Polyurethane)
grounds_features.append({
    'type': 'Feature',
    'id': 'ground-main-stadium-track',
    'properties': {
        'id': 'ground-main-stadium-track',
        'name': 'Saint Joseph College Ground (400m Athletic Track)',
        'category': 'sports',
        'type': 'running_track',
        'color': '#852b1b', # Authentic brick-red / terracotta running track
        'opacity': 0.96
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [stadium_coords]
    }
})

# Inner Turf Field (Scaled ~0.80 towards centroid)
inner_turf_coords = []
for p in stadium_coords:
    nx = cx + (p[0] - cx) * 0.80
    ny = cy + (p[1] - cy) * 0.80
    inner_turf_coords.append([nx, ny])

grounds_features.append({
    'type': 'Feature',
    'id': 'ground-main-stadium-turf',
    'properties': {
        'id': 'ground-main-stadium-turf',
        'name': 'Saint Joseph College Ground (Football & Cricket Pitch)',
        'category': 'sports',
        'type': 'grass_pitch',
        'color': '#15803d', # Vibrant natural athletic grass turf
        'opacity': 0.98
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [inner_turf_coords]
    }
})

# 6 Multi-lane running track white lane lines
for scale in [0.97, 0.93, 0.89, 0.86, 0.83, 0.80]:
    lane_coords = [[cx + (p[0] - cx) * scale, cy + (p[1] - cy) * scale] for p in stadium_coords]
    details_features.append({
        'type': 'Feature',
        'properties': {
            'type': 'track_lane',
            'color': '#ffffff',
            'width': 1.1,
            'dash': [6, 3]
        },
        'geometry': {
            'type': 'LineString',
            'coordinates': lane_coords
        }
    })

# Football field pitch markings on inner turf
fw = 0.00045
fh = 0.00032
pitch_box = [
    [cx - fw, cy - fh],
    [cx + fw, cy - fh],
    [cx + fw, cy + fh],
    [cx - fw, cy + fh],
    [cx - fw, cy - fh]
]
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'pitch_marking', 'color': '#ffffff', 'width': 1.8 },
    'geometry': { 'type': 'LineString', 'coordinates': pitch_box }
})
# Halfway line
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'pitch_marking', 'color': '#ffffff', 'width': 1.8 },
    'geometry': { 'type': 'LineString', 'coordinates': [[cx - fw, cy], [cx + fw, cy]] }
})
# Center circle
circle_pts = []
for deg in range(0, 361, 15):
    rad = math.radians(deg)
    rx = cx + math.cos(rad) * 0.000075
    ry = cy + math.sin(rad) * 0.000075
    circle_pts.append([rx, ry])
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'pitch_marking', 'color': '#ffffff', 'width': 1.8 },
    'geometry': { 'type': 'LineString', 'coordinates': circle_pts }
})
# Goal boxes (North & South ends)
for dy in [-fh, fh]:
    sign = -1 if dy > 0 else 1
    gw = 0.00018
    gh = 0.00008
    box = [
        [cx - gw, dy],
        [cx - gw, dy + sign * gh],
        [cx + gw, dy + sign * gh],
        [cx + gw, dy]
    ]
    details_features.append({
        'type': 'Feature',
        'properties': { 'type': 'pitch_marking', 'color': '#ffffff', 'width': 1.5 },
        'geometry': { 'type': 'LineString', 'coordinates': box }
    })

# ==============================================================================
# 2. TOURNAMENT BASKETBALL COURT (Way 1537952627) - Professional Dual Tone
# ==============================================================================
bb_coords = close_ring(ways['1537952627'])
bcx = sum(p[0] for p in bb_coords[:-1]) / (len(bb_coords)-1)
bcy = sum(p[1] for p in bb_coords[:-1]) / (len(bb_coords)-1)

# Outer apron (Forest Green)
grounds_features.append({
    'type': 'Feature',
    'id': 'ground-basketball-court-apron',
    'properties': {
        'id': 'ground-basketball-court',
        'name': 'Synthetic Basketball Court (Apron)',
        'category': 'sports',
        'type': 'court_apron',
        'color': '#14532d', # Deep forest green apron
        'opacity': 0.98
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [bb_coords]
    }
})

# Inner playing court (FIBA Royal Blue)
inner_bb_coords = [[bcx + (p[0] - bcx) * 0.88, bcy + (p[1] - bcy) * 0.88] for p in bb_coords]
grounds_features.append({
    'type': 'Feature',
    'id': 'ground-basketball-court-inner',
    'properties': {
        'id': 'ground-basketball-court-inner',
        'name': 'Synthetic Basketball Court (Inbounds)',
        'category': 'sports',
        'type': 'court_playing',
        'color': '#1d4ed8', # Professional court blue
        'opacity': 0.98
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [inner_bb_coords]
    }
})

# White boundary line
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'court_line', 'color': '#ffffff', 'width': 2.0 },
    'geometry': { 'type': 'LineString', 'coordinates': inner_bb_coords }
})
# Center circle
bb_circle = []
for deg in range(0, 361, 20):
    rad = math.radians(deg)
    bb_circle.append([bcx + math.cos(rad) * 0.00003, bcy + math.sin(rad) * 0.00003])
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'court_line', 'color': '#ffffff', 'width': 1.6 },
    'geometry': { 'type': 'LineString', 'coordinates': bb_circle }
})

# ==============================================================================
# 3. VOLLEYBALL CLAY COURT (Way 1537945385)
# ==============================================================================
vb_coords = close_ring(ways['1537945385'])
grounds_features.append({
    'type': 'Feature',
    'id': 'ground-volleyball-court',
    'properties': {
        'id': 'ground-volleyball-court',
        'name': 'SJEC Volleyball Court (Clay)',
        'category': 'sports',
        'type': 'court_clay',
        'color': '#b45309', # Natural crushed clay amber
        'opacity': 0.98
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [vb_coords]
    }
})
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'court_line', 'color': '#ffffff', 'width': 2.0 },
    'geometry': { 'type': 'LineString', 'coordinates': vb_coords }
})
# Net line across center
vcx = sum(p[0] for p in vb_coords[:-1]) / (len(vb_coords)-1)
vcy = sum(p[1] for p in vb_coords[:-1]) / (len(vb_coords)-1)
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'court_net', 'color': '#f8fafc', 'width': 2.8 },
    'geometry': { 'type': 'LineString', 'coordinates': [[vb_coords[0][0], vcy], [vb_coords[1][0], vcy]] }
})

# ==============================================================================
# 4. OUTDOOR BADMINTON COURTS (Ways 1538919065 & 1538919073)
# ==============================================================================
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
            'color': '#047857', # Tournament dark emerald
            'opacity': 0.96
        },
        'geometry': {
            'type': 'Polygon',
            'coordinates': [bm_coords]
        }
    })
    details_features.append({
        'type': 'Feature',
        'properties': { 'type': 'court_line', 'color': '#ffffff', 'width': 1.6 },
        'geometry': { 'type': 'LineString', 'coordinates': bm_coords }
    })

# ==============================================================================
# 5. JOSARENA OPEN-AIR AMPHITHEATRE (Way 1533207277)
# ==============================================================================
amphi_coords = close_ring(ways['1533207277'])
acx = sum(p[0] for p in amphi_coords[:-1]) / (len(amphi_coords)-1)
acy = sum(p[1] for p in amphi_coords[:-1]) / (len(amphi_coords)-1)

grounds_features.append({
    'type': 'Feature',
    'id': 'ground-josarena-amphi',
    'properties': {
        'id': 'ground-josarena-amphi',
        'name': 'Josarena Open-Air Amphitheatre (Hillside Stone Steps)',
        'category': 'landmark',
        'type': 'amphitheatre',
        'color': '#334155', # Dressed laterite / granite stone tiers
        'opacity': 0.98
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [amphi_coords]
    }
})

# Concentric stone seating steps
for s in [0.85, 0.70, 0.55, 0.40]:
    step_coords = [[acx + (p[0] - acx) * s, acy + (p[1] - acy) * s] for p in amphi_coords]
    details_features.append({
        'type': 'Feature',
        'properties': { 'type': 'amphi_step', 'color': '#94a3b8', 'width': 1.8 },
        'geometry': { 'type': 'LineString', 'coordinates': step_coords }
    })

# Raised Performance Stage
stage_box = [
    [acx - 0.00010, acy - 0.00006],
    [acx + 0.00010, acy - 0.00006],
    [acx + 0.00010, acy + 0.00006],
    [acx - 0.00010, acy + 0.00006],
    [acx - 0.00010, acy - 0.00006]
]
grounds_features.append({
    'type': 'Feature',
    'id': 'ground-josarena-stage',
    'properties': {
        'id': 'ground-josarena-stage',
        'name': 'Josarena Performance Stage',
        'category': 'landmark',
        'type': 'stage',
        'color': '#1e293b',
        'opacity': 1.0
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [stage_box]
    }
})
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'stage_rim', 'color': '#06b6d4', 'width': 2.0 },
    'geometry': { 'type': 'LineString', 'coordinates': stage_box }
})

# ==============================================================================
# 6. STUDENT SQUARE (Way 1538932918) - Paved Plaza
# ==============================================================================
sq_coords = close_ring(ways['1538932918'])
grounds_features.append({
    'type': 'Feature',
    'id': 'ground-student-square',
    'properties': {
        'id': 'ground-student-square',
        'name': 'Student Square (Interlocking Paver Plaza)',
        'category': 'amenity',
        'type': 'plaza',
        'color': '#2a3447', # Interlocking paver block tone
        'opacity': 0.98
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [sq_coords]
    }
})
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'plaza_curb', 'color': '#64748b', 'width': 1.5 },
    'geometry': { 'type': 'LineString', 'coordinates': sq_coords }
})

# ==============================================================================
# 7. MARY'S GARDEN (Way 1538919029) - Manicured Lawn
# ==============================================================================
mg_coords = close_ring(ways['1538919029'])
grounds_features.append({
    'type': 'Feature',
    'id': 'ground-marys-garden',
    'properties': {
        'id': 'ground-marys-garden',
        'name': "Mary's Garden & Quad Lawn",
        'category': 'amenity',
        'type': 'garden',
        'color': '#166534', # Deep lush tropical grass
        'opacity': 0.98
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [mg_coords]
    }
})
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'garden_border', 'color': '#15803d', 'width': 1.5 },
    'geometry': { 'type': 'LineString', 'coordinates': mg_coords }
})

# ==============================================================================
# 8. PAVED PARKING LOTS (Ways 1537948853 & 1537956248)
# ==============================================================================
pk1_coords = close_ring(ways['1537948853'])
grounds_features.append({
    'type': 'Feature',
    'id': 'ground-parking-main',
    'properties': {
        'id': 'ground-parking-main',
        'name': 'Main Entrance Visitor Parking (Asphalt)',
        'category': 'amenity',
        'type': 'parking',
        'color': '#1e293b', # Smooth dark asphalt
        'opacity': 0.95
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [pk1_coords]
    }
})
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'parking_curb', 'color': '#475569', 'width': 1.5 },
    'geometry': { 'type': 'LineString', 'coordinates': pk1_coords }
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
        'opacity': 0.95
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [pk2_coords]
    }
})

# ==============================================================================
# 9. CENTRAL ROUNDABOUT & MONUMENT ISLAND
# ==============================================================================
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
        'name': 'SJEC Central Roundabout Garden Island',
        'category': 'landmark',
        'type': 'garden_island',
        'color': '#15803d',
        'opacity': 0.98
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [roundabout_island]
    }
})
details_features.append({
    'type': 'Feature',
    'properties': { 'type': 'island_curb', 'color': '#f8fafc', 'width': 2.2 },
    'geometry': { 'type': 'LineString', 'coordinates': roundabout_island }
})

# Save to JSON
with open('src/data/sjec_real_grounds.json', 'w') as f:
    json.dump({'type': 'FeatureCollection', 'features': grounds_features}, f, indent=2)

with open('src/data/sjec_real_court_markings.json', 'w') as f:
    json.dump({'type': 'FeatureCollection', 'features': details_features}, f, indent=2)

print(f"Generated {len(grounds_features)} realistic ground polygons & {len(details_features)} pitch markings.")
