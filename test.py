import socket
import threading

host = "127.0.0.1"
port = 6660
addr = (host, port)
myname = 'howllow'
mypass = '123'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(addr)

def sendDict(dict):
    global sock
    sock.sendall(str(dict).encode('utf-8'))


def getResponse():
    return sock.recv(1024).decode('utf-8')


def getRegInfo():
    inputusr = input('Register username:')
    inputpas = input('Register password:')
    return [inputusr, inputpas]


def getLogInfo():
    inputusr = input('Login username:')
    inputpas = input('Login password:')
    return [inputusr, inputpas]


def register(username, password):
    dataDict = dict(username = username, password = password, type = 'register')
    sendDict(dataDict)
    ret = getResponse()
    if ret == 'rgok':
        print('Register Successful!\n')
        return 0
    else:
        print("Username already in use!!\n")
        return -1


def login(username, password):
    global myname
    global mypass
    dataDict = dict(username = username, password = password, type = 'login')
    sendDict(dataDict)
    ret = getResponse()
    while True:
        if ret == 'lgok':
            print('Login Successful!\nChatChanの世界にようこそ！！\n')
            myname = username
            mypass = password
            return 0
        elif ret == 'Online':
            print('User has already been ONLINE!!')
            return -1
        elif ret == 'PassWrong':
            print('Password is wrong!')
            return -1
        elif ret == 'Nonexistent':
            print('User nonexistent')


class RecvThread(threading.Thread):
    def run(self):
        while True:
            data = getResponse()
            while data.strip():

                if data == 'uook':
                    print("That's all!!")
                    break

                if data == 'mgok':
                    print("Group has been successfully made!!")
                    break

                if data == 'mgbad':
                    print("Group has existed!!")
                    break

                if data == 'pcbad':
                    print("Sending message failed. Maybe target doesn't exist.")
                    break

                if data == 'NoGrp':
                    print("Group doesn't exist.")
                    break

                if data == 'NotInGrp':
                    print("You are not in the group.")
                    break

                if data == 'egok':
                    print("Successfully entered!! Let's chat!!")
                    break

                if data == 'egbad':
                    print("Entering failed. Maybe group doesn't exist.")
                    break

                if data == 'gmok':
                    print("That's all!!")
                    break

                dataDict = eval(data)
                if type(dataDict) == dict:
                    if dataDict['type'] == 'useronline':
                        print(dataDict['listmsg'])

                    if dataDict['type'] == 'grpmember':
                        print(dataDict['listmsg'])

                    if dataDict['type'] == 'prchat':
                        print(dataDict['message'])

                    if dataDict['type'] == 'grpchat':
                        print(dataDict['message'])
                    break


class SendThread(threading.Thread):
    global myname
    global mypass
    def run(self):
        print("Please input your request:")
        while True:
            req = input()
            if req == 'prchat':
                msg = input("Who you wanna chat with:")
                chatwith = input("What you wanna say:")
                dataDict = dict(type = req, message = msg, chatwith = chatwith, username = myname, password = mypass)
                sendDict(dataDict)

            if req == 'useronline':
                dataDict = dict(username = myname, password = mypass, type = 'useronline')
                sendDict(dataDict)





if __name__ == '__main__':
    reginfo = getRegInfo()
    register(reginfo[0], reginfo[1])
    loginfo = getLogInfo()
    login(loginfo[0], loginfo[1])

    mysend = SendThread()
    myrecv = RecvThread()
    mysend.start()
    myrecv.start()
    mysend.join()
    myrecv.join()


