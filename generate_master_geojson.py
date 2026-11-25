import xml.etree.ElementTree as ET
import json
import math

tree = ET.parse('sjec_real_osm.osm')
root = tree.getroot()

# Load all nodes
nodes = {}
for n in root.findall('node'):
    nid = n.attrib['id']
    nodes[nid] = [float(n.attrib['lon']), float(n.attrib['lat'])]

# Load all ways
ways = {}
for w in root.findall('way'):
    wid = w.attrib['id']
    tags = {t.attrib['k']: t.attrib['v'] for t in w.findall('tag')}
    nd_refs = [nd.attrib['ref'] for nd in w.findall('nd')]
    coords = [nodes[ref] for ref in nd_refs if ref in nodes]
    ways[wid] = {
        'id': wid,
        'tags': tags,
        'nd_refs': nd_refs,
        'coords': coords
    }

print(f"Loaded {len(nodes)} nodes and {len(ways)} ways.")

# 1. BUILD ACCURATE BUILDINGS GEOJSON
# We need:
# - AB 1 (Relation 21097281: outer way 1538919052, inner 1538919032)
# - Admin Block (Way 1537952351)
# - AB 2 (Way 1537949013)
# - AB 3 (Way 1537942437)
# - AB 4 / Civil Dept (Way 1537951217)
# - Civil Block South (Way 1537949097)
# - Mechanical Workshop (Way 1538919037)
# - Mechanical & Academic Complex (Way 1537948656)
# - Saint Pio Chapel (Way 1537941341)
# - Saint Joseph Gents Hostel (Way 1537940526)
# - Saint Joseph Girls Hostel (Way 1537942615)
# - Central Canteen & Food Court (Way 1538919048)
# - Bethania House (Way 1537925229)
# - Guest House (Way 1537925232)
# - Main Gatehouse (Way 1537948657)
# - Scholars Residence A (Way 1538919056)
# - Scholars Residence B (Way 1538919066)
# - North Utilities (Way 1533207274, 1533207275)

