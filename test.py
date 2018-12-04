import socket
import sys
import signal

host = "127.0.0.1"
port = 6663
addr = (host, port)
myname = 'howllow'
mypass = '123'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(addr)
print(sock.fileno())

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
    if ret == 'lgok':
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


def useronline():
    dataDict = dict(username = myname, password = mypass, type = 'useronline')
    sendDict(dataDict)
    while True:
        data = getResponse()
        if (data == 'uook'):
            break
        print(data)
    print ("That's all!!")
    return 0


def prchat(chatwith, message):
    dataDict = dict(username = myname, password = mypass, type = 'prchat', chatwith = chatwith, message = message)
    sendDict(dataDict)
    ret = getResponse()
    print(ret)
    ret = getResponse()
    if ret == 'pcbad':
        print("Failed. Maybe target doesn't exist\n")


if __name__ == '__main__':
    reginfo = getRegInfo()
    register(reginfo[0], reginfo[1])
    loginfo = getLogInfo()
    login(loginfo[0], loginfo[1])

    chatwith = input('Who you want to chat with:')
    message = input('What you wanna say:')
    prchat(chatwith, message)
