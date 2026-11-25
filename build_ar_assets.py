import json
import math

def make_ellipse_coords(cx, cy, rx, ry, n=64, start_deg=0, end_deg=360):
    coords = []
    total_steps = n
    deg_span = end_deg - start_deg
    for i in range(total_steps + 1):
        deg = start_deg + (deg_span * i / total_steps)
        rad = math.radians(deg)
        coords.append([round(cx + rx * math.cos(rad), 7), round(cy + ry * math.sin(rad), 7)])
    return coords

def make_circle_coords(cx, cy, r_deg, n=32):
    return make_ellipse_coords(cx, cy, r_deg, r_deg * 0.98, n)

grounds = []
markings = []

# =========================================================================
# 1. ATHLETIC STADIUM (ST JOSEPH COLLEGE GROUND) - Exact from drone photo
# =========================================================================
stad_cx = 74.90095
stad_cy = 12.91035
track_rx_outer = 0.00092
track_ry_outer = 0.00062
field_rx = 0.00072
field_ry = 0.00042

grounds.append({
    'type': 'Feature',
    'properties': {
        'id': 'ground-running-track',
        'name': 'St Joseph College Ground — 400m Running Track',
        'type': 'running_track',
        'surface': 'cinder_synthetic',
        'color': '#c2410c',
        'opacity': 0.98
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [make_ellipse_coords(stad_cx, stad_cy, track_rx_outer, track_ry_outer)]
    }
})

grounds.append({
    'type': 'Feature',
    'properties': {
        'id': 'ground-football-pitch',
        'name': 'Central Athletic Field & Football Pitch',
        'type': 'football_pitch',
        'surface': 'natural_turf',
        'color': '#22c55e',
        'opacity': 0.98
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [make_ellipse_coords(stad_cx, stad_cy, field_rx, field_ry)]
    }
})

# 6 Track lane lines
for lane_idx in range(7):
    frac = lane_idx / 6.0
    lrx = field_rx + (track_rx_outer - field_rx) * frac
    lry = field_ry + (track_ry_outer - field_ry) * frac
    markings.append({
        'type': 'Feature',
        'properties': {
            'id': f'track-lane-{lane_idx+1}',
            'name': f'Athletic Track Lane {lane_idx+1}',
            'color': '#ffffff',
            'width': 1.2
        },
        'geometry': {
            'type': 'LineString',
            'coordinates': make_ellipse_coords(stad_cx, stad_cy, lrx, lry)
        }
    })

# Football pitch regulation lines
fw = 0.00054
fh = 0.00030
markings.append({
    'type': 'Feature',
    'properties': {'id': 'pitch-boundary', 'name': 'Football Pitch Touchlines', 'color': '#ffffff', 'width': 1.6},
    'geometry': {
        'type': 'LineString',
        'coordinates': [
            [round(stad_cx - fw, 7), round(stad_cy - fh, 7)],
            [round(stad_cx + fw, 7), round(stad_cy - fh, 7)],
            [round(stad_cx + fw, 7), round(stad_cy + fh, 7)],
            [round(stad_cx - fw, 7), round(stad_cy + fh, 7)],
            [round(stad_cx - fw, 7), round(stad_cy - fh, 7)]
        ]
    }
})

markings.append({
    'type': 'Feature',
    'properties': {'id': 'pitch-halfway', 'name': 'Halfway Line', 'color': '#ffffff', 'width': 1.6},
    'geometry': {
        'type': 'LineString',
        'coordinates': [
            [round(stad_cx, 7), round(stad_cy - fh, 7)],
            [round(stad_cx, 7), round(stad_cy + fh, 7)]
        ]
    }
})

markings.append({
    'type': 'Feature',
    'properties': {'id': 'pitch-center-circle', 'name': 'Center Circle', 'color': '#ffffff', 'width': 1.6},
    'geometry': {
        'type': 'LineString',
        'coordinates': make_circle_coords(stad_cx, stad_cy, 0.000085)
    }
})

# =========================================================================
# 2. JOSARENA OPEN-AIR AMPHITHEATRE (Exact match to user's photo media_1795537768052_2df5c568.jpg)
# =========================================================================
josa_cx = 74.89945
josa_cy = 12.91105

