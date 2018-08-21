from .client import ChatClient
import threading
import socket
import sys


PORT = 8000


class ChatServer(threading.Thread):
    def __init__(self, port, host='localhost'):
        super().__init__(daemon=True)
        self.port = port
        self.host = host
        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP,
        )
        self.client_pool = []

        try:
            self.server.bind((self.host, self.port))
        except socket.error:
            print('Bind failed {}'.format(socket.error))
            sys.exit()

        self.server.listen(10)

    def parser(self, id, nickname, conn, message):
        data = message.decode.split(maxsplit=1)
        if data[0] == '@quit':
            conn.sendall(b'You have left the channel. You will be missed.\n')
            reply = nickname.encode() + b' has left the channel.\n'
            [c.conn.sendall(reply) for c in self.client_pool if len(self.client_pool)]

