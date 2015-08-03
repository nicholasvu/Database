import requests
import pandas as pd
from pandas.io.json import json_normalize
import datetime as dt
import sqlite3 as lite

start_time = dt.datetime.now()
print start_time

r = requests.get('http://citibikenyc.com/stations/json')
o = r.json()['stationBeanList']

# Create a DataFrame object with the second item in the json object
df = pd.DataFrame(o)

con = lite.connect('citi_bike.db')
cur = con.cursor()

with con:
    cur.execute('DROP TABLE IF EXISTS citibike_reference')
    cur.execute('CREATE TABLE citibike_reference(id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )')
sql = 'INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'

with con:
    for station in r.json()['stationBeanList']:
        cur.execute(sql, (station['id'], station['totalDocks'], station['city'], station['altitude'], station['stAddress2'], station['longitude'], station['postalCode'], station['testStation'], station['stAddress1'], station['stationName'], station['landMark'], station['latitude'], station['location']))

# Extract the column from the dataframe and put them into a list.
station_ids = df['id'].tolist()

# Add the '_' to the station names and add the data type for SQLite
station_ids = ['_' + str(x) + ' INT' for x in station_ids]

# Create a table
with con:
    # for this code, I need to drop the already-existing table to run this block of code
    cur.execute('DROP TABLE IF EXISTS available_bikes')
    cur.execute("CREATE TABLE available_bikes (execution_time INT, "  + ", ".join(station_ids) + ");")

import time
from dateutil.parser import parse
import collections

def set_time():
    exec_time = parse(r.json()['executionTime'])

    with con:
        cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))
        id_bikes = collections.defaultdict(int)

        for station in r.json()['stationBeanList']:
            id_bikes[station['id']] = station['availableBikes']

        for k,v in id_bikes.iteritems():
            cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")

            # This code will execute 60 times.
for n in range(60):

    r = requests.get('http://citibikenyc.com/stations/json')
    o = r.json()['stationBeanList']
    df = pd.DataFrame(o)
    with con:
        cur.execute('DROP TABLE IF EXISTS citibike_reference')
        cur.execute('CREATE TABLE citibike_reference(id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )')
    sql = 'INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'

    with con:
        for station in r.json()['stationBeanList']:
            cur.execute(sql, (station['id'], station['totalDocks'], station['city'], station['altitude'], station['stAddress2'], station['longitude'], station['postalCode'], station['testStation'], station['stAddress1'], station['stationName'], station['landMark'], station['latitude'], station['location']))

    # Extract the column from the dataframe and put them into a list.
    station_ids = df['id'].tolist()

    # Add the '_' to the station names and add the data type for SQLite
    station_ids = ['_' + str(x) + ' INT' for x in station_ids]

    set_time()

    # Suspend execution for 1 minute
    if n!= 59:
        time.sleep(60)
        print n + 1, "cycles complete."
    else:
        print "That's enough waiting. We've done this every minute for an hour."
end_time = dt.datetime.now()
print end_time

print "Time elapsed: ", end_time - start_time

# Using a sql query to create a DataFrame
df2 = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time", con, index_col='execution_time')
hour_change = collections.defaultdict(int)

for col in df2.columns:
    station_vals = df2[col].tolist()
    station_id = col[1:] #trim the "_"
    station_change = 0

    for k, v in enumerate(station_vals):
        if k < len(station_vals) - 1:
            station_change += abs(station_vals[k] - station_vals[k+1])

    hour_change[int(station_id)] = station_change #convert the station id back to an integer

def keywithmaxval(d):
    # Create a list of the dict's keys and values
    v = list(d.values())
    k = list(d.keys())

    # list.index(value) will return the index of the value in the list
    return k[v.index(max(v))]

# Assign the max key to the max_station
max_station = keywithmaxval(hour_change)

# Query SQLite for reference information
cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station, ))
data = cur.fetchone()

print "The most active station is station id %s at %s latitude: %s longitude: %s" % data
print "With " + str(hour_change[max_station]) + " bicycles coming and going in the hour between " + dt.datetime.fromtimestamp(int(df2.index[0])).strftime('%Y-%m-%dT%H:%M:%S') + " and " + dt.datetime.fromtimestamp(int(df2.index[-1])).strftime('%Y-%m-%dT%H:%M:%S')

import matplotlib.pyplot as plt

plt.bar(hour_change.keys(), hour_change.values())
plt.show()
