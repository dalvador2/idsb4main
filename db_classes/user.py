import sqlite3
from house import House
class User:
    DBNAME = "isdp4.db"

    @classmethod
    def get_from_db(cls,uid):
        with sqlite3.connect(House.DBNAME) as conn:
            curr = conn.cursor()
            curr.execute(f"SELECT * FROM users WHERE uid={int(uid)}")
            values = curr.fetchone()
            conn.commit()
        retcls = cls(*values[1:])
        retcls.house_id = values[0]
        return retcls
    

    def __init__(self,uname, salt, passhash, house_id) -> None:
        self.uname = uname
        self.salt = salt
        self.passhash = passhash
        self.house_id = house_id
    
    def get_house(self):
        self.house = House.get_from_db(self.house_id)
    
    def enroll_to_db(self):
        with sqlite3.connect(User.DBNAME) as conn:
            curr = conn.cursor()
            curr.execute(f"""INSERT INTO users
                        (uname, 
                        salt, 
                        passhash,
                        house_id)
                        VALUES ({self.uname},
                        {self.salt},
                        "{self.passhash}",
                        {self.house_id})""")