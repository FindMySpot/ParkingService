import json


class SBBStationParking:

    _data = None

    def __init__(self):
        SBBStationParking._load_data()

    @staticmethod
    def _load_data():
        if SBBStationParking._data is None:
            with open('data/station-parking.json', 'r') as json_data:
                SBBStationParking._data = json.load(json_data)

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
        station_infos = list(filter(lambda x: x["fields"].get("didok", "") == didok, SBBStationParking.get_data()))
        parking_info = list(map(lambda x: SBBStationParking.extract_parking_info(x), station_infos))
        return {
            "didok": didok,
            "coordinates": station_infos[0].get("geometry", {}).get("coordinates", []),
            "parking": parking_info,
        } if len(station_infos) > 0 else {}

    @staticmethod
    def extract_parking_info(station):
        return {
            "parkrail_anzahl": station["fields"].get("parkrail_anzahl", -1),
            "parkrail_preis_tag": station["fields"].get("parkrail_preis_tag", -1),
            "parkrail_preis_monat": station["fields"].get("parkrail_preis_monat", -1),
        }
