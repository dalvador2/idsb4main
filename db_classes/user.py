import sqlite3
from .house import House
from .crypt_lib import PassFunc

class User:
    DBNAME = "isdp4.db"

    @classmethod
    def get_from_db(cls,uname):
        with sqlite3.connect(House.DBNAME) as conn:
            curr = conn.cursor()
            curr.execute(f"SELECT * FROM users WHERE uname='{uname}'")
            values = curr.fetchone()
            conn.commit()
        retcls = cls(*values[1:])
        retcls.user_id = values[0]
        return retcls
    
    @classmethod
    def gen_from_password(cls,uname,password, house_id):
        salt, passhash = PassFunc.genhashsalt(password)
        del password
        return cls(uname, salt, passhash, house_id)
    

    def __init__(self,uname, salt, passhash, house_id) -> None:
        self.uname = uname
        self.salt = salt
        self.passhash = passhash
        self.house_id = house_id
    
    def get_house(self):
        self.house = House.get_from_db(self.house_id)
    
    def verify_password(self,password):
        return PassFunc.verify(self.salt, self.passhash, password)
    
    def enroll_to_db(self):
        with sqlite3.connect(User.DBNAME) as conn:
            curr = conn.cursor()
            curr.execute("""INSERT INTO users
                        (uname, 
                        salt, 
                        passhash,
                        house_id)
                        VALUES (?,?,?,?)""",(self.uname, self.salt, self.passhash, self.house_id))
            conn.commit()
        