from datetime import datetime, timedelta
import sqlite3
from random import gauss
house = 2
INSERT_COMMAND = "INSERT INTO usage values (?,?,?,?)"
ts = datetime.now()-timedelta(100)
with sqlite3.connect("isdp4.db") as conn:
    for i in range(100):
        tc = ts + timedelta(i)
        usage = gauss(mu=28, sigma=8)
        generation = gauss(mu=3,sigma=0.4)
        cur = conn.cursor()
        cur.execute(INSERT_COMMAND,(tc,usage,generation,house))
    conn.commit()
