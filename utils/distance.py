import geopy.distance


def compute_distance(coords_1, coords_2):
    return geopy.distance.vincenty(coords_1, coords_2).km


def get_closest_stations(lat, lon, station_info):
    distances = []
    for didok in station_info:
        station = station_info[didok]
        geometry = station.get('geometry', None)
        if not geometry:
            continue

        coordinates = geometry['coordinates']
        coordinates = (coordinates[1], coordinates[0])
        distance = compute_distance((lat, lon), coordinates)
        distances.append({'distance': distance, 'station': station})

    distances = sorted(distances, key=lambda x: x['distance'])

    # Let's settle here for now
    return distances[:10]
