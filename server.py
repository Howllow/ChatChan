import socketserver
import time
import threading

GroupLst = []
ConnLst = []
host = '127.0.0.1'
port = 6663
addr = (host, port)

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
    def CheckDeadConn(self):
        if len(ConnLst) > 0:
            for conn in ConnLst:
                print (conn.ConnObj())
                if conn.ConnObj.fd == -1:
                    ConnLst.remove(conn)

    def check_in_grp(self, dataDict):
        grpname = dataDict['grpname']
        username = dataDict['username']
        hasGrp = False
        inGrp = False
        mygrp = None
        for grp in GroupLst:
            if grpname == grp.name:
                hasGrp = True
                for member in grp.members:
                    if member.username == username:
                        inGrp = True
                        mygrp = grp
                        break
                break
        if not hasGrp:
            return 'NoGrp'
        elif not inGrp:
            return 'NotInGrp'
        else: return mygrp


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
        self.CheckDeadConn()
        username = dataDict['username']
        password = dataDict['password']
        checkflag = 'True'
        'Check if they are correct, then change checkflag'
        for usr in ConnLst:
            if (usr.username == username):
                return 'Online'
        if checkflag == 'True':
            ConnLst.append(Connector(username, self.client_address, self.request))
            return 'ok'
        elif checkflag == 'PassWrong':
            return 'PassWrong'
        else:
            return 'Nonexistent'


    def do_makegrp(self, dataDict):
        checkflag = True
        username = dataDict['username']
        'Check if the Group has been existed' \
        'If not, record the username and password'
        if checkflag:
            grp = Group(Connector(username, self.client_address, self.request), dataDict['grpname'])
            GroupLst.append(grp)
            return ('ok')
        else:
            return ('bad')


    def do_prchat(self, dataDict):
        self.CheckDeadConn()
        target = dataDict['chatwith']
        message = dataDict['message']
        username = dataDict['username']
        for connects in ConnLst:
            if connects.username == target:
                tobj = connects.ConnObj
                tobj.sendall(('msg from ' + username + " " + time.time() + '\n' + message).encode('utf-8'))
                return 'ok'
        return 'bad'


    def do_entergrp(self, dataDict):
        grpname = dataDict['grpname']
        username = dataDict['username']
        for grp in GroupLst:
            if grpname == grp.name:
                'maybe some authority check here'
                grp.members.append(Connector(username, self.client_address, self.request))
                return 'ok'
        return 'bad'


    def do_grpchat(self, dataDict):
        self.CheckDeadConn()
        grpname = dataDict['grpname']
        username = dataDict['username']
        message = ("msg from GROUP " + grpname + " " + time.time() + '\n' + dataDict['message']).encode('utf-8')
        flag = self.check_in_grp(dataDict)
        if type(flag) == Group:
            mygrp = flag
            for member in mygrp.members:
                if member.username != username:
                    member.ConnObj.sendall(message)
            return 'ok'
        else:
            return flag


    def do_grpmember(self, dataDict):
        flag = self.check_in_grp(dataDict)
        conn = self.request
        if type(flag) == Group:
            mygrp = flag
            str = 'members in GROUP ' + mygrp.name + ':\n'
            conn.sendall(str.encode('utf-8'))
            for member in mygrp.members:
                conn.sendall((member.username + "\n").encode('utf-8'))
            return 'ok'
        else:
            return flag


    def do_useronline(self, dataDict):
        self.CheckDeadConn()
        for user in ConnLst:
            self.request.sendall((user.username + "\n").encode('utf-8'))
        return 'ok'


    def do_logout(selfs, dataDict):
        username = dataDict['username']
        for grp in GroupLst:
            for member in grp.members:
                if member.username == username:
                    grp.members.remove(member)
                    break
        for conns in ConnLst:
            if conns.username == username:
                ConnLst.remove(conns)
                break


    def find_meth(self, dataDict):
        print('finding method')
        return getattr(self, 'do_' + dataDict['type'], None)



    def handle(self):
        print('Got connection from', self.client_address)
        global GroupLst
        global ConnLst
        conn = self.request
        while True:
            data = conn.recv(1024).decode('utf-8')
            print(data)
            dataDict = eval(data)
            if not data or type(dataDict) != dict:
                continue
            meth = self.find_meth(dataDict)
            ret = meth(dataDict)
            conn.sendall(ret.encode('utf-8'))

if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(addr, Handler)
    print('waiting for connection...')
    server.serve_forever()






