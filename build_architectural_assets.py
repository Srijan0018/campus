import xml.etree.ElementTree as ET
import json
import math

# Load OSM data
tree = ET.parse('sjec_real_osm.osm')
root = tree.getroot()

nodes = {n.attrib['id']: [float(n.attrib['lon']), float(n.attrib['lat'])] for n in root.findall('node')}
ways = {}
for w in root.findall('way'):
    nd_refs = [nd.attrib['ref'] for nd in w.findall('nd')]
    coords = [nodes[ref] for ref in nd_refs if ref in nodes]
    tags = {t.attrib['k']: t.attrib['v'] for t in w.findall('tag')}
    ways[w.attrib['id']] = {
        'coords': coords,
        'tags': tags
    }

def close_ring(ring):
    if ring and ring[0] != ring[-1]:
        ring.append(ring[0])
    return ring

# ==============================================================================
# 1. AUTHENTIC ARCHITECTURAL BUILDING METADATA
# Wall colors: Real Mangalore off-white/ivory concrete (#f8fafc, #f1f5f9, #e2e8f0)
# Roof colors: Authentic Mangalore clay terracotta tiles (#852b1b, #991b1b)
# Solar: Photovoltaic metallic dark blue (#0f172a, #172554)
# Plinth: Laterite/granite foundation (#1e293b, #334155)
# ==============================================================================

