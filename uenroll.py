from db_classes import User

uname = input("uname :")
password = input("password :")
house = input("house id:")

x = User.gen_from_password(uname, password,house)
x.enroll_to_db()