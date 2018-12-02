import socket, asyncore
from asyncore import dispatcher
from asynchat import async_chat

PORT = 3154
HOST = '127.0.0.1'

class Cmd_Handler:
    """
    class to handle different commands
    """
    def undefined_cmd(self, session, cmd):
        session.push('Command is Undefined! : %s\n' % cmd)

    def handle_cmd(self, session, input):
        'check if it is an empty string'
        if not input.strip():
            return
        input_parts = input.split(':', 1)
        cmd = input_parts[0]
        try:
            info = input_parts[1]
        except(IndexError):
            info = ''
        func = getattr(self, 'handle_'.join(cmd), None)
        try:
            func(session, info)
        except(TypeError):
            self.undefined_cmd(session, cmd)



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
        'broadcast the message to all sessions in the room'
        for session in self.sessions:
            session.push(message)

    def handle_logout(self):
        raise EndSession

class WaitingRoom(Room):
    """
    Stay here after login and before the chat
    """

class Login(Cmd_Handler):
    """
    deal with login
    """
    def login(self, session, input):
        id_and_pas = input.split(":", 1)[1]
        id = id_and_pas.split(" ", 1)[0]
        pas = id_and_pas.split(" ", 1)[1]
        """
        search id in database
        if there isn't this id, return 'Fail'
        if there is, compare password
        """
        session.push('Login Successful')

        return ('Login Successful')

class ChatRoom(Room):

class Logout:

class Session(async_chat):


class Chat_Server(dispatcher):
    def __init__(self, host, port):
        dispatcher.__init__(self)
        self.create_socket(self, socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr(self)
        self.bind((host, port))
        self.listen(self, 5)
        self.users = {}

if __name__ == '__main__':
    s = Chat_Server(PORT)
	try:
		asyncore.loop()
	except KeyboardInterrupt:
		print