# Outer Paver Promenade enclosing Josarena
grounds.append({
    'type': 'Feature',
    'properties': {
        'id': 'josarena-promenade',
        'name': 'Josarena Upper Paver Promenade & Walkway',
        'type': 'plaza_pavement',
        'color': '#ded8ce',
        'opacity': 0.95
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [make_ellipse_coords(josa_cx, josa_cy, 0.00015, 0.00013, 32, 200, 360) + [[josa_cx, josa_cy], [round(josa_cx + 0.00015 * math.cos(math.radians(200)), 7), round(josa_cy + 0.00013 * math.sin(math.radians(200)), 7)]]]
    }
})

# Concentric Alternating Grass Terraces and Stone Steps
for tier in range(8):
    tr = 0.000035 + tier * 0.000014
    is_grass = (tier % 2 == 0)
    label = 'Lawn Terrace' if is_grass else 'Stone Step Seating'
    grounds.append({
        'type': 'Feature',
        'properties': {
            'id': f'josarena-tier-{tier+1}',
            'name': f'Josarena Amphitheatre {label} Tier {tier+1}',
            'type': 'amphitheatre_steps',
            'color': '#22c55e' if is_grass else '#cbd5e1',
            'opacity': 0.98
        },
        'geometry': {
            'type': 'Polygon',
            'coordinates': [make_ellipse_coords(josa_cx, josa_cy, tr, tr * 0.92, 24, 210, 350) + [[josa_cx, josa_cy], [round(josa_cx + tr * math.cos(math.radians(210)), 7), round(josa_cy + tr * 0.92 * math.sin(math.radians(210)), 7)]]]
        }
    })

# Hexagonal Stone Stage at base of Josarena
grounds.append({
    'type': 'Feature',
    'properties': {
        'id': 'josarena-stage',
        'name': 'Josarena Performance Stone Stage',
        'type': 'amphitheatre_stage',
        'color': '#94a3b8',
        'opacity': 1.0
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [make_circle_coords(josa_cx, josa_cy - 0.000005, 0.000028, 6)]
    }
})

# =========================================================================
# 3. BASKETBALL COURT (Exact match to photos 970ea679.jpg & 568afbc9.png)
# =========================================================================
bb_cx = 74.89899
bb_cy = 12.91041
bb_w = 0.00012
bb_h = 0.00022
apron_pad = 0.000025

# Concrete outer apron
grounds.append({
    'type': 'Feature',
    'properties': {
        'id': 'court-bb-apron',
        'name': 'Basketball Court Concrete Apron Deck',
        'type': 'sports_court_apron',
        'surface': 'concrete_deck',
        'color': '#cbd5e1',
        'opacity': 0.98
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [[
            [round(bb_cx - bb_w - apron_pad, 7), round(bb_cy - bb_h - apron_pad, 7)],
            [round(bb_cx + bb_w + apron_pad, 7), round(bb_cy - bb_h - apron_pad, 7)],
            [round(bb_cx + bb_w + apron_pad, 7), round(bb_cy + bb_h + apron_pad, 7)],
            [round(bb_cx - bb_w - apron_pad, 7), round(bb_cy + bb_h + apron_pad, 7)],
            [round(bb_cx - bb_w - apron_pad, 7), round(bb_cy - bb_h - apron_pad, 7)]
        ]]
    }
})

# Inbounds playing surface (Light concrete grey)
grounds.append({
    'type': 'Feature',
    'properties': {
        'id': 'court-bb-inbounds',
        'name': 'Basketball Court Inbounds Surface',
        'type': 'basketball_court',
        'surface': 'acrylic_concrete',
        'color': '#e2e8f0',
        'opacity': 0.98
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [[
            [round(bb_cx - bb_w, 7), round(bb_cy - bb_h, 7)],
            [round(bb_cx + bb_w, 7), round(bb_cy - bb_h, 7)],
            [round(bb_cx + bb_w, 7), round(bb_cy + bb_h, 7)],
            [round(bb_cx - bb_w, 7), round(bb_cy + bb_h, 7)],
            [round(bb_cx - bb_w, 7), round(bb_cy - bb_h, 7)]
        ]]
    }
})

