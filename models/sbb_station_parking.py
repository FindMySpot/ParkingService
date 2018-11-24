import json

data = None

with open('data/station-parking.json', 'r') as json_data:
    data = json.load(json_data)

def get_data():
    return data