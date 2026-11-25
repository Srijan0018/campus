import xml.etree.ElementTree as ET

tree = ET.parse('sjec_real_osm.osm')
root = tree.getroot()

nodes = {}
for n in root.findall('node'):
    nid = n.attrib['id']
    lat = float(n.attrib['lat'])
    lon = float(n.attrib['lon'])
    nodes[nid] = (lon, lat)

print(f"Total nodes: {len(nodes)}")

ways_info = []
for w in root.findall('way'):
    wid = w.attrib['id']
    tags = {t.attrib['k']: t.attrib['v'] for t in w.findall('tag')}
    nd_refs = [nd.attrib['ref'] for nd in w.findall('nd')]
    coords = [nodes[ref] for ref in nd_refs if ref in nodes]
    if not coords:
        continue
    cx = sum(c[0] for c in coords) / len(coords)
    cy = sum(c[1] for c in coords) / len(coords)
    ways_info.append({
        'id': wid,
        'tags': tags,
        'centroid': (cx, cy),
        'coords_count': len(coords),
        'coords': coords
    })

print(f"Total ways: {len(ways_info)}")

print("\n--- BUILDINGS AND GROUND FEATURES ---")
for w in ways_info:
    tags = w['tags']
    if 'building' in tags or 'leisure' in tags or 'amenity' in tags:
        print(f"Way {w['id']} | name: {tags.get('name')} | building: {tags.get('building')} | leisure: {tags.get('leisure')} | amenity: {tags.get('amenity')} | centroid: ({w['centroid'][0]:.6f}, {w['centroid'][1]:.6f}) | pts: {w['coords_count']}")
