import requests


class ParkingAvailability:

    def __init__(self):
        self.url = 'http://not/yet/filled/mate'

    def get_stations_availability(self, stations):
        response = self.make_request(stations)
        availability = self.get_availability(response)

        return availability

    def make_request(self, stations):
        params = {'stations': stations}
        response = requests.get(self.url, params=params)

        return response.json()

    @staticmethod
    def get_availability(response):
        if not response['availability']:
            return -1

        availability = response['availability']
        return availability
