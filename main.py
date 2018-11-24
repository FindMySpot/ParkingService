from flask import Flask, jsonify
from models.sbb_station_parking import SBBStationParking

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({'Hello': 'world'})


@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(SBBStationParking.get_data())


@app.route('/stations', methods=['GET'])
def get_stations():
    # Return all the stations contained in the data
    return jsonify({
        'url_accessed': '/stations',
        'params': None
    })


@app.route('/station/<int:didok>', methods=['GET'])
def get_station(didok):
    # Return the station with the corresponding didok
    return jsonify({
        'url_accessed': '/station/<int:didok>',
        'params': didok
    })


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
