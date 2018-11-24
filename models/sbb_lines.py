import requests


from utils.distance import compute_distance


class TransportOpenData:

    def __init__(self, start, end):
        self.url = 'http://transport.opendata.ch/v1/connections?from={start}&to={end}'
        self.start = start
        self.end = end
        self.price_per_km = 0.3

    def make_request(self):
        final_url = self.url.format(start=self.start, end=self.end)
        response = requests.get(final_url)

        return response.json()

    def get_distance(self, response):
        if not response['connections']:
            return -1

        connection = response['connections'][0]

        distance = self.get_distance_of_connection(connection['sections'])
        return distance

    def get_distance_of_connection(self, sections):
        total_distance = 0
        for section in sections:
            if not section['journey']:
                continue

            distance = self.get_distance_of_section(section['journey']['passList'])
            total_distance += distance

        return total_distance

    @staticmethod
    def get_distance_of_section(pass_list):
        if not pass_list:
            return -1

        total_distance = 0

        current_coordinates = (pass_list[0]['station']['coordinate']['x'],
                               pass_list[0]['station']['coordinate']['y'])

        for entry in pass_list[1:]:
            next_coordinates = (entry['station']['coordinate']['x'],
                                entry['station']['coordinate']['y'])
            distance = compute_distance(current_coordinates, next_coordinates)
            total_distance += distance

            current_coordinates = next_coordinates

        return total_distance

    def get_cost(self):
        response = self.make_request()
        distance = self.get_distance(response)

        return distance * self.price_per_km


