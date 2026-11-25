import xml.etree.ElementTree as ET

tree = ET.parse('sjec_real_osm.osm')
root = tree.getroot()

for rel in root.findall('relation'):
    rid = rel.attrib['id']
    tags = {t.attrib['k']: t.attrib['v'] for t in rel.findall('tag')}
    members = [(m.attrib['type'], m.attrib['ref'], m.attrib.get('role')) for m in rel.findall('member')]
    print(f"Relation {rid}: tags={tags}, count={len(members)}")
    for m in members:
        print(f"   Member {m[0]} {m[1]} role={m[2]}")
