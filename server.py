from flask import Flask
import sqlite3
import datetime

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# Given a room, return how long it is available from the current time
@app.route("/classroom/<facility_id>")
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

if __name__ == '__main__':
    app.run()
