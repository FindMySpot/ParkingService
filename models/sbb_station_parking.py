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
    def get_parking_information_for_station(didok):
        station_carparks = list(filter(lambda x: x["fields"].get("didok", "") == didok, SBBStationParking.get_data()))
        parking_info = list(map(lambda x: {
            "parkrail_anzahl": x["fields"].get("parkrail_anzahl", -1),
            "parkrail_preis_tag": x["fields"].get("parkrail_preis_tag", -1),
            "parkrail_preis_monat": x["fields"].get("parkrail_preis_monat", -1),
        }, station_carparks))
        return {
            "didok": didok,
            "coordinates": station_carparks[0]["geometry"]["coordinates"],
            "parking": parking_info,
        } if len(station_carparks) > 0 else {}
