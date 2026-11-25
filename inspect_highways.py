import xml.etree.ElementTree as ET

tree = ET.parse('sjec_real_osm.osm')
root = tree.getroot()

nodes = {}
for n in root.findall('node'):
    nid = n.attrib['id']
    nodes[nid] = (float(n.attrib['lon']), float(n.attrib['lat']))

for w in root.findall('way'):
    tags = {t.attrib['k']: t.attrib['v'] for t in w.findall('tag')}
    if 'highway' in tags:
        nd_refs = [nd.attrib['ref'] for nd in w.findall('nd')]
        coords = [nodes[ref] for ref in nd_refs if ref in nodes]
        cx = sum(c[0] for c in coords) / len(coords)
        cy = sum(c[1] for c in coords) / len(coords)
        print(f"Way {w.attrib['id']}: highway={tags.get('highway')} | name={tags.get('name')} | oneway={tags.get('oneway')} | junction={tags.get('junction')} | cx={cx:.6f}, cy={cy:.6f} | pts={len(coords)} | tags={tags}")
