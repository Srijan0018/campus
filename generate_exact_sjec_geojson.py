import xml.etree.ElementTree as ET
import json
import math

tree = ET.parse('sjec_real_osm.osm')
root = tree.getroot()

nodes = {n.get('id'): (float(n.get('lon')), float(n.get('lat'))) for n in root.findall('node')}

# 1. SJEC Campus Boundary (Way 279811603)
boundary_way = None
for w in root.findall('way'):
    if w.get('id') == '279811603':
        refs = [nd.get('ref') for nd in w.findall('nd')]
        boundary_coords = [list(nodes[r]) for r in refs if r in nodes]
        break

print(f"Extracted SJEC boundary with {len(boundary_coords)} vertices")

# 2. Extract Buildings
buildings_meta = {
    '1537949013': {
        'name': 'Academic Block II (AB-II)',
        'shortName': 'AB-II',
        'category': 'academic',
        'levels': 6,
        'height': 24,
        'color': '#1e3a8a',
        'roofColor': '#2563eb',
        'facade': 'glass-accent',
        'description': 'Premier academic hub housing Computer Science (CSE), Information Science (ISE), and the Central Computer Centre (CCC) in the basement. Features the state-of-the-art 1,000-seat Kalam Auditorium on the top floor.',
        'departments': ['Computer Science & Engineering', 'Information Science & Engineering', 'Computer Applications (MCA)'],
        'facilities': ['A.P.J. Abdul Kalam Auditorium (5th Floor - 1,000 capacity)', 'Central Computer Centre (Basement)', 'AI & Robotics Research Lab', 'Advanced Server Room'],
        'photo': 'https://images.shiksha.com/mediadata/images/1501133097phpxoZBkv.jpeg'
    },
    '1537942437': {
        'name': 'Academic Block III (AB-III)',
        'shortName': 'AB-III',
        'category': 'academic',
        'levels': 9,
        'height': 32,
        'color': '#0f172a',
        'roofColor': '#0284c7',
        'facade': 'sky-accent',
        'description': 'Tallest architectural landmark on campus (9 levels). Houses Electronics & Communication (ECE), Electrical & Electronics (EEE), Artificial Intelligence & Data Science (AI&DS), MBA, and the top-floor Spoorthi Conference Hall.',
        'departments': ['Electronics & Communication Engg', 'Electrical & Electronics Engg', 'Artificial Intelligence & Data Science', 'Business Administration (MBA)'],
        'facilities': ['Spoorthi Conference Hall (7th Floor - 400 seats)', 'VLSI & Embedded Systems Studio', 'Power Systems Lab', 'Executive MBA Lecture Theatres']
    },
    '1537952351': {
        'name': 'Administrative Block',
        'shortName': 'Admin',
        'category': 'administrative',
        'levels': 4,
        'height': 16,
        'color': '#0f766e',
        'roofColor': '#14b8a6',
        'facade': 'teal-accent',
        'description': 'The executive heart of St Joseph Engineering College. Accommodates the Director’s Office, Principal’s Office, Admissions, Accounts, Board Room, and Controller of Examinations.',
        'departments': ['Directorate & Governance', 'Principal & Academic Dean', 'Admissions & Student Welfare', 'Finance & Examination Cell'],
        'facilities': ['Main College Reception & Information Counter', 'Executive Council Chamber', 'Central Archives', 'Visitor Boardroom']
    },
    '1537951217': {
        'name': 'Department of Civil Engineering',
        'shortName': 'Civil Engg',
        'category': 'academic',
        'levels': 5,
        'height': 20,
        'color': '#334155',
        'roofColor': '#475569',
        'facade': 'slate-accent',
        'description': 'Multi-tier modern facility equipped with advanced structural testing apparatus, environmental laboratories, and computer-aided structural design studios.',
        'departments': ['Civil Engineering'],
        'facilities': ['Structural Dynamics & Materials Lab', 'Geotechnical Soil Mechanics Lab', 'Environmental Water Analysis Lab', 'Total Station & Surveying Centre']
    },
    '1537949097': {
        'name': 'Civil Block & Workshop Annex',
        'shortName': 'Civil Annex',
        'category': 'academic',
        'levels': 3,
        'height': 13,
        'color': '#475569',
        'roofColor': '#64748b',
        'facade': 'stone-accent',
        'description': 'Specialized heavy structural prototyping and concrete testing facility.',
        'departments': ['Civil Engineering Testing Division'],
        'facilities': ['Highway Materials Laboratory', 'Concrete Technology Testing Beds']
    },
    '1537941341': {
        'name': 'Saint Pio Chapel',
        'shortName': 'Chapel',
        'category': 'landmark',
        'levels': 3,
        'height': 16,
        'color': '#b45309',
        'roofColor': '#f59e0b',
        'facade': 'amber-glow',
        'description': 'Iconic campus sanctuary nestled in the central quadrangle, featuring high vaulted ceilings, stained glass windows, and a serene prayer garden.',
        'departments': ['Campus Ministry & Spiritual Wellness'],
        'facilities': ['Central Nave & Sanctuary', 'Choir Loft', 'Marian Meditation Grotto', 'Chaplain Counseling Chamber']
    },
    '1537940526': {
        'name': 'Saint Joseph Gents Hostel',
        'shortName': 'Gents Hostel',
        'category': 'hostel',
        'levels': 5,
        'height': 18,
        'color': '#1e1b4b',
        'roofColor': '#4338ca',
        'facade': 'indigo-accent',
        'description': 'Expansive residential complex for male students offering modern furnished rooms, central steam mess, Wi-Fi study lounges, and indoor sports.',
        'departments': ['Hostel Administration'],
        'facilities': ['Central Dining Mess (300+ seating)', 'Recreation Hall (Table Tennis, Carrom)', 'Solar Water Heating', 'Resident Warden Office']
    },
    '1537942615': {
        'name': 'Saint Joseph Girls Hostel',
        'shortName': 'Girls Hostel',
        'category': 'hostel',
        'levels': 5,
        'height': 18,
        'color': '#831843',
        'roofColor': '#db2777',
        'facade': 'rose-accent',
        'description': 'Secure multi-storey residence for female students with premium air-conditioned units, dedicated dining, study lounges, and round-the-clock security.',
        'departments': ['Ladies Hostel Directorate'],
        'facilities': ['Air Conditioned Suites', 'Dedicated In-House Dining Mess', 'Reading Room', '24/7 CCTV & Security Desk']
    },
    '1537925229': {
        'name': 'Bethania House',
        'shortName': 'Bethania',
        'category': 'hostel',
        'levels': 3,
        'height': 12,
        'color': '#312e81',
        'roofColor': '#4f46e5',
        'facade': 'purple-accent',
        'description': 'Historic residential lodge and pastoral retreat on campus.',
        'departments': ['Pastoral Care'],
        'facilities': ['Guest Rooms', 'Seminar Room']
    },
    '1537925232': {
        'name': 'Guest House & Faculty Residence',
        'shortName': 'Guest House',
        'category': 'amenity',
        'levels': 2,
        'height': 9,
        'color': '#475569',
        'roofColor': '#ea580c',
        'facade': 'orange-roof',
        'description': 'Furnished executive guest rooms with hipped tiled roofs accommodating visiting university dignitaries, examiners, and corporate recruiters.',
        'departments': ['Hospitality'],
        'facilities': ['Executive Suites', 'Visiting Faculty Dining']
    },
    '1537948656': {
        'name': 'Academic & Faculty Residence Complex',
        'shortName': 'Academic Annex',
        'category': 'academic',
        'levels': 5,
        'height': 18,
        'color': '#1e293b',
        'roofColor': '#ef4444',
        'facade': 'red-roof',
        'description': '5-storey building with red tiled hipped roof housing faculty quarters, student council rooms, and research project incubators.',
        'departments': ['Research & Innovation Incubation'],
        'facilities': ['Innovation & Entrepreneurship Cell', 'Faculty Quarters']
    },
    '1537948657': {
        'name': 'Main Entrance Security Gatehouse',
        'shortName': 'Gatehouse',
        'category': 'administrative',
        'levels': 1,
        'height': 5,
        'color': '#334155',
        'roofColor': '#06b6d4',
        'facade': 'cyan-crown',
        'description': 'Primary highway gateway along NH 169 with security surveillance, visitor verification, and automated vehicle barriers.',
        'departments': ['Campus Security'],
        'facilities': ['24/7 Checkpost', 'RFID Verification']
    },
    '1538919037': {
        'name': 'Mechanical Workshop Green Bay',
        'shortName': 'Mech Bay',
        'category': 'academic',
        'levels': 2,
        'height': 10,
        'color': '#334155',
        'roofColor': '#10b981',
        'facade': 'green-metal',
        'description': 'Heavy manufacturing workshop with gabled green metal roof housing lathe machines, shaping beds, and foundry bays.',
        'departments': ['Mechanical Engineering'],
        'facilities': ['Machine Shop', 'Welding & Forging Bay']
    },
    '1538919044': {
        'name': 'Central Covered Parking Pavilion',
        'shortName': 'Parking Pavilion',
        'category': 'amenity',
        'levels': 1,
        'height': 4,
        'color': '#1e293b',
        'roofColor': '#ef4444',
        'facade': 'red-metal',
        'description': 'Solar-canopied weather-protected parking zone for two-wheelers and staff automobiles.',
        'departments': ['Campus Facility Maintenance'],
        'facilities': ['EV Charging Stations', 'Shaded Vehicle Bays']
    },
    '1538919048': {
        'name': 'Central Canteen & Food Court',
        'shortName': 'Food Court',
        'category': 'amenity',
        'levels': 2,
        'height': 9,
        'color': '#7c2d12',
        'roofColor': '#ea580c',
        'facade': 'terracotta-roof',
        'description': 'Vibrant multi-cuisine campus dining facility serving Mangalorean snacks, fresh juice, coffee, and daily hot lunch.',
        'departments': ['Student Amenities'],
        'facilities': ['Food Court', 'The Lassi Corner', 'Stationery Store', 'ATM']
    },
    '1538919056': {
        'name': 'Scholars Residence Block A',
        'shortName': 'Scholars A',
        'category': 'hostel',
        'levels': 3,
        'height': 12,
        'color': '#334155',
        'roofColor': '#64748b',
        'facade': 'slate-roof',
        'description': 'Residential accommodation unit for postgraduate scholars and final-year student researchers.',
        'departments': ['Hostel Administration'],
        'facilities': ['Quiet Study Rooms', 'High-Speed Wi-Fi']
    },
    '1538919066': {
        'name': 'Scholars Residence Block B',
        'shortName': 'Scholars B',
        'category': 'hostel',
        'levels': 3,
        'height': 12,
        'color': '#334155',
        'roofColor': '#64748b',
        'facade': 'slate-roof',
        'description': 'Residential wing with hipped roof offering serene garden views.',
        'departments': ['Hostel Administration'],
        'facilities': ['Furnished Quarters']
    },
    '1533207274': {
        'name': 'North Utility & Electrical Substation',
        'shortName': 'Substation',
        'category': 'administrative',
        'levels': 1,
        'height': 5,
        'color': '#475569',
        'roofColor': '#f59e0b',
        'facade': 'amber-accent',
        'description': 'Dedicated campus electrical transformer station and generator backup vaults.',
        'departments': ['Electrical Maintenance'],
        'facilities': ['11kV Transformer', '500kVA Diesel Generators']
    },
    '1533207275': {
        'name': 'North Campus Maintenance Depot',
        'shortName': 'Maint Depot',
        'category': 'administrative',
        'levels': 1,
        'height': 5,
        'color': '#475569',
        'roofColor': '#64748b',
        'facade': 'grey-accent',
        'description': 'Logistics and maintenance equipment storage facility.',
        'departments': ['Estate Office'],
        'facilities': ['Groundskeeping Depot']
    }
}

