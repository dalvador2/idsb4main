from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import cryptography
import sqlite3 as sqlite
import os

def genhashsalt(password):
    salt = os.urandom(16)
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
    )
    password = bytes(password, encoding="utf8")
    hash = kdf.derive(password)
    return salt, hash

def verify(salt, hash, password):
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
    )
    password = bytes(password, encoding="utf8")
    correct = True
    try:
        kdf.verify(password, hash)
    except cryptography.exceptions.InvalidKey:
        correct = False
    return correct


print(genhashsalt(input("password")))