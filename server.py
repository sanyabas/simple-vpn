from Crypto.Random import get_random_bytes

from util import get_password, encrypt, decrypt

import socket


class CryptoHandler:
    def __init__(self, password, connection, address):
        self._password = password
        self._socket = connection
        self._address = address

    def setup(self):
        self._session_key = get_random_bytes(16)
        print(self._session_key)
        ciphertext = self._socket.recv(48)
        client_key = decrypt(self._password, ciphertext)

        ciphertext = encrypt(client_key, self._session_key)
        ciphertext = encrypt(self._password, ciphertext)
        self._socket.sendall(ciphertext)

        ciphertext = self._socket.recv(48)
        r_a = decrypt(self._session_key, ciphertext)
        r_b = get_random_bytes(16)
        ciphertext = encrypt(self._session_key, r_a + r_b)
        self._socket.sendall(ciphertext)
        print('r_a', r_a)
        print('r_b', r_b)

        ciphertext = self._socket.recv(48)
        r_b_received = decrypt(self._session_key, ciphertext)
        if r_b_received != r_b:
            raise ValueError('r_b invalid')

        self._socket.settimeout(0.5)

    def _recv(self) -> bytes:
        data = b''
        while True:
            try:
                tmp = self._socket.recv(1024)
                print('tmp', tmp)
                data += tmp

                if not tmp:
                    break
            except socket.timeout:
                break

        return data

    def handle(self) -> None:
        ciphertext = self._recv()
        if not ciphertext:
            print('no ciphertext')
            return

        data = decrypt(self._session_key, ciphertext)

        print(f'{self._address}: {data}')

        self._socket.sendall(data)


class CryptoServer:
    def __init__(self, address, filename: str):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._address = address
        self._password = get_password(filename)

    def listen(self):
        self.socket.bind(self._address)
        self.socket.listen(1)
        while True:
            conn, addr = self.socket.accept()
            with conn:
                handler = CryptoHandler(self._password, conn, addr)
                handler.setup()
                handler.handle()


def create_server(host: str, port: int, filename: str):
    server = CryptoServer((host, port), filename)
    server.listen()
