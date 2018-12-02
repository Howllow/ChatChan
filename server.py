import socket, asyncore
from asyncore import dispatcher
from asynchat import async_chat

PORT = 3154
HOST = '127.0.0.1'

class Cmd_Handler:
    """
    class to handle different commands
    """
    def undefined_cmd(self, cmd):

    def handle_cmd(self, session, cmd):

class EndSession:
    """
    do something when a session is ending
    """

class Room(Cmd_Handler):
    """
    general class of ROOM
    """
    def __init__(self):
        self.sessions = []

    def add(self, session):
        'add a session to the room'
        self.sessions.append(session)

    def remove(self, session):
        'remove a session from the room'
        self.sessions.remove(session)

    def broadcast(self, message):
        'broadcast the massage to all sessions in the room'
        for session in self.sessions:
            session.push(message)

    def handle_logout(self):
        raise EndSession


class LoginHere(Room):

class ChatRoom(Room):

class LogoutHere(Room):

class Session(async_chat):

class Chat_Server(dispatcher):
    def __init__(self):
        dispatcher.__init__(self)
        self.create_socket(self, socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr(self)
        self.bind((HOST, PORT))
        self.listen(self, 5)
        self.users = {}

if __name__ == '__main__':
	s = Chat_Server(PORT)
	try:
		asyncore.loop()
	except KeyboardInterrupt:
		print





