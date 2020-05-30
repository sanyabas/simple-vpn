import socket

HOST, PORT = 'localhost', 31337


class CryptoClient:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host: str, port: int):
        self.socket.connect((host, port))

    def send(self, data: str):
        self.socket.sendall(data.encode())

    def recv(self, size: int) -> bytes:
        return self.socket.recv(size)


if __name__ == '__main__':
    client = CryptoClient()
    client.connect(HOST, PORT)
    client.send('AAAAAAAAAAAAAAAA\n')
    print(client.recv(2048))