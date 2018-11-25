from flask import Flask, jsonify
from flask_cors import CORS

from models.sbb_station_parking import SBBStationParking
from models.sbb_lines import TransportOpenData
from models.sbb_parking_availability import ParkingAvailability
from utils.distance import compute_route

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return jsonify(SBBStationParking.get_info_for_station(4100))


@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(SBBStationParking.get_data())


@app.route('/geo/stations', methods=['GET'])
def get_geo_stations():
    # Return all the stations contained in the data
    return jsonify(SBBStationParking.get_geo_info_for_all_stations())


@app.route('/stations', methods=['GET'])
def get_stations():
    # Return all the stations contained in the data
    return jsonify(SBBStationParking.get_info_for_all_stations())


@app.route('/station/<int:didok>', methods=['GET'])
def get_station(didok):
    # Return the station with the corresponding didok
    return jsonify(SBBStationParking.get_info_for_station(didok))


@app.route('/route/start/<string:start>/end/<string:end>', methods=['GET'])
def get_route(start, end):
    # Return the route between two stations
    # Return the cost between two stations
    transporter = TransportOpenData(start, end)
    cost_dict = {'cost': transporter.get_cost()}
    geo_dict = transporter.get_geo_json()
    return jsonify({ **cost_dict, **geo_dict })


@app.route('/find-stations/lat/<string:lat>/lon/<string:lon>', methods=['GET'])
def get_closest_stations(lat, lon):
    # Return the closest 10 stations based on the location passed
    return jsonify(SBBStationParking.get_closest_stations(float(lat), float(lon)))


@app.route('/find-available-stations/lat/<string:lat>/lon/<string:lon>', methods=['GET'])
def get_closest_stations_with_availability(lat, lon):
    # Return the closest 10 stations based on the location passed
    stations = SBBStationParking.get_closest_stations(float(lat), float(lon))

    station_names = []
    for station in stations:
        station_name = station['station_name']
        station_names.append(station_name)

    parking_inspector = ParkingAvailability()
    availabilities = parking_inspector.get_stations_availability(station_names)

    for i, station in enumerate(stations):
        availability = availabilities[i]
        station['station']['available_spots'] = availability

    return jsonify(stations)


@app.route('/get-possible-routes/v1/lat/<string:lat>/lon/<string:lon>/destination/<string:destination>',
           methods=['GET'])
def get_possible_routes(lat, lon, destination):
    # Return the closest 10 stations based on the location passed
    closest_stations = SBBStationParking.get_closest_stations(float(lat), float(lon))
    routes = []

    for station in closest_stations:
        station_name = station['station']['station_name']
        transporter = TransportOpenData(station_name, destination)
        route = compute_route(transporter, station)
        if not route:
            continue

        routes.append(route)

    routes = sorted(routes, key=lambda x: x['total_cost'])

    return jsonify(routes)


if __name__ == '__main__':
    app.run(debug=True)