# Detailed metadata for each verified building
BUILDING_METADATA = {
    'rel-21097281': {
        'id': 'bldg-ab1',
        'osm_id': 'rel-21097281',
        'name': 'Academic Block I (AB-I)',
        'short_code': 'AB-I',
        'category': 'academic',
        'levels': 4,
        'height': 16,
        'base_height': 0,
        'color': '#0284c7', # Sky Blue
        'roof_color': '#b91c1c', # Terracotta Red Gable
        'roof_shape': 'gabled',
        'photo': 'https:#images.shiksha.com/mediadata/images/1501133097phpxoZBkv.jpeg',
        'summary': 'Core undergraduate academic wing featuring dual inner courtyards. Houses the Department of Electrical & Electronics Engineering (EEE), basic sciences, and the renowned Fr Fred Memorial Hall.',
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
        'height': 16,
        'base_height': 0,
        'color': '#0d9488', # Teal Emerald
        'roof_color': '#991b1b', # Pyramidal Red
        'roof_shape': 'pyramidal',
        'photo': 'https:#www.eduska.com/assets/user_photo/9a31daf7134d1fef9f6069fa4b2244f6.jpg',
        'summary': 'The institutional headquarters of SJEC. First building greeting visitors from the entrance boulevard, with a grand portico and administrative services.',
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
        'height': 24,
        'base_height': 0,
        'color': '#06b6d4', # Bright Cyan
        'roof_color': '#b91c1c', # Red Gabled
        'roof_shape': 'gabled',
        'photo': 'https:#images.shiksha.com/mediadata/images/1501133097phpxoZBkv.jpeg',
        'summary': 'Major computing and information hub housing CSE, ISE, MCA, the Central Library, the Central Computer Centre (CCC) in the basement, and the 1,000-seat Kalam Auditorium.',
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
        'height': 34,
        'base_height': 0,
        'color': '#3b82f6', # Cobalt Blue
        'roof_color': '#1e3a8a', # Dark Solar Blue Flat Roof
        'roof_shape': 'flat',
        'photo': 'https:#www.sjec.ac.in/images/slider/campus-life.jpg',
        'summary': 'The tallest block on campus (9 storeys, 34m) with modern stepped L-architecture. Features Spoorthi Conference Hall on the 7th floor, Prerana Hall on ground floor, ECE, MBA, and the 300 kWp rooftop solar plant.',
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
        'height': 20,
        'base_height': 0,
        'color': '#8b5cf6', # Purple/Violet
        'roof_color': '#dc2626', # Red Gabled
        'roof_shape': 'gabled',
        'photo': 'https:#www.sjec.ac.in/images/departments/civil-engineering.jpg',
        'summary': 'Dedicated Civil Engineering complex housing design studios, material testing labs, CAD facilities, and the Bishop Aloysius Paul Hall for conferences.',
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
        'height': 12,
        'base_height': 0,
        'color': '#a855f7',
        'roof_color': '#991b1b',
        'roof_shape': 'gabled',
        'photo': '',
        'summary': 'Southern Civil engineering extension housing environmental testing, water resources, and surveying yards.',
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
        'height': 10,
        'base_height': 0,
        'color': '#10b981', # Emerald green
        'roof_color': '#15803d', # Green metal roof
        'roof_shape': 'gabled',
        'photo': '',
        'summary': 'Heavy industrial workshop with gabled green metal roof, overhead crane bays, CNC machine tools, and fabrication cells.',
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
        'height': 18,
        'base_height': 0,
        'color': '#f59e0b', # Amber
        'roof_color': '#b91c1c', # Red Hipped
        'roof_shape': 'hipped',
        'photo': '',
        'summary': '5-storey building with classic white facade and red hipped roof housing Mechanical Engineering lecture halls, CAMD labs, and faculty offices.',
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
        'height': 16,
        'base_height': 0,
        'color': '#eab308', # Warm Golden Yellow
        'roof_color': '#a16207', # Warm Amber
        'roof_shape': 'cruciform',
        'photo': 'https:#www.sjec.ac.in/images/amenities/chapel.jpg',
        'summary': 'The iconic spiritual sanctuary of the college. Distinctive cruciform church architecture surrounded by serene prayer gardens and lit courtyards.',
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
        'height': 28,
        'base_height': 0,
        'color': '#6366f1', # Indigo
        'roof_color': '#4338ca', # Indigo/Red
        'roof_shape': 'terraced',
        'photo': 'https:#www.sjec.ac.in/images/amenities/gents-hostel.jpg',
        'summary': 'Multi-wing residential complex on the northeastern slope providing single and shared accommodations for ~600 male students.',
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
        'height': 18,
        'base_height': 0,
        'color': '#ec4899', # Pink
        'roof_color': '#be185d',
        'roof_shape': 'gabled',
        'photo': 'https:#www.sjec.ac.in/images/amenities/ladies-hostel.jpg',
        'summary': 'Secure residential haven in the southern campus perimeter, featuring modern AC accommodation blocks, separate dining halls, and garden grounds.',
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
        'height': 9,
        'base_height': 0,
        'color': '#f97316', # Orange
        'roof_color': '#c2410c',
        'roof_shape': 'gabled',
        'photo': 'https:#www.sjec.ac.in/images/amenities/canteen.jpg',
        'summary': 'Multi-cuisine campus dining hub with indoor seating, fast-food stalls, fresh juices, and outdoor shaded tables beside Josarena.',
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
        'height': 12,
        'base_height': 0,
        'color': '#64748b',
        'roof_color': '#475569',
        'roof_shape': 'flat',
        'photo': '',
        'summary': 'Administrative and clerical residence for resident directors, campus priests, and institutional authorities.',
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
        'height': 11,
        'base_height': 0,
        'color': '#78716c',
        'roof_color': '#57534e',
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
        'height': 5,
        'base_height': 0,
        'color': '#475569',
        'roof_color': '#334155',
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
        'height': 4,
        'base_height': 0,
        'color': '#334155',
        'roof_color': '#991b1b',
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
        'height': 12,
        'base_height': 0,
        'color': '#64748b',
        'roof_color': '#78716c',
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
        'height': 12,
        'base_height': 0,
        'color': '#64748b',
        'roof_color': '#78716c',
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
        'height': 5,
        'base_height': 0,
        'color': '#475569',
        'roof_color': '#334155',
        'roof_shape': 'flat',
        'photo': '',
        'summary': 'Houses 11 kV transformers, high-capacity diesel generators (500 kVA), and central automatic transfer switches ensuring 24/7 uninterrupted campus power.',
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
        'height': 5,
        'base_height': 0,
        'color': '#475569',
        'roof_color': '#334155',
        'roof_shape': 'flat',
        'photo': '',
        'summary': 'Base for campus civil maintenance, plumbing, electrical stores, and estate upkeep equipment.',
        'departments': ['Estate Office & Maintenance'],
        'facilities': ['Civil Maintenance Stores', 'Plumbing & Hardware Depot'],
        'accessibility': 'Ground level entry'
    }
}

# Construct features list
features = []

# 1. Add Relation 21097281 (Academic Block 1 — AB 1)
# Outer way: 1538919052, Inner way: 1538919032
outer_coords = ways['1538919052']['coords']
inner_coords = ways['1538919032']['coords']
# Ensure closed
if outer_coords[0] != outer_coords[-1]:
    outer_coords.append(outer_coords[0])
if inner_coords[0] != inner_coords[-1]:
    inner_coords.append(inner_coords[0])

ab1_meta = BUILDING_METADATA['rel-21097281']
features.append({
    'type': 'Feature',
    'id': ab1_meta['id'],
    'properties': {
        **ab1_meta
    },
    'geometry': {
        'type': 'Polygon',
        'coordinates': [outer_coords, inner_coords]
    }
})

# 2. Add all other buildings from ways
for wid, meta in BUILDING_METADATA.items():
    if wid.startswith('rel-'):
        continue
    if wid not in ways:
        print(f"Warning: Way {wid} not found in OSM data")
        continue
    w_coords = ways[wid]['coords']
    if not w_coords:
        continue
    if w_coords[0] != w_coords[-1]:
        w_coords.append(w_coords[0])
    features.append({
        'type': 'Feature',
        'id': meta['id'],
        'properties': {
            **meta
        },
        'geometry': {
            'type': 'Polygon',
            'coordinates': [w_coords]
        }
    })

print(f"Generated {len(features)} verified buildings.")

# Save to sjec_real_buildings.json
buildings_fc = {
    'type': 'FeatureCollection',
    'features': features
}
with open('src/data/sjec_real_buildings.json', 'w') as f:
    json.dump(buildings_fc, f, indent=2)
print("Saved src/data/sjec_real_buildings.json")

