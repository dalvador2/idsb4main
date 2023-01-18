import sqlite3
import pandas as pd
from .errors import *

class House:
    DBNAME = "isdp4.db"
    @classmethod
    def get_from_db(cls,house_id = None, house_address = None):
        if house_id is None and house_address is None:
            raise RecordError
        elif house_id is None:
            with sqlite3.connect(House.DBNAME) as conn:
                curr = conn.cursor()
                curr.execute(f"SELECT * FROM houses WHERE address='{house_address}'")
                values = curr.fetchone()
                conn.commit()
        else:
            with sqlite3.connect(House.DBNAME) as conn:
                curr = conn.cursor()
                curr.execute(f"SELECT * FROM houses WHERE house_id={int(house_id)}")
                values = curr.fetchone()
                conn.commit()
        if values is None:
            raise PresenceError
        retcls = cls(*values[1:])
        retcls.house_id = values[0]
        return retcls
    
    def __init__(self,square_meter, occupants, address, level=0, score=0) -> None:
        self.square_meter = square_meter
        self.occupants = occupants
        self.address = address
        self.level = level
        self.score = score
    
    def enroll_into_db(self):
        with sqlite3.connect(House.DBNAME) as conn:
            curr = conn.cursor()
            curr.execute(f"""INSERT INTO houses
                        (square_meter, 
                        occupants, 
                        address,
                        level)
                        VALUES ({self.square_meter},
                        {self.occupants},
                        "{self.address}",
                        {self.level})""")
            conn.commit()
    def get_data(self):
        with sqlite3.connect(House.DBNAME) as conn:
            df = pd.read_sql_query(f"SELECT * FROM usage WHERE house_id={self.house_id}",conn)
            df.set_index("datetime", inplace=True)
            return df


    



if __name__ == "__main__":
    x = House.get_from_db(1)
    y = House(square_meter=4, occupants=1, address="29E Herbert Street",level=0)
    y.enroll_into_db()
