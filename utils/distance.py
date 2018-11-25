import geopy.distance


PRICE_GAS_PER_KM = 0.15
NUMBER_OF_ROUTES = 3


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
        distances.append({
            'distance': distance,
            'station': station,
            'trip_cost': distance * PRICE_GAS_PER_KM
        })

    distances = sorted(distances, key=lambda x: x['distance'])

    # Let's settle here for now
    return distances[:NUMBER_OF_ROUTES]


def compute_route(transporter, station):
    train_cost = transporter.get_cost()
    geo_dict = transporter.get_geo_json()

    drive_cost = station['trip_cost']
    parking_cost = station['station']['parking']['price_per_day']
    occupied_spaces = station['station']['parking']['occupied_spaces']
    parking_spots = station['station']['parking']['parking_spots']

    if parking_spots == occupied_spaces:
        return None

    if not parking_cost:
        parking_cost = 0

    route = {
        'car_route': station,
        'train_route': {
            'cost': train_cost,
            'geo_dict': geo_dict
        },
        'total_cost': train_cost + parking_cost + drive_cost,
        'train_cost': train_cost,
        'parking_cost': parking_cost,
        'drive_cost': drive_cost
    }

    return route
