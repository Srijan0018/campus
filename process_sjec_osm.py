import xml.etree.ElementTree as ET
import json

tree = ET.parse('sjec_real_osm.osm')
root = tree.getroot()

nodes = {n.get('id'): (float(n.get('lon')), float(n.get('lat'))) for n in root.findall('node')}

boundary_way = None
for w in root.findall('way'):
    if w.get('id') == '279811603':
        refs = [nd.get('ref') for nd in w.findall('nd')]
        boundary_coords = [nodes[r] for r in refs if r in nodes]
        boundary_way = (w.get('id'), boundary_coords)
        break

print(f'SJEC Boundary found with {len(boundary_coords)} vertices.')
min_lon = min(c[0] for c in boundary_coords)
max_lon = max(c[0] for c in boundary_coords)
min_lat = min(c[1] for c in boundary_coords)
max_lat = max(c[1] for c in boundary_coords)
print(f'Bbox: Lon [{min_lon:.6f}, {max_lon:.6f}], Lat [{min_lat:.6f}, {max_lat:.6f}]')

# Check point-in-polygon helper
def point_in_poly(x, y, poly):
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# Classify all ways
sjec_buildings = []
outside_buildings = []
sjec_sports = []
sjec_roads = []

for w in root.findall('way'):
    wid = w.get('id')
    if wid == '279811603':
        continue
    tags = {t.get('k'): t.get('v') for t in w.findall('tag')}
    refs = [nd.get('ref') for nd in w.findall('nd')]
    coords = [nodes[r] for r in refs if r in nodes]
    if not coords:
        continue
    
    clon = sum(c[0] for c in coords) / len(coords)
    clat = sum(c[1] for c in coords) / len(coords)
    
    # Check if inside SJEC or nearby extension
    inside = point_in_poly(clon, clat, boundary_coords)
    
    if 'building' in tags:
        entry = {
            'id': wid,
            'name': tags.get('name', ''),
            'tags': tags,
            'coords': coords,
            'center': [clon, clat],
            'inside': inside
        }
        if inside or 'Academic' in tags.get('name', '') or 'Saint Joseph' in tags.get('name', '') or 'Bethania' in tags.get('name', '') or 'Civil' in tags.get('name', '') or 'Administrative' in tags.get('name', ''):
            sjec_buildings.append(entry)
        else:
            outside_buildings.append(entry)
            
    elif any(k in tags for k in ['leisure', 'sport', 'amenity', 'landuse']):
        sjec_sports.append({
            'id': wid,
            'tags': tags,
            'coords': coords,
            'center': [clon, clat],
            'inside': inside
        })
    elif 'highway' in tags:
        sjec_roads.append({
            'id': wid,
            'tags': tags,
            'coords': coords,
            'inside': inside
        })

print(f'\nSJEC Buildings: {len(sjec_buildings)}')
for b in sjec_buildings:
    print(f"  [{b['id']}] {b['name']} ({b['tags'].get('building:levels', b['tags'].get('building', ''))}) center={b['center']} inside={b['inside']}")

print(f'\nOutside Buildings (to mask out): {len(outside_buildings)}')
for b in outside_buildings[:8]:
    print(f"  [{b['id']}] {b['name']} center={b['center']}")

print(f'\nSJEC Sports/Grounds/Features: {len(sjec_sports)}')
for s in sjec_sports:
    print(f"  [{s['id']}] tags={s['tags']} center={s['center']}")
