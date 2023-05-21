from flask import Flask, jsonify, request
import sqlite3
import datetime

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# Given a room, return how long it is available from the current time
@app.route("/classroom/<facility_id>", methods=["GET"])
def classroom(facility_id):
    now = datetime.datetime.now()
    dow = now.weekday()
    now_minutes = now.hour * 60 + now.minute
    # Defaults for testing
    # dow = 1
    # now_minutes = 960 # 4pm
    soonest_start = 1440  # 24 * 60
    conn = sqlite3.connect("roomMatrix.db")
    cursor = conn.cursor()
    data = cursor.execute(
        "SELECT start_minutes, end_minutes FROM block WHERE facility_id=? AND day_of_week=?",
        [facility_id, dow],
    )
    for pair in data:
        if pair[0] < now_minutes and pair[1] > now_minutes:
            return f"Classroom in use until {pair[1]//60}:{pair[1]%60}"
        elif pair[0] > now_minutes and pair[0] < soonest_start:
            soonest_start = pair[0]
    return soonest_start - now_minutes


# Given a lat/long and optional page paramter, return closest buildings on that page and their available rooms
@app.route("/closest", methods=["GET"])
def closest():
    """
    Takes 'lat', 'long' as float query parameters. Optional integer 'page' parameter indexed from 0.
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
    latitude = float(args.get("lat"))
    longitude = float(args.get("long"))
    print(f"latitude: {latitude}, longitude: {longitude}")
    page = int(
        args.get("page", 0)
    )  # get page parmeter if it exists or else default to 0

    # Get all the rows from the roomMatrix.db database's building table
    conn = sqlite3.connect("roomMatrix.db")
    cursor = conn.cursor()
    all_buildings = list(cursor.execute("SELECT * FROM building"))

    # store the (page+1)th page of closest 3 buildings from all_buildings in buildings
    closest_buildings = get_closest_by_page(all_buildings, latitude, longitude, page)

    result = []  # final result to be returned

    for building in closest_buildings:
        rooms = cursor.execute(
            "SELECT * FROM classroom WHERE building_number=?", (building[0])
        )
        result_rooms = [{"room": room[0], "availablefor": classroom(room[0])} for room in rooms] # rooms to be added to the final result
        result.append({"building": building[1], "rooms": result_rooms})

    conn.close()

    return jsonify(buildings=result)


def get_closest_by_page(buildings, lat, long, page):
    """
    input: a list of buildings, lat, long, and page number
    returns the (page+1)th page of the list of buildings sorted by euclidian distance from the given lat/long
    each page has 3 buildings
    """
    buildings.sort(
        key=lambda building: euclidian_distance(building[2], building[3], lat, long)
    )
    if (page + 1) * 3 > len(buildings):
        return buildings[page * 3 :]
    return buildings[page * 3 : (page + 1) * 3]


# define euclidian distance between two points
def euclidian_distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


if __name__ == "__main__":
    app.run()
