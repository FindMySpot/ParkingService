import geopy.distance


def compute_distance(coords_1, coords_2):
    return geopy.distance.vincenty(coords_1, coords_2).km


def get_closest_stations(lat, lon, stations):
    distances = []
    for station in stations:
        distance = compute_distance((lat, lon), station.get_coordinates())
        distances.append((distance, station))

    sorted(distances, key=lambda x: x[0])

    # Let's settle here for now
    return distances[:10]