buildings_features = []
for w in root.findall('way'):
    wid = w.get('id')
    if wid in buildings_meta:
        refs = [nd.get('ref') for nd in w.findall('nd')]
        coords = [list(nodes[r]) for r in refs if r in nodes]
        if coords[0] != coords[-1]:
            coords.append(coords[0])
            
        meta = buildings_meta[wid]
        clon = sum(c[0] for c in coords[:-1]) / (len(coords) - 1)
        clat = sum(c[1] for c in coords[:-1]) / (len(coords) - 1)
        
        feature = {
            'type': 'Feature',
            'id': f'bldg-{wid}',
            'properties': {
                'id': f'bldg-{wid}',
                'osmId': wid,
                'name': meta['name'],
                'shortName': meta['shortName'],
                'category': meta['category'],
                'height': meta['height'],
                'minHeight': 0,
                'floors': meta['levels'],
                'color': meta['color'],
                'roofColor': meta['roofColor'],
                'hoverColor': '#06b6d4',
                'description': meta['description'],
                'departments': meta.get('departments', []),
                'facilities': meta.get('facilities', []),
                'photo': meta.get('photo'),
                'entranceCoord': [round(clon, 6), round(clat, 6)],
                'centroid': [round(clon, 6), round(clat, 6)]
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': [coords]
            }
        }
        buildings_features.append(feature)

