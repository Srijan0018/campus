import xml.etree.ElementTree as ET

tree = ET.parse('sjec_real_osm.osm')
root = tree.getroot()

print("=== WAYS WITH TAGS ===")
for elem in root.findall('way'):
    tags = {t.attrib['k']: t.attrib['v'] for t in elem.findall('tag')}
    if any(k in tags for k in ['name', 'building', 'amenity', 'leisure', 'shop']):
        print(f"Way {elem.attrib['id']}: name={tags.get('name')} | building={tags.get('building')} | tags={tags}")

print("\n=== NODES WITH TAGS ===")
for elem in root.findall('node'):
    tags = {t.attrib['k']: t.attrib['v'] for t in elem.findall('tag')}
    if len(tags) > 0:
        lat = elem.attrib['lat']
        lon = elem.attrib['lon']
        print(f"Node {elem.attrib['id']} ({lat}, {lon}): tags={tags}")
