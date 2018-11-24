from flask import Flask, jsonify
from models.sbb_station_parking import SBBStationParking

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(SBBStationParking.get_data())

if __name__ == '__main__':
    app.run(debug=True)