print(f"Generated {len(buildings_features)} exact real-world 3D building features")

# 3. Extract Sports Grounds, Courts, Amphitheatre, Gardens
grounds_features = []
for w in root.findall('way'):
    wid = w.get('id')
    tags = {t.get('k'): t.get('v') for t in w.findall('tag')}
    refs = [nd.get('ref') for nd in w.findall('nd')]
    coords = [list(nodes[r]) for r in refs if r in nodes]
    if not coords or len(coords) < 3:
        continue
    if coords[0] != coords[-1]:
        coords.append(coords[0])
        
    clon = sum(c[0] for c in coords[:-1]) / (len(coords) - 1)
    clat = sum(c[1] for c in coords[:-1]) / (len(coords) - 1)
    
    # Saint Joseph College Ground (Main Stadium)
    if wid == '1537946636':
        grounds_features.append({
            'type': 'Feature',
            'id': 'ground-main-stadium',
            'properties': {
                'id': 'ground-main-stadium',
                'name': 'Saint Joseph College Ground (Main Stadium)',
                'type': 'stadium_turf',
                'fillColor': '#064e3b',
                'outlineColor': '#10b981',
                'description': 'Regulation natural turf stadium field with athletic track for football tournaments, cricket matches, and annual sports meets.'
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': [coords]
            }
        })
    # Josarena Amphitheatre
    elif wid == '1533207277':
        grounds_features.append({
            'type': 'Feature',
            'id': 'josarena-amphitheatre',
            'properties': {
                'id': 'josarena-amphitheatre',
                'name': 'Josarena Open-Air Amphitheatre',
                'type': 'amphitheatre',
                'fillColor': '#065f46',
                'outlineColor': '#34d399',
                'description': 'Iconic 1,200-capacity stepped open-air cultural amphitheatre hosting annual TIARA fests and concerts.'
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': [coords]
            }
        })
    # Basketball Court
    elif wid == '1537952627' or tags.get('sport') == 'basketball':
        grounds_features.append({
            'type': 'Feature',
            'id': f'court-basketball-{wid}',
            'properties': {
                'id': f'court-basketball-{wid}',
                'name': 'Synthetic Basketball Hardcourt',
                'type': 'basketball_court',
                'fillColor': '#1d4ed8',
                'outlineColor': '#60a5fa',
                'description': 'Regulation acrylic synthetic basketball hardcourt with floodlights.'
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': [coords]
            }
        })
    # Volleyball Court
    elif wid == '1537945385' or tags.get('sport') == 'volleyball':
        grounds_features.append({
            'type': 'Feature',
            'id': 'court-volleyball',
            'properties': {
                'id': 'court-volleyball',
                'name': 'SJEC Volleyball Court',
                'type': 'volleyball_court',
                'fillColor': '#b45309',
                'outlineColor': '#f59e0b',
                'description': 'Red clay outdoor volleyball court.'
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': [coords]
            }
        })
    # Badminton Courts
    elif tags.get('sport') == 'badminton':
        grounds_features.append({
            'type': 'Feature',
            'id': f'court-badminton-{wid}',
            'properties': {
                'id': f'court-badminton-{wid}',
                'name': 'Badminton Court',
                'type': 'badminton_court',
                'fillColor': '#059669',
                'outlineColor': '#34d399',
                'description': 'Outdoor badminton court.'
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': [coords]
            }
        })
    # Mary's Garden
    elif wid == '1538919029':
        grounds_features.append({
            'type': 'Feature',
            'id': 'garden-mary',
            'properties': {
                'id': 'garden-mary',
                'name': "Mary's Garden & Quad Lawn",
                'type': 'garden',
                'fillColor': '#047857',
                'outlineColor': '#10b981',
                'description': 'Landscaped botanical lawn and palm courtyard.'
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': [coords]
            }
        })
    # Student Square
    elif wid == '1538932918':
        grounds_features.append({
            'type': 'Feature',
            'id': 'student-square',
            'properties': {
                'id': 'student-square',
                'name': 'Student Square Plaza',
                'type': 'plaza',
                'fillColor': '#1e293b',
                'outlineColor': '#38bdf8',
                'description': 'Paved outdoor gathering plaza under tree canopies.'
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': [coords]
            }
        })
    # Concrete Parking
    elif tags.get('amenity') == 'parking':
        grounds_features.append({
            'type': 'Feature',
            'id': f'parking-{wid}',
            'properties': {
                'id': f'parking-{wid}',
                'name': 'Campus Parking Surface',
                'type': 'parking',
                'fillColor': '#1e293b',
                'outlineColor': '#475569',
                'description': 'Paved concrete parking lot.'
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': [coords]
            }
        })

