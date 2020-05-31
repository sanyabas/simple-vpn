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
        self._send(ciphertext)

        # Get session key double encrypted
        ciphertext = self._recv(80)
        ciphertext = decrypt(password, ciphertext)
        self._key = decrypt(client_key, ciphertext)
        print(self._key)

        # Check key
        r_a = Random.get_random_bytes(16)
        ciphertext = encrypt(self._key, r_a)
        self._send(ciphertext)
        print('r_a', r_a)

        ciphertext = self._recv(64)
        r_ab = decrypt(self._key, ciphertext)
        if r_ab[:16] != r_a:
            raise ValueError('r_a invalid')

        r_b = r_ab[16:]
        ciphertext = encrypt(self._key, r_b)
        self._send(ciphertext)
        print('r_b', r_b)

    def connect(self, host: str, port: int):
        self.socket.connect((host, port))
        self._get_key()

    def _send(self, data: bytes):
        print('sent', data)
        self.socket.sendall(data)

    def send(self, data: bytes):
        ciphertext = encrypt(self._key, data)

        self._send(ciphertext)

    def _recv(self, size: int) -> bytes:
        return self.socket.recv(size)

    def recv(self) -> bytes:
        data = b''
        while True:
            tmp = self._recv(1024)
            if not tmp:
                break
            data += tmp

        return data


if __name__ == '__main__':
    client = CryptoClient('./password.txt')
    client.connect(HOST, PORT)
    client.send(b'AAAAAAAAAAAAAAAAAAAAa\n')
    print(client.recv())