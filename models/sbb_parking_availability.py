import requests


class ParkingAvailability:

    def __init__(self):
        self.url = 'http://not/yet/filled/mate/availability/{stations}'

    def get_stations_availability(self, stations):
        response = self.make_request(stations)
        availability = self.get_availability(response)

        return availability

    def make_request(self, stations):
        encoded = ""
        for station in stations:
            encoded += station + '#'
        final_url = self.url.format(stations=encoded)
        response = requests.get(final_url)

        return response.json()

    @staticmethod
    def get_availability(response):
        if not response['availability']:
            return -1

        availability = response['availability']
        return availability
