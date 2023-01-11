from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import cryptography
import os

class PassFunc:
    @classmethod
    def genhashsalt(cls,password):
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
    @classmethod
    def verify(cls,salt, hash, password):
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