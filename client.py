import random
import uuid


class ChatClient():
    def __init__(self, conn=None, addr=None):
        self.id = str(uuid.uuid4())
        self.nickname = 'user_{}'.format(int(random.random() * 10000))
        self.conn = conn
        self.addr = addr
