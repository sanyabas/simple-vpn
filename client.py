from Crypto import Random

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
        self._send(ciphertext)

        # Get session key double encrypted
        ciphertext = self._recv(80)
        ciphertext = decrypt(password, ciphertext)
        self._key = decrypt(client_key, ciphertext)

        # Check key
        r_a = Random.get_random_bytes(16)
        ciphertext = encrypt(self._key, r_a)
        self._send(ciphertext)

        ciphertext = self._recv(64)
        r_ab = decrypt(self._key, ciphertext)
        if r_ab[:16] != r_a:
            raise ValueError('r_a invalid')

        r_b = r_ab[16:]
        ciphertext = encrypt(self._key, r_b)
        self._send(ciphertext)

        print('Secure connection established')

    def connect(self, host: str, port: int):
        self.socket.connect((host, port))
        self._get_key()
        self.socket.settimeout(1)

    def _send(self, data: bytes):
        self.socket.sendall(data)

    def send(self, data: bytes):
        ciphertext = encrypt(self._key, data)
        print('sent', ciphertext)

        self._send(ciphertext)

    def _recv(self, size: int) -> bytes:
        return self.socket.recv(size)

    def recv(self) -> bytes:
        data = b''
        while True:
            try:
                tmp = self._recv(1024)
                if not tmp:
                    break
                data += tmp
            except socket.timeout:
                break

        return data

    def receive(self) -> bytes:
        while True:
            response = self.recv()
            if response:
                return decrypt(self._key, response)

    def close(self):
        self.socket.close()


def communicate(host, port, filename):
    client = CryptoClient(filename)
    client.connect(host, port)
    try:
        while True:
            text = input('>: ')
            client.send(text.encode())
            response = client.receive()
            print(response.decode())
    finally:
        client.close()
        return


if __name__ == '__main__':
    communicate(HOST, PORT, './password.txt')