import socketserver
import time
import threading
import db

GroupLst = []
ConnLst = []

class Connector:
    def __init__(self, username, AdPt, ConnObj):
        self.username = username
        self.AdPt = AdPt
        self.ConnObj = ConnObj

class Group:
    def __init__(self, owner, name):
        self.owner = owner
        self.name = 'group ' + name
        self.createTime = time.time()
        self.members = [owner]
        self.id = 'Group' + str(len(GroupLst))

class Handler(socketserver.BaseRequestHandler):
    def do_register(self, dataDict):
        username = dataDict['username']
        password = dataDict['password']
        checkflag = True
        'Check if username has been existed' \
        'If not, record the username and password'
        if checkflag == True:
            return 'ok'
        else:
            return 'bad'

    def do_login(self, dataDict):
        username = dataDict['username']
        password = dataDict['password']
        checkflag = 'True'
        'Check if they are correct, then change checkflag'
        if checkflag == 'True':
            ConnLst.append(Connector(username, self.client_address, self.request))
            return 'ok'
        elif checkflag == 'PassWrong':
            return 'PassWrong'
        else:
            return 'Nonexistent'

    def do_makegrp(self, dataDict):
        checkflag = True
        'Check if the Group has been existed' \
        'If not, record the username and password'
        if checkflag:
            grp = Group(dataDict['username'], dataDict['grpname'])
            GroupLst.append(grp)
            return ('ok')
        else:
            return ('bad')

    def do_prchat(self, dataDict):

    def do_grpchat(self, dataDict):

    def do_grpmember

    def do_useronline

    def find_meth(self, dataDict):
        return getattr(self, 'do_' + dataDict['type'], None)



    def handle(self):
        print('Got connection from', self.client_address)
        global GroupLst
        global ConnLst
        conn = self.request
        ret = 'ok'
        while True:
            data = conn.recv(1024).decode('utf-8')
            dataDict = eval(data)
            if not data or type(dataDict) != 'dict':
                continue
            meth = self.find_meth(dataDict)
            ret = meth(dataDict)
            conn.sendall(ret.encode('utf-8'))