ARCH_BUILDINGS = {
    'rel-21097281': {
        'id': 'bldg-ab1',
        'osm_id': 'rel-21097281',
        'name': 'Academic Block I (AB-I)',
        'short_code': 'AB-I',
        'category': 'academic',
        'levels': 4,
        'height': 16.5,
        'wall_color': '#e2e8f0',     # Off-white / light limestone concrete
        'roof_color': '#852b1b',     # Mangalore red terracotta clay tiles
        'plinth_color': '#334155',   # Coastal laterite stone foundation
        'accent_color': '#0284c7',   # Architectural blue window mullions
        'roof_shape': 'gabled',
        'photo': 'https://upload.wikimedia.org/wikipedia/commons/6/6c/St._Joseph_Engineering_College_Mangaluru.jpg',
        'summary': 'Core undergraduate academic wing with dual inner light-well courtyards. Houses EEE Department, Basic Sciences, and the historic Fr Fred Memorial Hall.',
        'departments': [
            'Electrical & Electronics Engineering (EEE)',
            'Basic Sciences & Mathematics',
            'Humanities & Social Sciences'
        ],
        'facilities': [
            'Fr. Fred Memorial Hall (Basement Assembly Hall)',
            'Analog & Digital Electronics Design Lab',
            'Power Systems & High Voltage Simulation Lab',
            'Electrical Machines & Drives Laboratory',
            'Departmental Reference Library & Reading Room'
        ],
        'accessibility': 'Elevator equipped, ramped north portico, accessible restrooms'
    },
    '1537952351': {
        'id': 'bldg-admin',
        'osm_id': 'way-1537952351',
        'name': 'Administrative Block',
        'short_code': 'ADMIN',
        'category': 'administrative',
        'levels': 4,
        'height': 16.0,
        'wall_color': '#f8fafc',     # Classical pristine ivory facade
        'roof_color': '#852b1b',     # Pyramidal Mangalore clay tile roof
        'plinth_color': '#1e293b',   # Polished dark granite plinth
        'accent_color': '#0d9488',
        'roof_shape': 'pyramidal',
        'photo': 'https://www.eduska.com/assets/user_photo/9a31daf7134d1fef9f6069fa4b2244f6.jpg',
        'summary': 'Institutional headquarters of SJEC. Features a prominent entrance portico overlooking the central roundabout, housing Directorate, Principal, and Admissions.',
        'departments': [
            'Directorate & Governing Board',
            'Principal & Vice-Principal Offices',
            'Admissions & Public Relations',
            'Finance & Accounts Department',
            'Autonomous Examination Center'
        ],
        'facilities': [
            'Director Conference Chamber',
            'Principal Executive Office',
            'Main Admissions & Enrolment Desk',
            'Central Records & Documentation Vault',
            'Academic Council Boardroom'
        ],
        'accessibility': 'Direct wheelchair ramp from visitor parking, central elevator'
    },
    '1537949013': {
        'id': 'bldg-ab2',
        'osm_id': 'way-1537949013',
        'name': 'Academic Block II (AB-II)',
        'short_code': 'AB-II',
        'category': 'academic',
        'levels': 6,
        'height': 24.5,
        'wall_color': '#f1f5f9',     # Clean architectural concrete
        'roof_color': '#991b1b',     # Terracotta red gabled accents with white parapet
        'plinth_color': '#1e293b',   # Granite plinth
        'accent_color': '#06b6d4',
        'roof_shape': 'gabled',
        'photo': 'https://images.shiksha.com/mediadata/images/1501133097phpxoZBkv.jpeg',
        'summary': 'Premier computing sciences hub. Houses CSE, ISE, MCA, Central Library, Central Computer Centre (CCC) in basement, and the 1,000-seat A.P.J. Abdul Kalam Auditorium.',
        'departments': [
            'Computer Science & Engineering (CSE)',
            'Information Science & Engineering (ISE)',
            'Computer Applications (MCA)'
        ],
        'facilities': [
            'A.P.J. Abdul Kalam Auditorium (5th Floor - 1,000 Seats)',
            'Central Computer Centre (CCC - High Speed Gigabit Hub)',
            'Central Library & Digital Information Repository',
            'Advanced AI, ML & Deep Learning GPU Lab',
            'Cybersecurity & Network Forensics Laboratory'
        ],
        'accessibility': 'Dual high-speed passenger elevators, tactile guidance paths'
    },
    '1537942437': {
        'id': 'bldg-ab3',
        'osm_id': 'way-1537942437',
        'name': 'Academic Block III (AB-III)',
        'short_code': 'AB-III',
        'category': 'academic',
        'levels': 9,
        'height': 34.0,              # Tallest 9-storey academic tower
        'wall_color': '#f8fafc',     # Modern white concrete & architectural louvers
        'roof_color': '#0f172a',     # Rooftop 300 kWp Photovoltaic Solar Power Plant
        'plinth_color': '#1e293b',   # Basalt foundation plinth
        'accent_color': '#2563eb',
        'roof_shape': 'flat_solar',
        'photo': 'https://www.sjec.ac.in/images/slider/campus-life.jpg',
        'summary': 'The tallest tower on campus (9 storeys, 34m) with stepped modern architecture. Houses ECE, AI&DS, MBA, Spoorthi Hall (7th floor), Prerana Hall (ground floor), and 300 kWp rooftop solar plant.',
        'departments': [
            'Electronics & Communication Engineering (ECE)',
            'Artificial Intelligence & Data Science (AI&DS)',
            'Business Administration (MBA)'
        ],
        'facilities': [
            'Spoorthi Conference Hall (7th Floor - National Conventions)',
            'Prerana Seminar Hall (Ground Floor - 200 Seats)',
            '300 kWp Rooftop Solar Grid Photovoltaic Array',
            'Robotics & Embedded Systems Research Lab',
            'VLSI & Microelectronics Fabrication Testbench',
            'MBA Interactive Case-Study Studio'
        ],
        'accessibility': 'Dual passenger elevators with battery backup, wide stair cores'
    },
    '1537951217': {
        'id': 'bldg-ab4',
        'osm_id': 'way-1537951217',
        'name': 'Academic Block IV — Department of Civil Engineering',
        'short_code': 'AB-IV',
        'category': 'academic',
        'levels': 5,
        'height': 20.0,
        'wall_color': '#e2e8f0',     # Off-white concrete with brick accents
        'roof_color': '#991b1b',     # Red gabled tile roof
        'plinth_color': '#334155',
        'accent_color': '#9c4221',   # Exposed brickwork tone
        'roof_shape': 'gabled',
        'photo': 'https://www.sjec.ac.in/images/departments/civil-engineering.jpg',
        'summary': 'Civil Engineering block with materials testing labs, CAD studios, and Bishop Aloysius Paul Hall.',
        'departments': [
            'Civil Engineering',
            'Centre for Environmental & Structural Studies'
        ],
        'facilities': [
            'Bishop Aloysius Paul Hall',
            'Computer-Aided Civil Design (CAD) & BIM Laboratory',
            'Strength of Materials & Concrete Testing Lab',
            'Geotechnical & Soil Mechanics Laboratory',
            'Surveying Stores & Total Station Station'
        ],
        'accessibility': 'Passenger elevator, ground floor heavy equipment access'
    },
    '1537949097': {
        'id': 'bldg-civil-south',
        'osm_id': 'way-1537949097',
        'name': 'Civil Block & Environmental Labs',
        'short_code': 'CIVIL-S',
        'category': 'academic',
        'levels': 3,
        'height': 12.0,
        'wall_color': '#cbd5e1',
        'roof_color': '#852b1b',
        'plinth_color': '#334155',
        'accent_color': '#64748b',
        'roof_shape': 'gabled',
        'photo': '',
        'summary': 'Southern Civil engineering extension housing environmental testing and hydraulics flow channels.',
        'departments': ['Civil Engineering Testing Wings'],
        'facilities': ['Environmental Engineering Lab', 'Hydraulics & Fluid Flow Channel'],
        'accessibility': 'Ground level entry'
    },
    '1538919037': {
        'id': 'bldg-mech-workshop',
        'osm_id': 'way-1538919037',
        'name': 'Central Mechanical Workshops (Green Bay)',
        'short_code': 'MECH-W',
        'category': 'academic',
        'levels': 2,
        'height': 9.5,
        'wall_color': '#64748b',     # Industrial gray concrete & brick
        'roof_color': '#14532d',     # Deep forest green corrugated industrial roof
        'plinth_color': '#1e293b',
        'accent_color': '#15803d',
        'roof_shape': 'gabled_metal',
        'photo': '',
        'summary': 'Heavy industrial workshop with gabled green metal roof, overhead crane, CNC machining, and metallurgy furnaces.',
        'departments': ['Mechanical Engineering'],
        'facilities': [
            'CNC Machining & Turning Centre',
            'Machine Shop (Lathes, Shapers, Milling Machines)',
            'Welding & Sheet Metal Fabrication Bay',
            'Foundry & Forging Laboratory'
        ],
        'accessibility': 'Wide industrial roll-up doors, heavy vehicle driveway'
    },
    '1537948656': {
        'id': 'bldg-mech-complex',
        'osm_id': 'way-1537948656',
        'name': 'Mechanical Engineering Department & Faculty Complex',
        'short_code': 'MECH-ENG',
        'category': 'academic',
        'levels': 5,
        'height': 18.5,
        'wall_color': '#f8fafc',     # Crisp white facade (as OSM tag: building:colour=white)
        'roof_color': '#852b1b',     # Red hipped roof (as OSM tag: roof:colour=red, roof:shape=hipped)
        'plinth_color': '#334155',
        'accent_color': '#f59e0b',
        'roof_shape': 'hipped',
        'photo': '',
        'summary': '5-storey building with classic white facade and red hipped roof housing Mechanical Engineering classrooms and CAMD labs.',
        'departments': ['Mechanical Engineering'],
        'facilities': [
            'Computer Aided Mechanical Design (CAMD) Lab',
            'Fluid Mechanics & Hydraulic Machinery Lab',
            'Thermodynamics & Heat Transfer Laboratory',
            'Departmental Seminar Hall & Faculty Cabins'
        ],
        'accessibility': 'Elevator equipped, accessible main lobby'
    },
    '1537941341': {
        'id': 'bldg-chapel',
        'osm_id': 'way-1537941341',
        'name': 'Saint Pio Chapel',
        'short_code': 'CHAPEL',
        'category': 'landmark',
        'levels': 3,
        'height': 16.0,
        'wall_color': '#ffffff',     # Pristine whitewashed church stone
        'roof_color': '#852b1b',     # Traditional Mangalore clay tiled pitch roof
        'plinth_color': '#475569',   # Laterite stone terrace
        'accent_color': '#eab308',   # Golden cross spire & belfry
        'roof_shape': 'cruciform',
        'photo': 'https://www.sjec.ac.in/images/amenities/chapel.jpg',
        'summary': 'The iconic spiritual sanctuary of the college. Distinctive cruciform church architecture surrounded by serene prayer gardens.',
        'departments': ['Campus Ministry & Spiritual Wellness'],
        'facilities': [
            'Central Nave & Sanctuary',
            'Eucharistic Adoration Chapel',
            'Choir Gallery & Pipe Organ Area',
            'Surrounding Meditative Courtyard'
        ],
        'accessibility': 'Ramped side entrance, acoustic induction loop'
    },
    '1537940526': {
        'id': 'bldg-gents-hostel',
        'osm_id': 'way-1537940526',
        'name': 'Saint Joseph Gents Hostel',
        'short_code': 'BOYS-HOSTEL',
        'category': 'hostel',
        'levels': 9,
        'height': 28.0,
        'wall_color': '#e2e8f0',     # Natural warm gray/cream residential tower
        'roof_color': '#852b1b',     # Terracotta red parapet trim
        'plinth_color': '#1e293b',
        'accent_color': '#4f46e5',
        'roof_shape': 'terraced',
        'photo': 'https://www.sjec.ac.in/images/amenities/gents-hostel.jpg',
        'summary': 'Multi-wing residential dormitory on the northeast slope providing accommodation for ~600 male scholars with gym and dining mess.',
        'departments': ['Student Welfare & Residential Living'],
        'facilities': [
            'Air-conditioned and Standard Resident Rooms',
            'Multi-counter Dining Mess & Cafeteria',
            'Hostel Gymnasium & Fitness Club',
            '24/7 Wi-Fi Reading & Study Lounges',
            'Indoor Table Tennis & Recreation Rooms'
        ],
        'accessibility': 'Elevators in main tower, accessible ground rooms'
    },
    '1537942615': {
        'id': 'bldg-girls-hostel',
        'osm_id': 'way-1537942615',
        'name': 'Saint Joseph Girls Hostel (Ladies Residence)',
        'short_code': 'GIRLS-HOSTEL',
        'category': 'hostel',
        'levels': 5,
        'height': 18.0,
        'wall_color': '#f5f5f4',     # Elegant warm off-white / stone beige
        'roof_color': '#852b1b',     # Red Mangalore clay tile gables
        'plinth_color': '#334155',
        'accent_color': '#be185d',
        'roof_shape': 'gabled',
        'photo': 'https://www.sjec.ac.in/images/amenities/ladies-hostel.jpg',
        'summary': 'Secure residential sanctuary in the southern perimeter featuring modern AC blocks and garden grounds.',
        'departments': ['Student Welfare & Residential Living'],
        'facilities': [
            'Modern AC Wing & Deluxe Living Quarters',
            'Hygienic Dining Hall & Bakery Counter',
            'Solar Water Heating & RO Water Plants',
            'Private Badminton Court & Lawn Garden',
            '24/7 Wardens & Security Surveillance'
        ],
        'accessibility': 'Elevator access, secure gated access ramp'
    },
    '1538919048': {
        'id': 'bldg-canteen',
        'osm_id': 'way-1538919048',
        'name': 'Central Canteen & Food Court (The Lassi Corner)',
        'short_code': 'CANTEEN',
        'category': 'amenity',
        'levels': 2,
        'height': 9.0,
        'wall_color': '#78716c',     # Rustic cafe stone & wood trim
        'roof_color': '#852b1b',     # Red gabled metal/tile roof
        'plinth_color': '#292524',
        'accent_color': '#ea580c',
        'roof_shape': 'gabled',
        'photo': 'https://www.sjec.ac.in/images/amenities/canteen.jpg',
        'summary': 'Multi-cuisine campus dining hub with indoor seating, fast-food stalls, fresh juices, and open-air seating beside Josarena.',
        'departments': ['Campus Dining & Catering Services'],
        'facilities': [
            'South Indian & North Indian Meals Counter',
            'The Lassi Corner (Juices, Shakes & Sundaes)',
            'Bakery, Confectionery & Snack Counter',
            'Outdoor Tree-Shaded Veranda Seating'
        ],
        'accessibility': 'Step-free ground floor access'
    },
    '1537925229': {
        'id': 'bldg-bethania',
        'osm_id': 'way-1537925229',
        'name': 'Bethania House',
        'short_code': 'BETHANIA',
        'category': 'administrative',
        'levels': 3,
        'height': 12.0,
        'wall_color': '#f8fafc',
        'roof_color': '#852b1b',
        'plinth_color': '#334155',
        'accent_color': '#475569',
        'roof_shape': 'flat',
        'photo': '',
        'summary': 'Administrative residence for resident directors, campus priests, and institutional authorities.',
        'departments': ['Institutional Management'],
        'facilities': ['Director Chamber', 'Conference Suite', 'Chaplain Quarters'],
        'accessibility': 'Accessible ground floor'
    },
    '1537925232': {
        'id': 'bldg-guesthouse',
        'osm_id': 'way-1537925232',
        'name': 'SJEC Guest House & VIP Suites',
        'short_code': 'GUEST',
        'category': 'amenity',
        'levels': 3,
        'height': 11.0,
        'wall_color': '#f1f5f9',
        'roof_color': '#852b1b',
        'plinth_color': '#334155',
        'accent_color': '#57534e',
        'roof_shape': 'hipped',
        'photo': '',
        'summary': 'Accommodates visiting university dignitaries, NBA/NAAC accreditation teams, corporate placement recruiters, and guest researchers.',
        'departments': ['Hospitality & Public Relations'],
        'facilities': ['Air-conditioned VIP Suites', 'Dining Lounge', 'Meeting Room'],
        'accessibility': 'Ground level entry'
    },
    '1537948657': {
        'id': 'bldg-main-gate',
        'osm_id': 'way-1537948657',
        'name': 'Main Entrance Security Gatehouse',
        'short_code': 'GATE-1',
        'category': 'administrative',
        'levels': 1,
        'height': 5.0,
        'wall_color': '#334155',     # Granite gate pillar
        'roof_color': '#1e293b',     # Dark architectural canopy
        'plinth_color': '#0f172a',
        'accent_color': '#06b6d4',
        'roof_shape': 'flat',
        'photo': '',
        'summary': '24/7 Security checkpoint at the Solapur-Mangalore Highway (NH 169) entrance gate. Automated RFID boom barriers, visitor registry, and bus shelter.',
        'departments': ['Campus Security & Transport Division'],
        'facilities': ['Security Control Station', 'Visitor Pass Desk', 'RFID Vehicle Entry Barrier'],
        'accessibility': 'Direct street-level access'
    },
    '1538919044': {
        'id': 'bldg-parking-pavilion',
        'osm_id': 'way-1538919044',
        'name': 'Central Covered Parking Pavilion',
        'short_code': 'PARK-PAV',
        'category': 'amenity',
        'levels': 1,
        'height': 4.0,
        'wall_color': '#334155',
        'roof_color': '#852b1b',
        'plinth_color': '#1e293b',
        'accent_color': '#475569',
        'roof_shape': 'sloped',
        'photo': '',
        'summary': 'Covered parking pavilion with red metal canopy for faculty vehicles and two-wheelers.',
        'departments': ['Campus Facilities'],
        'facilities': ['Faculty Four-Wheeler Bays', 'Staff Two-Wheeler Covered Rows', 'EV Charging Point'],
        'accessibility': 'Paved ground parking'
    },
    '1538919056': {
        'id': 'bldg-scholars-a',
        'osm_id': 'way-1538919056',
        'name': 'Faculty & Staff Residence A',
        'short_code': 'RES-A',
        'category': 'hostel',
        'levels': 3,
        'height': 12.0,
        'wall_color': '#e2e8f0',
        'roof_color': '#852b1b',
        'plinth_color': '#334155',
        'accent_color': '#64748b',
        'roof_shape': 'gabled',
        'photo': '',
        'summary': 'Staff residential quarters for teaching faculty and campus personnel.',
        'departments': ['Residential Facilities'],
        'facilities': ['Family Living Suites', 'Dedicated Parking'],
        'accessibility': 'Accessible ground suites'
    },
    '1538919066': {
        'id': 'bldg-scholars-b',
        'osm_id': 'way-1538919066',
        'name': 'Faculty & Staff Residence B',
        'short_code': 'RES-B',
        'category': 'hostel',
        'levels': 3,
        'height': 12.0,
        'wall_color': '#e2e8f0',
        'roof_color': '#852b1b',
        'plinth_color': '#334155',
        'accent_color': '#64748b',
        'roof_shape': 'hipped',
        'photo': '',
        'summary': 'Staff residential quarters for campus administrators.',
        'departments': ['Residential Facilities'],
        'facilities': ['Family Living Suites', 'Garden Court'],
        'accessibility': 'Accessible ground suites'
    },
    '1533207274': {
        'id': 'bldg-substation',
        'osm_id': 'way-1533207274',
        'name': 'North Campus Electrical Substation & Backup Power',
        'short_code': 'POWER',
        'category': 'administrative',
        'levels': 1,
        'height': 5.0,
        'wall_color': '#475569',
        'roof_color': '#1e293b',
        'plinth_color': '#0f172a',
        'accent_color': '#f59e0b',
        'roof_shape': 'flat',
        'photo': '',
        'summary': 'Houses 11 kV transformers, high-capacity diesel generators (500 kVA), and central automatic transfer switches.',
        'departments': ['Campus Electrical Maintenance'],
        'facilities': ['11 kV High Tension Transformer', '500 kVA Diesel Generator Sets', 'Power Distribution Panels'],
        'accessibility': 'Restricted utility access'
    },
    '1533207275': {
        'id': 'bldg-depot',
        'osm_id': 'way-1533207275',
        'name': 'North Campus Maintenance Depot',
        'short_code': 'MAINT',
        'category': 'administrative',
        'levels': 1,
        'height': 5.0,
        'wall_color': '#475569',
        'roof_color': '#1e293b',
        'plinth_color': '#0f172a',
        'accent_color': '#64748b',
        'roof_shape': 'flat',
        'photo': '',
        'summary': 'Base for campus civil maintenance, plumbing, electrical stores, and estate upkeep equipment.',
        'departments': ['Estate Office & Maintenance'],
        'facilities': ['Civil Maintenance Stores', 'Plumbing & Hardware Depot'],
        'accessibility': 'Ground level entry'
    }
}