# Golden Yellow 3-Point Aprons (Both baskets from photo!)
for sign in [-1, 1]:
    arc_cy = bb_cy + sign * (bb_h - 0.00007)
    grounds.append({
        'type': 'Feature',
        'properties': {
            'id': f'court-bb-yellow-apron-{sign}',
            'name': 'Basketball Court 3-Point Gold Zone',
            'type': 'court_marking_zone',
            'color': '#eab308',
            'opacity': 0.98
        },
        'geometry': {
            'type': 'Polygon',
            'coordinates': [make_ellipse_coords(bb_cx, arc_cy, 0.000065, 0.000055, 32)]
        }
    })

# Terracotta / Red-Orange Key Free-Throw Boxes (from photo!)
for sign in [-1, 1]:
    key_cy = bb_cy + sign * (bb_h - 0.000045)
    kw = 0.000035
    kh = 0.000045
    grounds.append({
        'type': 'Feature',
        'properties': {
            'id': f'court-bb-red-key-{sign}',
            'name': 'Basketball Court Terracotta Key Box',
            'type': 'court_key_box',
            'color': '#ea580c',
            'opacity': 0.98
        },
        'geometry': {
            'type': 'Polygon',
            'coordinates': [[
                [round(bb_cx - kw, 7), round(key_cy - kh, 7)],
                [round(bb_cx + kw, 7), round(key_cy - kh, 7)],
                [round(bb_cx + kw, 7), round(key_cy + kh, 7)],
                [round(bb_cx - kw, 7), round(key_cy + kh, 7)],
                [round(bb_cx - kw, 7), round(key_cy - kh, 7)]
            ]]
        }
    })

# Sky Blue Center Circle & Free Throw Circles (from photo!)
grounds.append({
    'type': 'Feature',
    'properties': {
        'id': 'court-bb-blue-center-circle',
        'name': 'Basketball Court Sky Blue Center Circle',
        'type': 'court_center_circle',
        'color': '#0284c7',
        'opacity': 0.98
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [make_circle_coords(bb_cx, bb_cy, 0.000030)]
    }
})

for sign in [-1, 1]:
    ft_cy = bb_cy + sign * (bb_h - 0.00009)
    grounds.append({
        'type': 'Feature',
        'properties': {
            'id': f'court-bb-blue-freethrow-{sign}',
            'name': 'Basketball Court Sky Blue Free-Throw Circle',
            'type': 'court_circle',
            'color': '#0284c7',
            'opacity': 0.98
        },
        'geometry': {
            'type': 'Polygon',
            'coordinates': [make_circle_coords(bb_cx, ft_cy, 0.000025)]
        }
    })

# White Lines for Basketball Court
markings.append({
    'type': 'Feature',
    'properties': {'id': 'bb-boundary-line', 'name': 'Basketball Court Boundary', 'color': '#ffffff', 'width': 1.6},
    'geometry': {
        'type': 'LineString',
        'coordinates': [
            [round(bb_cx - bb_w, 7), round(bb_cy - bb_h, 7)],
            [round(bb_cx + bb_w, 7), round(bb_cy - bb_h, 7)],
            [round(bb_cx + bb_w, 7), round(bb_cy + bb_h, 7)],
            [round(bb_cx - bb_w, 7), round(bb_cy + bb_h, 7)],
            [round(bb_cx - bb_w, 7), round(bb_cy - bb_h, 7)]
        ]
    }
})

markings.append({
    'type': 'Feature',
    'properties': {'id': 'bb-half-line', 'name': 'Basketball Half-Court Line', 'color': '#ffffff', 'width': 1.6},
    'geometry': {
        'type': 'LineString',
        'coordinates': [
            [round(bb_cx - bb_w, 7), round(bb_cy, 7)],
            [round(bb_cx + bb_w, 7), round(bb_cy, 7)]
        ]
    }
})

# =========================================================================
# 4. VOLLEYBALL / BADMINTON COURTS (Photo media_1795537826001_970ea679.jpg)
# =========================================================================
vb_cx = 74.89880
vb_cy = 12.91028
vb_w = 0.00008
vb_h = 0.00010

grounds.append({
    'type': 'Feature',
    'properties': {
        'id': 'court-volleyball-surface',
        'name': 'Volleyball & Badminton Courts',
        'type': 'volleyball_court',
        'color': '#94a3b8',
        'opacity': 0.95
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [[
            [round(vb_cx - vb_w, 7), round(vb_cy - vb_h, 7)],
            [round(vb_cx + vb_w, 7), round(vb_cy - vb_h, 7)],
            [round(vb_cx + vb_w, 7), round(vb_cy + vb_h, 7)],
            [round(vb_cx - vb_w, 7), round(vb_cy + vb_h, 7)],
            [round(vb_cx - vb_w, 7), round(vb_cy - vb_h, 7)]
        ]]
    }
})