print(f"Extracted {len(grounds_features)} sports grounds and campus plazas")

# 4. Extract Real Roads and Walkways
highways_features = []
for w in root.findall('way'):
    tags = {t.get('k'): t.get('v') for t in w.findall('tag')}
    if 'highway' not in tags:
        continue
    wid = w.get('id')
    hw = tags.get('highway')
    name = tags.get('name', '')
    refs = [nd.get('ref') for nd in w.findall('nd')]
    coords = [list(nodes[r]) for r in refs if r in nodes]
    if len(coords) < 2:
        continue
        
    is_footway = hw in ['footway', 'path', 'pedestrian', 'steps']
    is_trunk = hw in ['trunk', 'primary']
    
    highways_features.append({
        'type': 'Feature',
        'id': f'hw-{wid}',
        'properties': {
            'id': f'hw-{wid}',
            'name': name or ('Pedestrian Walkway' if is_footway else 'Campus Driveway'),
            'type': 'pedestrian_walkway' if is_footway else ('trunk_highway' if is_trunk else 'campus_road'),
            'width': 3.5 if is_footway else (8 if is_trunk else 5.5)
        },
        'geometry': {
            'type': 'LineString',
            'coordinates': coords
        }
    })

print(f"Extracted {len(highways_features)} real highway and footway lines")

# Save processed GeoJSON datasets
with open('src/data/sjec_real_buildings.json', 'w', encoding='utf-8') as f:
    json.dump({'type': 'FeatureCollection', 'features': buildings_features}, f, indent=2)

with open('src/data/sjec_real_grounds.json', 'w', encoding='utf-8') as f:
    json.dump({'type': 'FeatureCollection', 'features': grounds_features}, f, indent=2)

with open('src/data/sjec_real_highways.json', 'w', encoding='utf-8') as f:
    json.dump({'type': 'FeatureCollection', 'features': highways_features}, f, indent=2)

with open('src/data/sjec_real_boundary.json', 'w', encoding='utf-8') as f:
    json.dump({'type': 'FeatureCollection', 'features': [{
        'type': 'Feature',
        'properties': {'name': "Saint Joseph's Engineering College Boundary"},
        'geometry': {'type': 'Polygon', 'coordinates': [boundary_coords]}
    }]}, f, indent=2)

print("All GeoJSON files generated successfully!")
