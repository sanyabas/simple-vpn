from socketserver import StreamRequestHandler, TCPServer, BaseRequestHandler
from typing import Tuple, Callable

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from util import get_password, encrypt, decrypt


class CryptoTCPHandler(StreamRequestHandler):
    def setup(self) -> None:
        super(CryptoTCPHandler, self).setup()

        # EKE algorithm
        self._session_key = get_random_bytes(16)
        print(self._session_key)
        ciphertext = self.rfile.read(32)
        client_key = decrypt(self.server._password, ciphertext)

        ciphertext = encrypt(client_key, self._session_key)
        ciphertext = encrypt(self.server._password, ciphertext)
        self.wfile.write(ciphertext)

        ciphertext = self.rfile.read(32)
        r_a = decrypt(self._session_key, ciphertext)
        r_b = get_random_bytes(16)
        ciphertext = encrypt(self._session_key, r_a + r_b)
        self.wfile.write(ciphertext)
        print('r_a', r_a)
        print('r_b', r_b)

        ciphertext = self.rfile.read(32)
        r_b_received = decrypt(self._session_key, ciphertext)
        if r_b_received != r_b:
            raise ValueError('r_b invalid')

    def handle(self) -> None:
        while True:
            data = self.rfile.readline().strip()
            if data == b'':
                return

            print(f'{self.client_address}: {data}')

            self.wfile.write(data)


class CryptoServer(TCPServer):
    def __init__(self, server_address: Tuple[str, int], RequestHandlerClass: Callable[..., BaseRequestHandler], filename: str):
        super().__init__(server_address, RequestHandlerClass)
        self._password = get_password(filename)


def create_server(host: str, port: int, filename: str):
    with CryptoServer((host, port), CryptoTCPHandler, filename) as server:
        server.serve_forever()

        return server
