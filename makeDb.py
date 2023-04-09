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
                     id INTEGER PRIMARY KEY,
                     building_id INTEGER,
                     classroom_number TEXT,
                     FOREIGN KEY(building_id) REFERENCES building(id)
                  )""")
cursor.execute("""CREATE TABLE block
                  (
                     id INTEGER PRIMARY KEY,
                     classroom_id INTEGER,
                     day_of_week INTEGER,
                     start_minutes INTEGER,
                     end_minutes INTEGER,
                     FOREIGN KEY(classroom_id) REFERENCES classroom(id)
                  )""")


building1 = ('Dreese Labs', '279', 40.002300, -83.015877)
cursor.execute("INSERT INTO building VALUES (NULL,?,?,?,?)", building1)
classroom1 = (1, 'DL0369')
cursor.execute("INSERT INTO classroom VALUES (NULL,?,?)", classroom1)
"""
block1 = (1, 1, 100, 150)
block2 = (1, 2, 100, 180)
cursor.execute("INSERT INTO block VALUES (NULL,?,?,?,?)", block1)
cursor.execute("INSERT INTO block VALUES (NULL,?,?,?,?)", block2)
"""
conn.commit()
