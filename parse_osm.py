import xml.etree.ElementTree as ET
import json

tree = ET.parse('sjec_real_osm.osm')
root = tree.getroot()

nodes = {}
node_tags = {}
for n in root.findall('node'):
    nid = n.get('id')
    lat = float(n.get('lat'))
    lon = float(n.get('lon'))
    nodes[nid] = (lon, lat)
    tags = {t.get('k'): t.get('v') for t in n.findall('tag')}
    if tags:
        node_tags[nid] = (tags, (lon, lat))

print(f'Total nodes: {len(nodes)}')

buildings = []
highways = []
campus_boundary = None
other_ways = []

for w in root.findall('way'):
    wid = w.get('id')
    tags = {t.get('k'): t.get('v') for t in w.findall('tag')}
    nd_refs = [nd.get('ref') for nd in w.findall('nd')]
    coords = [nodes[ref] for ref in nd_refs if ref in nodes]
    
    if wid == '279811603' or tags.get('name') == "Saint Joseph's Engineering College":
        campus_boundary = (wid, tags, coords)
    
    if 'building' in tags:
        buildings.append((wid, tags, coords))
    elif 'highway' in tags:
        highways.append((wid, tags, coords))
    else:
        other_ways.append((wid, tags, coords))

print(f'Campus boundary: {campus_boundary is not None}')
if campus_boundary:
    print(f'Campus boundary way id: {campus_boundary[0]} with {len(campus_boundary[2])} nodes')
    print('Campus tags:', campus_boundary[1])

print(f'\nTotal Buildings: {len(buildings)}')
for wid, tags, coords in buildings:
    name = tags.get('name', 'Unnamed')
    levels = tags.get('building:levels', tags.get('levels', 'unknown'))
    b_type = tags.get('building')
    # calculate centroid
    if coords:
        clon = sum(c[0] for c in coords) / len(coords)
        clat = sum(c[1] for c in coords) / len(coords)
        print(f'Building {wid}: name="{name}" b_type={b_type} levels={levels} center=({clon:.6f}, {clat:.6f}) nodes={len(coords)} tags={tags}')

print(f'\nTotal Highways: {len(highways)}')
for wid, tags, coords in highways:
    name = tags.get('name', '')
    hw = tags.get('highway')
    if coords:
        clon = sum(c[0] for c in coords) / len(coords)
        clat = sum(c[1] for c in coords) / len(coords)
        print(f'Highway {wid}: name="{name}" type={hw} center=({clon:.6f}, {clat:.6f}) nodes={len(coords)}')

print(f'\nOther ways (sports, landuse, leisure, etc.):')
for wid, tags, coords in other_ways:
    if any(k in tags for k in ['leisure', 'amenity', 'sport', 'landuse']):
        print(f'Way {wid}: tags={tags} nodes={len(coords)}')

print(f'\nNamed Nodes in OSM:')
for nid, (tags, coord) in node_tags.items():
    if tags.get('name') or tags.get('amenity'):
        print(f'Node {nid}: tags={tags} coord={coord}')
