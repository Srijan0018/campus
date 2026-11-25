import xml.etree.ElementTree as ET
import json

tree = ET.parse('sjec_real_osm.osm')
root = tree.getroot()

nodes = {}
for n in root.findall('node'):
    nid = n.attrib['id']
    lat = float(n.attrib['lat'])
    lon = float(n.attrib['lon'])
    nodes[nid] = (lon, lat)

def get_way_coords(elem):
    nd_refs = [nd.attrib['ref'] for nd in elem.findall('nd')]
    return [nodes[ref] for ref in nd_refs if ref in nodes]

print("=== CHECKING ALL WAYS NEAR ADMIN & AB 1 ===")
# Admin Block is at (74.898694, 12.910723)
for w in root.findall('way'):
    wid = w.attrib['id']
    tags = {t.attrib['k']: t.attrib['v'] for t in w.findall('tag')}
    coords = get_way_coords(w)
    if not coords:
        continue
    cx = sum(c[0] for c in coords) / len(coords)
    cy = sum(c[1] for c in coords) / len(coords)
    if 74.8980 <= cx <= 74.8995 and 12.9098 <= cy <= 12.9115:
        print(f"Way {wid}: name={tags.get('name')} | building={tags.get('building')} | leisure={tags.get('leisure')} | amenity={tags.get('amenity')} | cx={cx:.6f}, cy={cy:.6f} | pts={len(coords)} | all_tags={tags}")
