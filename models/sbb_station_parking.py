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