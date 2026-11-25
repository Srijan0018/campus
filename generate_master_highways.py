import xml.etree.ElementTree as ET
import json

tree = ET.parse('sjec_real_osm.osm')
root = tree.getroot()

nodes = {n.attrib['id']: [float(n.attrib['lon']), float(n.attrib['lat'])] for n in root.findall('node')}

highway_features = []
for w in root.findall('way'):
    wid = w.attrib['id']
    tags = {t.attrib['k']: t.attrib['v'] for t in w.findall('tag')}
    if 'highway' in tags:
        nd_refs = [nd.attrib['ref'] for nd in w.findall('nd')]
        coords = [nodes[ref] for ref in nd_refs if ref in nodes]
        if len(coords) < 2:
            continue
        
        hw_type = tags.get('highway')
        name = tags.get('name') or ('NH 169 Solapur-Mangalore Highway' if hw_type == 'trunk' else 'Campus Access Road')
        surface = tags.get('surface', 'asphalt')
        is_pedestrian = hw_type in ['footway', 'path', 'pedestrian', 'steps'] or tags.get('smoothness') == 'good' and surface == 'paving_stones'
        
        highway_features.append({
            'type': 'Feature',
            'id': f'hw-{wid}',
            'properties': {
                'id': f'hw-{wid}',
                'osm_id': wid,
                'name': name,
                'highway': hw_type,
                'surface': surface,
                'oneway': tags.get('oneway', 'no'),
                'is_pedestrian': is_pedestrian,
                'is_primary': hw_type in ['trunk', 'residential', 'tertiary']
            },
            'geometry': {
                'type': 'LineString',
                'coordinates': coords
            }
        })

print(f"Generated {len(highway_features)} authentic campus road and walkway lines.")

with open('src/data/sjec_real_highways.json', 'w') as f:
    json.dump({'type': 'FeatureCollection', 'features': highway_features}, f, indent=2)
print("Saved src/data/sjec_real_highways.json")