# =========================================================================
# 5. STUDENT SQUARE & COURTYARD PAVED PLAZAS
# =========================================================================
grounds.append({
    'type': 'Feature',
    'properties': {
        'id': 'plaza-student-square',
        'name': 'Student Square Interlocking Paver Promenade',
        'type': 'plaza_pavement',
        'surface': 'sandstone_pavers',
        'color': '#ded8ce',
        'opacity': 0.95
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [[
            [74.89880, 12.91040],
            [74.89920, 12.91040],
            [74.89925, 12.91080],
            [74.89890, 12.91080],
            [74.89880, 12.91060],
            [74.89880, 12.91040]
        ]]
    }
})

# Admin Forecourt & Portico Paved Apron
grounds.append({
    'type': 'Feature',
    'properties': {
        'id': 'plaza-admin-forecourt',
        'name': 'Administrative Block Forecourt & Portico Apron',
        'type': 'plaza_pavement',
        'color': '#e5e0d8',
        'opacity': 0.95
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [[
            [74.89850, 12.91050],
            [74.89892, 12.91050],
            [74.89892, 12.91060],
            [74.89850, 12.91060],
            [74.89850, 12.91050]
        ]]
    }
})

# Admin Roundabout Manicured Green Lawn Mound (with St. Joseph Statue from photo media_1795537700260_9fc64388.png!)
grounds.append({
    'type': 'Feature',
    'properties': {
        'id': 'lawn-admin-roundabout',
        'name': 'St Joseph Statue Roundabout Lawn Mound',
        'type': 'manicured_lawn',
        'surface': 'tropical_lawn',
        'color': '#16a34a',
        'opacity': 0.98
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [make_circle_coords(74.89868, 12.91054, 0.000035)]
    }
})

# St Joseph statue pedestal in center of roundabout
grounds.append({
    'type': 'Feature',
    'properties': {
        'id': 'statue-st-joseph-pedestal',
        'name': 'Patron Saint Joseph Statue Pedestal',
        'type': 'architectural_monument',
        'color': '#ffffff',
        'opacity': 1.0
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [make_circle_coords(74.89868, 12.91054, 0.000008)]
    }
})

# AB-III Entrance Plaza & Promenade
grounds.append({
    'type': 'Feature',
    'properties': {
        'id': 'plaza-ab3-entrance',
        'name': 'Academic Block III Entrance Plaza',
        'type': 'plaza_pavement',
        'color': '#cbd5e1',
        'opacity': 0.95
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [[
            [74.89928, 12.91015],
            [74.89988, 12.91015],
            [74.89988, 12.91022],
            [74.89928, 12.91022],
            [74.89928, 12.91015]
        ]]
    }
})

# Chapel Stepped Paved Apron (from photo media_1795538229433_9097ba55.png)
grounds.append({
    'type': 'Feature',
    'properties': {
        'id': 'plaza-chapel-steps',
        'name': 'Saint Pio Chapel Entrance Stepped Plaza',
        'type': 'plaza_pavement',
        'color': '#ded8ce',
        'opacity': 0.95
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [make_circle_coords(74.89913, 12.91090, 0.000035)]
    }
})

# Main Gate Entry Plaza & Highway Entrance (from photo media_1795537944181_ac6a3487.jpg)
grounds.append({
    'type': 'Feature',
    'properties': {
        'id': 'plaza-main-gate',
        'name': 'Main Entrance Gate Apron & Security Forecourt',
        'type': 'plaza_pavement',
        'color': '#475569',
        'opacity': 0.98
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [[
            [74.89725, 12.91040],
            [74.89760, 12.91040],
            [74.89760, 12.91070],
            [74.89725, 12.91070],
            [74.89725, 12.91040]
        ]]
    }
})

# Save files
with open('src/data/sjec_real_grounds.json', 'w') as f:
    json.dump({'type': 'FeatureCollection', 'features': grounds}, f, indent=2)

with open('src/data/sjec_real_court_markings.json', 'w') as f:
    json.dump({'type': 'FeatureCollection', 'features': markings}, f, indent=2)

print('Generated enhanced photo-matched grounds and court markings.')
