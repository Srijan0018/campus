import xml.etree.ElementTree as ET

tree = ET.parse('sjec_real_osm.osm')
root = tree.getroot()

nodes = {}
for n in root.findall('node'):
    nid = n.attrib['id']
    nodes[nid] = (float(n.attrib['lon']), float(n.attrib['lat']))

for w in root.findall('way'):
    wid = w.attrib['id']
    tags = {t.attrib['k']: t.attrib['v'] for t in w.findall('tag')}
    if 'building:part' in tags or 'roof:shape' in tags:
        nd_refs = [nd.attrib['ref'] for nd in w.findall('nd')]
        coords = [nodes[ref] for ref in nd_refs if ref in nodes]
        cx = sum(c[0] for c in coords) / len(coords)
        cy = sum(c[1] for c in coords) / len(coords)
        print(f"Way {wid}: part={tags.get('building:part')}, roof={tags.get('roof:shape')}, colour={tags.get('roof:colour')}, cx={cx:.6f}, cy={cy:.6f}, tags={tags}")
