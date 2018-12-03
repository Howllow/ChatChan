import socket
import sys
import signal

host = "127.0.0.1"
port = 6663
addr = (host, port)
username = 'howllow'
password = '123'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(addr)

dataDict = dict(username = 'howllow', password = '123', type = 'register')
sock.sendall(str(dataDict).encode('utf-8'))
ret = sock.recv(1024).decode('utf-8')

if ret == 'ok':
    print('Register Successful!\n')
else:
    print("Username already in use!!\n")

def myhandler(signum, frame):
    dataDict = dict(username='howllow', password='123', type='logout')
    sock.sendall(str(dataDict).encode('utf-8'))
    exit()

dataDict = dict(username = 'howllow', password = '123', type = 'login')
sock.sendall(str(dataDict).encode('utf-8'))
ret = sock.recv(1024).decode('utf-8')
if ret == 'ok':
    print('Login Successful!\nChatChanの世界にようこそ！！\n')
elif ret == 'Online':
    print('User has already been ONLINE!!')

dataDict = dict(username = 'howllow', password = '123', type = 'useronline')
sock.sendall(str(dataDict).encode('utf-8'))
ret = ''
while True:
    data = sock.recv(1024).decode('utf-8')
    if (data == 'ok'):
        break
    print(data)
print ("That's all!!")



while True:
    continue
