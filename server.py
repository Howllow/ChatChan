import socketserver
import time

GroupLst = []
ConnLst = []
host = '127.0.0.1'
port = 6660
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
                if conn.ConnObj.fileno() == -1:
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
            return 'rgok'
        else:
            return 'rgbad'


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
            return 'lgok'
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
            return ('mgok')
        else:
            return ('mgbad')


    def do_prchat(self, dataDict):
        self.CheckDeadConn()
        target = dataDict['chatwith']
        for connects in ConnLst:
            if connects.username == target:
                tobj = connects.ConnObj
                tobj.sendall(str(dataDict).encode('utf-8'))
                return 'pcok'
        return 'pcbad'


    def do_entergrp(self, dataDict):
        grpname = dataDict['grpname']
        username = dataDict['username']
        for grp in GroupLst:
            if grpname == grp.name:
                'maybe some authority check here'
                grp.members.append(Connector(username, self.client_address, self.request))
                return 'egok'
        return 'egbad'


    def do_grpchat(self, dataDict):
        self.CheckDeadConn()
        username = dataDict['username']
        flag = self.check_in_grp(dataDict)
        if type(flag) == Group:
            mygrp = flag
            for member in mygrp.members:
                if member.username != username:
                    member.ConnObj.sendall(str(dataDict).encode('utf-8'))
            return 'gcok'
        else:
            return flag


    def do_grpmember(self, dataDict):
        self.CheckDeadConn()
        flag = self.check_in_grp(dataDict)
        conn = self.request
        if type(flag) == Group:
            mygrp = flag
            str = 'members in GROUP ' + mygrp.name + ':\n'
            for member in mygrp.members:
                str += member.username + "\n"
            mydict = dataDict
            mydict['listmsg'] = str
            self.request.sendall(str(mydict).encode('utf-8'))
            return 'gmok'
        else:
            return flag


    def do_useronline(self, dataDict):
        self.CheckDeadConn()
        alluser = "Users Online:\n"
        for user in ConnLst:
            alluser += user.username + "\n"
        mydict = dataDict
        mydict['listmsg'] = alluser
        self.request.sendall(str(mydict).encode('utf-8'))
        return 'uook'


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
            print ("ret: %s" % ret)
            conn.sendall(ret.encode('utf-8'))


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(addr, Handler)
    print('waiting for connection...')
    server.serve_forever()






