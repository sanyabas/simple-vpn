from Crypto.Cipher import AES


def get_password(filename: str):
    with open(filename, 'rb') as file:
        return file.read(16)


def encrypt(key: bytes, data: bytes):
    cipher = AES.new(key, AES.MODE_CBC)

    return cipher.iv + cipher.encrypt(data)


def decrypt(key: bytes, data: bytes):
    iv = data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    return cipher.decrypt(data[16:])