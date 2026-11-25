import xml.etree.ElementTree as ET

tree = ET.parse('sjec_real_osm.osm')
root = tree.getroot()

for rel in root.findall('relation'):
    rid = rel.attrib['id']
    tags = {t.attrib['k']: t.attrib['v'] for t in rel.findall('tag')}
    if tags.get('type') == 'multipolygon' or 'building' in tags or 'amenity' in tags or 'leisure' in tags:
        print(f"Relation {rid}: {tags}")
        for m in rel.findall('member'):
            print(f"   Member {m.attrib['type']} {m.attrib['ref']} role={m.attrib.get('role')}")
