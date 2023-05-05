import sqlite3

conn = sqlite3.connect('roomMatrix.db')
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")
cursor.execute("""CREATE TABLE building
                  (
                     building_number TEXT PRIMARY KEY,
                     name TEXT,
                     latitude REAL,
                     longitude REAL
                  )""")
cursor.execute("""CREATE TABLE classroom
                  (
                     facility_id TEXT PRIMARY KEY,
                     building_number TEXT,
                     FOREIGN KEY(building_number) REFERENCES building(building_number)
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
"""
building1 = ('279', 'Dreese Labs', 40.002300, -83.015877)
cursor.execute("INSERT INTO building VALUES (?,?,?,?)", building1)
classroom1 = ('DL0369', '279')
classroom2 = ('DL0357', '279')
cursor.execute("INSERT INTO classroom VALUES (?,?)", classroom1)
cursor.execute("INSERT INTO classroom VALUES (?,?)", classroom2)
block1 = ('DL0369', 1, 100, 150)
block2 = ('DL0369', 2, 100, 180)
cursor.execute("INSERT INTO block VALUES (NULL,?,?,?,?)", block1)
cursor.execute("INSERT INTO block VALUES (NULL,?,?,?,?)", block2)
"""
conn.commit()
