from datetime import datetime, timedelta
import sqlite3
from random import gauss
def data_gen(house_id):
    INSERT_COMMAND = "INSERT INTO usage values (?,?,?,?)"
    ts = datetime.now()-timedelta(100)
    u_mu = gauss(mu=28, sigma=8)
    g_mu = gauss(mu=5,sigma = 0.4)
    with sqlite3.connect("isdp4.db") as conn:
        for i in range(100):
            tc = ts + timedelta(i)
            usage = gauss(mu=u_mu, sigma=8)
            generation = gauss(mu=g_mu,sigma=0.4)
            cur = conn.cursor()
            cur.execute(INSERT_COMMAND,(tc,usage,generation,house_id))
        conn.commit()