# Generate buildings FeatureCollection
features = []

# Academic Block 1 (AB-1)
ab1_outer = close_ring(ways['1538919052']['coords'])
ab1_inner = close_ring(ways['1538919032']['coords'])
ab1_meta = ARCH_BUILDINGS['rel-21097281']
features.append({
    'type': 'Feature',
    'id': ab1_meta['id'],
    'properties': {
        **ab1_meta,
        'color': ab1_meta['wall_color']
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [ab1_outer, ab1_inner]
    }
})

for wid, meta in ARCH_BUILDINGS.items():
    if wid.startswith('rel-'):
        continue
    if wid not in ways:
        continue
    w_coords = close_ring(ways[wid]['coords'])
    if not w_coords or len(w_coords) < 3:
        continue
    features.append({
        'type': 'Feature',
        'id': meta['id'],
        'properties': {
            **meta,
            'color': meta['wall_color']
        },
        'geometry': {
            'type': 'Polygon',
            'coordinates': [w_coords]
        }
    })

print(f"Generated {len(features)} architectural buildings.")

with open('src/data/sjec_real_buildings.json', 'w') as f:
    json.dump({'type': 'FeatureCollection', 'features': features}, f, indent=2)

# ==============================================================================
# 2. EXTRACT 3D ROOF PARTS & GABLED WINGS FROM REAL OSM DATA
# Way 1538932914, 1538932920, 1538932921, 1538932922, 1538932926, 1538932928, 1538932931 (AB 1 gables)
# Way 1538932911 (AB 2 gable)
# Way 1538919068 (Admin pyramidal roof)
# Way 1538932917 (Civil Block gable)
# Way 1538919035, 1538919067, 1538919077 (Gents hostel roofs)
# Way 1538919064 (Girls hostel gable)
# ==============================================================================

