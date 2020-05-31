from argparse import ArgumentParser

from server import create_server
from client import communicate


def parse_args():
    parser = ArgumentParser(description='Simple VPN shell')
    parser.add_argument('host', help='remote host to connect', nargs='?', default='localhost')
    parser.add_argument('rport', help='remote port to connect', type=int, nargs='?', default=31337)
    parser.add_argument('-l', '--listen', action='store_true', help='work as a server')
    parser.add_argument('-p', '--port', type=int, help='listen on specific port', default=31337)
    parser.add_argument('-f', '--file', help='path to file containing password', required=True)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    if args.listen and args.port:
        create_server('', args.port, args.file)
    else:
        communicate(args.host, args.rport, args.file)
