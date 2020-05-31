from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

BLOCK_SIZE = 16


def get_password(filename: str):
    with open(filename, 'rb') as file:
        return file.read(BLOCK_SIZE)


def encrypt(key: bytes, data: bytes):
    cipher = AES.new(key, AES.MODE_CBC)

    return cipher.iv + cipher.encrypt(pad(data, BLOCK_SIZE))


def decrypt(key: bytes, data: bytes):
    iv = data[:BLOCK_SIZE]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    return unpad(cipher.decrypt(data[BLOCK_SIZE:]), BLOCK_SIZE)