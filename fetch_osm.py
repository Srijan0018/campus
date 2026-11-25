import urllib.request
import json
import time

query = """[out:json][timeout:40];
(
  nwr["amenity"="college"](12.905,74.894,12.918,74.908);
  nwr["amenity"="university"](12.905,74.894,12.918,74.908);
  nwr["name"~"Joseph",i](12.905,74.894,12.918,74.908);
  nwr["name"~"SJEC",i](12.905,74.894,12.918,74.908);
  way(12.908,74.895,12.916,74.904);
  node(12.908,74.895,12.916,74.904);
);
out body;
>;
out skel qt;
"""

endpoints = [
    'https://overpass.kumi.systems/api/interpreter',
    'https://overpass.private.coffee/api/interpreter',
    'https://overpass-api.de/api/interpreter',
]

success = False
for ep in endpoints:
    print(f'Trying endpoint: {ep} ...')
    req = urllib.request.Request(
        ep,
        data=query.encode('utf-8'),
        headers={'User-Agent': 'CampusFlow-SJEC-Map/1.0 (sjec.edu research)'}
    )
    try:
        with urllib.request.urlopen(req, timeout=35) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            elements = data.get('elements', [])
            print(f'SUCCESS! Total elements: {len(elements)}')
            with open('sjec_osm_raw.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print('Saved sjec_osm_raw.json')
            success = True
            break
    except Exception as e:
        print(f'Failed on {ep}: {e}')
        time.sleep(1)

if not success:
    print('Trying OSM raw map API...')
    # OSM map API bbox: min_lon,min_lat,max_lon,max_lat
    map_url = 'https://api.openstreetmap.org/api/0.6/map?bbox=74.896,12.909,74.904,12.916'
    req = urllib.request.Request(map_url, headers={'User-Agent': 'CampusFlow-SJEC-Map/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            osm_xml = resp.read().decode('utf-8')
            with open('sjec_osm_raw.osm', 'w', encoding='utf-8') as f:
                f.write(osm_xml)
            print(f'SUCCESS! Saved sjec_osm_raw.osm, length: {len(osm_xml)}')
    except Exception as e:
        print('OSM map API error:', e)
