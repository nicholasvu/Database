import sqlite3 as lite
import pandas as pd
import pandas.io.sql as psql

con = lite.connect('getting_started.db')
cur = con.cursor()

populate_cities = """
insert into cities (name, state) values
    ('New York City', 'NY'),
    ('Boston', 'MA'),
    ('Chicago', 'IL'),
    ('Miami', 'FL'),
    ('Dallas', 'TX'),
    ('Seattle', 'WA'),
    ('Portland', 'OR'),
    ('San Francisco', 'CA'),
    ('Los Angeles', 'CA');
"""

populate_weather = """
INSERT INTO weather (city,year,warm_month,cold_month,average_high) VALUES
    ('New York City',2013,'July','January',62),
    ('Boston',2013,'July','January',59),
    ('Chicago',2013,'July','January',59),
    ('Miami',2013,'August','January',84),
    ('Dallas',2013,'July','January',77),
    ('Seattle',2013,'July','January',61),
    ('Portland',2013,'July','December',63),
    ('San Francisco',2013,'September','December',64),
    ('Los Angeles',2013,'September','December',75);
"""

cur.execute("DROP TABLE IF EXISTS cities")
cur.execute("CREATE TABLE cities (name text, state text)")
cur.execute("DROP TABLE IF EXISTS weather")
cur.execute("CREATE TABLE weather (city text,year integer,warm_month text,cold_month text,average_high integer)")

cur.execute(populate_weather)
cur.execute(populate_cities)

query_cities = "select * from cities"
cities = pd.read_sql(query_cities,con)

query_weather = "select * from weather"
weather = pd.read_sql(query_weather,con)
weather["name"] = weather["city"]
weather.drop('city', axis=1, inplace=True)

combined = pd.DataFrame.merge(cities,weather, how='inner', left_on = 'name', right_on = 'name')

combined_july = combined[combined['warm_month'] == 'July']

together = combined_july.apply(lambda x:'%s, %s' % (x['name'],x['state']),axis=1)
print "cities that are warmest in July are:", ', '.join(together.tolist())

year = 2013
