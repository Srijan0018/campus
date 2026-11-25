import json

with open('src/data/sjec_real_buildings.json', 'r') as f:
    bldgs = json.load(f)

roof_parts = []

def inset_polygon(coords, factor=0.8):
    cx = sum(c[0] for c in coords[:-1]) / (len(coords) - 1)
    cy = sum(c[1] for c in coords[:-1]) / (len(coords) - 1)
    new_coords = []
    for c in coords:
        nx = cx + (c[0] - cx) * factor
        ny = cy + (c[1] - cy) * factor
        new_coords.append([round(nx, 7), round(ny, 7)])
    return new_coords, cx, cy

for b in bldgs['features']:
    bid = b['properties']['id']
    name = b['properties']['name']
    poly = b['geometry']['coordinates'][0]
    h = b['properties'].get('height', 15)
    r_color = b['properties'].get('roof_color', '#852b1b')

    if bid == 'bldg-admin':
        # Tier 1 lower hipped roof
        tier1, cx, cy = inset_polygon(poly, 0.90)
        roof_parts.append({
            'type': 'Feature',
            'properties': {
                'id': f'{bid}-roof-tier1',
                'name': f'{name} — Lower Hipped Roof Eaves',
                'building_id': bid,
                'base_height': h - 0.8,
                'height': h + 1.2,
                'roof_color': '#852b1b'
            },
            'geometry': {'type': 'Polygon', 'coordinates': [tier1]}
        })
        # Tier 2 upper lantern clerestory pagoda roof (from user photo media_1795537700260_9fc64388.png)
        tier2, _, _ = inset_polygon(poly, 0.45)
        roof_parts.append({
            'type': 'Feature',
            'properties': {
                'id': f'{bid}-roof-tier2',
                'name': f'{name} — Upper Clerestory Lantern Pagoda',
                'building_id': bid,
                'base_height': h + 1.2,
                'height': h + 3.0,
                'roof_color': '#78350f'
            },
            'geometry': {'type': 'Polygon', 'coordinates': [tier2]}
        })
    elif bid == 'bldg-chapel':
        # Octagonal pyramid roof
        tier1, cx, cy = inset_polygon(poly, 0.88)
        roof_parts.append({
            'type': 'Feature',
            'properties': {
                'id': f'{bid}-octagonal-roof',
                'name': 'Saint Pio Chapel — Octagonal Terracotta Roof',
                'building_id': bid,
                'base_height': h - 0.6,
                'height': h + 2.4,
                'roof_color': '#852b1b'
            },
            'geometry': {'type': 'Polygon', 'coordinates': [tier1]}
        })
        # Soaring Cross Tower (from user photo media_1795538229433_9097ba55.png)
        cross_poly, _, _ = inset_polygon(poly, 0.22)
        roof_parts.append({
            'type': 'Feature',
            'properties': {
                'id': f'{bid}-cross-tower',
                'name': 'Saint Pio Chapel — Concrete Cross Tower',
                'building_id': bid,
                'base_height': h + 2.4,
                'height': h + 5.5,
                'roof_color': '#ffffff'
            },
            'geometry': {'type': 'Polygon', 'coordinates': [cross_poly]}
        })
    elif bid == 'bldg-ab3':
        # 300 kWp rooftop solar array (from user photo media_1795537907737_63e43a1e.jpg)
        solar_poly, _, _ = inset_polygon(poly, 0.82)
        roof_parts.append({
            'type': 'Feature',
            'properties': {
                'id': f'{bid}-solar-array',
                'name': 'AB-III 300 kWp Rooftop Solar Grid Array',
                'building_id': bid,
                'base_height': h - 0.2,
                'height': h + 0.8,
                'roof_color': '#0f172a'
            },
            'geometry': {'type': 'Polygon', 'coordinates': [solar_poly]}
        })
    elif bid == 'bldg-gents-hostel':
        # Boys Hostel Rooftop Penthouse & Elevator Core (from user photo media_1795537804189_cc447159.jpg)
        pent_poly, _, _ = inset_polygon(poly, 0.35)
        roof_parts.append({
            'type': 'Feature',
            'properties': {
                'id': f'{bid}-penthouse',
                'name': 'Boys Hostel Rooftop Elevator Core & Tank',
                'building_id': bid,
                'base_height': h,
                'height': h + 3.2,
                'roof_color': '#80917a'
            },
            'geometry': {'type': 'Polygon', 'coordinates': [pent_poly]}
        })
        gabled_poly, _, _ = inset_polygon(poly, 0.85)
        roof_parts.append({
            'type': 'Feature',
            'properties': {
                'id': f'{bid}-roof-pitched',
                'name': f'{name} — Roof Pitch Wing',
                'building_id': bid,
                'base_height': h - 0.6,
                'height': h + 1.4,
                'roof_color': r_color
            },
            'geometry': {'type': 'Polygon', 'coordinates': [gabled_poly]}
        })
    else:
        gabled_poly, _, _ = inset_polygon(poly, 0.85)
        roof_parts.append({
            'type': 'Feature',
            'properties': {
                'id': f'{bid}-roof-pitched',
                'name': f'{name} — Roof Pitch Wing',
                'building_id': bid,
                'base_height': h - 0.6,
                'height': h + 1.4,
                'roof_color': r_color
            },
            'geometry': {'type': 'Polygon', 'coordinates': [gabled_poly]}
        })

with open('src/data/sjec_real_roof_parts.json', 'w') as f:
    json.dump({'type': 'FeatureCollection', 'features': roof_parts}, f, indent=2)

print(f'Generated {len(roof_parts)} photo-verified roof features.')
