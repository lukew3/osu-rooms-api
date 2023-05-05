from flask import Flask, jsonify
import sqlite3
import datetime

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# Given a room, return how long it is available from the current time
@app.route("/classroom/<facility_id>", methods=['GET'])
def classroom(facility_id):
    now = datetime.datetime.now()
    dow = now.weekday()
    now_minutes = now.hour * 60 + now.minute
    # Defaults for testing
    # dow = 1
    # now_minutes = 960 # 4pm 
    soonest_start = 1440 # 24 * 60
    conn = sqlite3.connect('roomMatrix.db')
    cursor = conn.cursor()
    data = cursor.execute("SELECT start_minutes, end_minutes FROM block WHERE facility_id=? AND day_of_week=?", [facility_id, dow])
    for pair in data:
        if pair[0] < now_minutes and pair[1] > now_minutes:
            return f"Classroom in use until {pair[1]//60}:{pair[1]%60}"
        elif pair[0] > now_minutes and pair[0] < soonest_start:
            soonest_start = pair[0]
    return f"Room available for {soonest_start-now_minutes} minutes"

# Given a lat/long, return 3 closest buildings and their available rooms
@app.route("/closest", methods=['GET'])
def closest():
    """
    Takes 'lat', 'long' as float query parameters. Optional integer 'page' parameter.
    Returns a json list of closest buildings and all available rooms with the amount of time they are available
    returns something like: [
        {
            building: 'Dreese Labs',
            rooms: [
                {
                    'room': 'DL0369',
                    'availablefor': 100
                }]}]
    """
    args = request.args
    latitude = args.get("lat")
    longitude = args.get("longitude")
    buildings = []
    for building in []:
        rooms = []
        for room in []:
            rooms.append({'room': 'roomname', 'availablefor': 100})
        buildings.append({'building': 'buildingname', 'rooms': rooms})
    return jsonify(buildings=buildings)


if __name__ == '__main__':
    app.run()
