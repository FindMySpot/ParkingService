from flask import Flask, jsonify
from models.sbb_station_parking import SBBStationParking

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify(SBBStationParking.get_parking_information_for_station(3004))


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
    return jsonify(SBBStationParking.get_parking_information_for_station(didok))


@app.route('/route/start/<int:didok_start>/end/<int:didok_end>', methods=['GET'])
def get_route(didok_start, didok_end):
    # Return the route between two stations
    return jsonify({
        'url_accessed': '/route/start/<int:didok>/end/<int:didok>',
        'params': [didok_start, didok_end]
    })


@app.route('/find-stations/lat/<string:lat>/lon/<string:lon>', methods=['GET'])
def get_closest_stations(lat, lon):
    # Return the closest 3 stations based on the location passed
    return jsonify({
        'url_accessed': '/find-stations/lat/<string:lat>/lon/<string:lon>',
        'params': [lat, lon]
    })


if __name__ == '__main__':
    app.run(debug=True)
