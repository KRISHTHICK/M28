
# This script initializes the SQLite database with some example data
import sqlite3

conn = sqlite3.connect('carbon_emissions.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS emissions (product TEXT, emission REAL)''')
c.execute('INSERT INTO emissions (product, emission) VALUES (?, ?)', ('laptop', 50.0))
conn.commit()
conn.close()
