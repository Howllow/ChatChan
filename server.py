import socket, asyncore
from asyncore import dispatcher
from asynchat import async_chat

PORT = 3154
HOST = '127.0.0.1'
class Chat_Server(dispatcher):
    def __init__(self):
        dispatcher.__init__(self)
        self.create_socket(self, socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr(self)
        self.bind((HOST, PORT))
        self.listen(self, 5)
        self.users = {}

if __name__ == '__main__':
	s = ChatServer(PORT)
	try:
		asyncore.loop()
	except KeyboardInterrupt:
		print





