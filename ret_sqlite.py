import sqlite3 as lite
import pandas as pd

con = lite.connect('getting_started.db')

with con:

    cur = con.cursor()
    cur.execute("SELECT * FROM cities")

    rows = cur.fetchall()
    cols = [desc[0] for desc in cur.description]
    df = pd.DataFrame(rows)

    for col in cols:
        print col
        
    for row in rows:
        print row
