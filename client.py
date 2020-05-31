from Crypto import Random
from Crypto.Cipher import AES

from util import get_password, encrypt, decrypt

import socket

HOST, PORT = 'localhost', 31337


class CryptoClient:
    def __init__(self, filename: str):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._filename = filename

    def _get_key(self):
        # EKE algorithm
        client_key = Random.get_random_bytes(16)
        password = get_password(self._filename)
        ciphertext = encrypt(password, client_key)
        print(client_key)
        self.send(ciphertext)

        # Get session key double encrypted
        ciphertext = self.recv(48)
        ciphertext = decrypt(password, ciphertext)
        self._key = decrypt(client_key, ciphertext)
        print(self._key)

        # Check key
        r_a = Random.get_random_bytes(16)
        ciphertext = encrypt(self._key, r_a)
        self.send(ciphertext)
        print('r_a', r_a)

        ciphertext = self.recv(48)
        r_ab = decrypt(self._key, ciphertext)
        if r_ab[:16] != r_a:
            raise ValueError('r_a invalid')

        r_b = r_ab[16:]
        ciphertext = encrypt(self._key, r_b)
        self.send(ciphertext)
        print('r_b', r_b)

    def connect(self, host: str, port: int):
        self.socket.connect((host, port))
        self._get_key()

    def send(self, data: bytes):
        self.socket.sendall(data)

    def recv(self, size: int) -> bytes:
        return self.socket.recv(size)


if __name__ == '__main__':
    client = CryptoClient('./password.txt')
    client.connect(HOST, PORT)
    client.send(b'AAAAAAAAAAAAAAAA\n')
    print(client.recv(2048))