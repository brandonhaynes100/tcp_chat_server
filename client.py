import random
import uuid


class ChatClient():
    """ Called by server.py ChatServer to allow each client to connect to the chat
        server (via telnet or netcat) and use the features of the chat system.
    """
    def __init__(self, conn=None, addr=None):
        self.id = str(uuid.uuid4())
        self.nickname = 'user_{}'.format(int(random.random() * 10000))
        self.conn = conn
        self.addr = addr
