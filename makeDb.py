import sqlite3

conn = sqlite3.connect('roomMatrix.db')
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")
cursor.execute("""CREATE TABLE building
                  (
                     id INTEGER PRIMARY KEY,
                     name TEXT,
                     building_number TEXT,
                     latitude REAL,
                     longitude REAL
                  )""")
cursor.execute("""CREATE TABLE classroom
                  (
                     facility_id TEXT PRIMARY KEY,
                     building_id INTEGER,
                     FOREIGN KEY(building_id) REFERENCES building(id)
                  )""")
cursor.execute("""CREATE TABLE block
                  (
                     facility_id TEXT,
                     day_of_week INTEGER,
                     start_minutes INTEGER,
                     end_minutes INTEGER,
                     FOREIGN KEY(facility_id) REFERENCES classroom(facility_id)
                  )""")


# https://www.latlong.net/convert-address-to-lat-long.html
building1 = ('Dreese Labs', '279', 40.002300, -83.015877)
cursor.execute("INSERT INTO building VALUES (NULL,?,?,?,?)", building1)
classroom1 = ('DL0369', 1)
classroom2 = ('DL0357', 1)
cursor.execute("INSERT INTO classroom VALUES (?,?)", classroom1)
cursor.execute("INSERT INTO classroom VALUES (?,?)", classroom2)
"""
block1 = ('DL0369', 1, 100, 150)
block2 = ('DL0369', 2, 100, 180)
cursor.execute("INSERT INTO block VALUES (NULL,?,?,?,?)", block1)
cursor.execute("INSERT INTO block VALUES (NULL,?,?,?,?)", block2)
"""
conn.commit()
