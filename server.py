from client import ChatClient
import threading
import socket
import sys


PORT = 8000


class ChatServer(threading.Thread):
    """ Clients should be able to connect using a telnet or netcat client and communicate
        with each other. Clients should also be able to run special commands to quit,
        list users, reset their nickname, and send direct messages.
    """
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
        if message.decode().startswith('@'):
            data = message.decode().split(maxsplit=1)

            if data[0] == '@quit':
                conn.sendall(b'You have left the channel. You will be missed.\n')
                reply = nickname.encode() + b' has left the channel.\n'
                [c.conn.sendall(reply) for c in self.client_pool if len(self.client_pool)]
                self.client_pool = [c for c in self.client_pool if c.id != id]
                conn.close()
            elif data[0] == '@list':
                conn.sendall(b'Here is a list of all users in the channel:\n')
                [conn.sendall('{} \n'.format(chatters.nickname).encode()) for chatters in self.client_pool] #we know there is at least this user in client_pool
            elif data[0] == '@nickname':
                #unsure exactly, perhaps -
                # for client with client.id = id, client.nickname = data[1]
                # however, I'm not sure we can change the  properties of client here
                # since we have copies of the values passed to us, but not the actual
                # object to change directly. Due to time constraints, we were unable
                # to investigate further.
                conn.sendall(b'Sorry, updating your nickname is not functional yet.\n')
            elif data[0] == '@dm':
                #needs to be filled out.
                conn.sendall(b'Sorry, that feature is not functional yet.\n')
                pass
            else:
                conn.sendall(b'Invalid command! Please try again.\n')
        else:
            reply = nickname.encode() + b': ' + message
            [c.conn.sendall(reply) for c in self.client_pool if len(self.client_pool)]


    def run_thread(self, id, nickname, conn, addr):
        print('{} connected with {}:{}'.format(nickname, addr[0], str(addr[1])))
        try:
            while True:
                data = conn.recv(4086)
                self.parser(id, nickname, conn, data)
        except (ConnectionResetError, BrokenPipeError, OSError):
            conn.close()

    def run(self):
        print('Server running on {}'.format(PORT))
        while True:
            conn, addr = self.server.accept()
            client = ChatClient(conn, addr)
            self.client_pool.append(client)
            threading.Thread(
                target=self.run_thread,
                args=(client.id, client.nickname, client.conn, client.addr),
                daemon=True,
            ).start()


    def exit(self):
        self.server.close()


if __name__ == '__main__':
    """ Main program to run if this file was called directly
    """
    server = ChatServer(PORT)
    try:
        server.run()
    except KeyboardInterrupt:
        [c.conn.close() for c in server.client_pool if len(server.client_pool)]
        server.exit()


