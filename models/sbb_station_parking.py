import json

from utils.distance import get_closest_stations


class SBBStationParking:

    _data = None
    _station_info = {}

    def __init__(self):
        SBBStationParking._load_data()

    @staticmethod
    def _load_data():
        if SBBStationParking._data is None:
            with open('data/station-parking.json', 'r') as json_data:
                SBBStationParking._data = json.load(json_data)
                SBBStationParking.create_station_info()

    @staticmethod
    def create_station_info():
        for entry in SBBStationParking._data:
            station_info = {
                'parking': {
                    'parking_spots': entry["fields"].get("parkrail_anzahl", None),
                    'price_per_day': entry["fields"].get("parkrail_preis_tag", None),
                    'price_per_month': entry["fields"].get("parkrail_preis_monat", None)
                },
                'didok': entry['fields']['didok'],
                'geometry': entry.get("geometry", None),
                'station_name': entry["fields"].get("stationsbezeichnung", ""),
                "properties": {
                    "Name": entry["fields"].get("stationsbezeichnung", "")
                }
            }
            if SBBStationParking.is_valid_station_info(station_info):
                SBBStationParking._station_info[entry['fields']['didok']] = station_info

    @staticmethod
    def is_valid_station_info(station_info):
        if not station_info["geometry"]:
            return False
        return True

    @staticmethod
    def get_data():
        SBBStationParking._load_data()
        return SBBStationParking._data

    @staticmethod
    def get_info_for_all_stations():
        didoks = set(map(lambda x: x["fields"]["didok"], SBBStationParking.get_data()))
        return {
            "stations": list(map(lambda x: SBBStationParking.get_info_for_station(x), didoks))
        }

    @staticmethod
    def get_info_for_station(didok):
        return SBBStationParking._station_info.get(didok, {})

    @staticmethod
    def get_geo_info_for_all_stations():
        SBBStationParking._load_data()
        didoks = set(map(lambda x: x["didok"], SBBStationParking._station_info.values()))
        return {
            "type": "FeatureCollection",
            "features": list(map(lambda x: SBBStationParking.get_geo_info_for_station(x), didoks))
        }

    @staticmethod
    def get_geo_info_for_station(didok):
        station_info = SBBStationParking._station_info.get(didok, None)
        if not station_info:
            return {}

        return {
            "type": "Feature",
            "geometry": station_info["geometry"],
            "properties": station_info["properties"],
        }

    @staticmethod
    def get_closest_stations(lat, lon):
        SBBStationParking.get_data()
        distances = get_closest_stations(lat, lon, SBBStationParking._station_info)
        return distances

