from socketserver import StreamRequestHandler, TCPServer


class CryptoTCPHandler(StreamRequestHandler):
    def handle(self) -> None:
        while True:
            data = self.rfile.readline().strip()
            if data == b'':
                return

            print(f'{self.client_address}: {data}')

            self.wfile.write(data)


def create_server(host: str, port: int):
    with TCPServer((host, port), CryptoTCPHandler) as server:
        server.serve_forever()

        return server
