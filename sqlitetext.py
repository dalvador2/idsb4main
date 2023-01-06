import sqlite3
import pandas as pd

class House:
    DBNAME = "isdp4.db"
    @classmethod
    def get_from_db(cls,house_id):
        with sqlite3.connect(House.DBNAME) as conn:
            curr = conn.cursor()
            curr.execute(f"SELECT * FROM houses WHERE house_id={int(house_id)}")
            values = curr.fetchone()
            conn.commit()
        retcls = cls(*values[1:])
        retcls.house_id = values[0]
        return retcls
    
    def __init__(self,square_meter, occupants, address, level) -> None:
        self.square_meter = square_meter
        self.occupants = occupants
        self.address = address
        self.level = level
    
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


    




x = House.get_from_db(1)
y = House(square_meter=4, occupants=1, address="29E Herbert Street",level=0)
y.enroll_into_db()