roof_part_features = []
roof_part_ways = [
    ('1538932914', '#852b1b', 16.5, 15.0, 'gabled'),
    ('1538932920', '#852b1b', 16.5, 15.0, 'gabled'),
    ('1538932921', '#852b1b', 16.5, 15.0, 'gabled'),
    ('1538932922', '#852b1b', 16.5, 15.0, 'gabled'),
    ('1538932926', '#852b1b', 16.5, 15.0, 'gabled'),
    ('1538932928', '#852b1b', 16.5, 15.0, 'gabled'),
    ('1538932931', '#852b1b', 16.5, 15.0, 'gabled'),
    ('1538932911', '#852b1b', 24.5, 23.0, 'gabled'),
    ('1538919068', '#852b1b', 16.0, 14.5, 'pyramidal'),
    ('1538932917', '#852b1b', 20.0, 18.5, 'gabled'),
    ('1538919035', '#852b1b', 15.0, 13.5, 'hipped'),
    ('1538919067', '#852b1b', 12.0, 10.5, 'pyramidal'),
    ('1538919077', '#852b1b', 22.0, 20.5, 'gabled'),
    ('1538919064', '#852b1b', 18.0, 16.5, 'gabled')
]

for wid, col, height, base_h, shape in roof_part_ways:
    if wid in ways:
        c = close_ring(ways[wid]['coords'])
        if len(c) >= 3:
            roof_part_features.append({
                'type': 'Feature',
                'id': f'roof-{wid}',
                'properties': {
                    'roof_color': col,
                    'height': height,
                    'base_height': base_h,
                    'shape': shape
                },
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [c]
                }
            })

# Add AB-III Rooftop Solar Grid Array (photovoltaic panels on flat roof of Way 1537942437)
ab3_coords = close_ring(ways['1537942437']['coords'])
ab3_cx = sum(p[0] for p in ab3_coords[:-1]) / (len(ab3_coords)-1)
ab3_cy = sum(p[1] for p in ab3_coords[:-1]) / (len(ab3_coords)-1)

# Scaled inner solar array polygon
solar_polygon = [[ab3_cx + (p[0] - ab3_cx) * 0.88, ab3_cy + (p[1] - ab3_cy) * 0.88] for p in ab3_coords]
roof_part_features.append({
    'type': 'Feature',
    'id': 'solar-ab3',
    'properties': {
        'roof_color': '#0f172a', # Photovoltaic dark blue-black
        'height': 34.4,
        'base_height': 33.8,
        'shape': 'solar_grid'
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [solar_polygon]
    }
})

print(f"Generated {len(roof_part_features)} authentic 3D roof parts & solar arrays.")
with open('src/data/sjec_real_roof_parts.json', 'w') as f:
    json.dump({'type': 'FeatureCollection', 'features': roof_part_features}, f, indent=2)

print("Saved architectural building and roof assets cleanly!")
