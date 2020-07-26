from socket import *
from time import ctime
import sys




HOST = ''
# PORT = 21568
PORT = int(sys.argv[1])
BUFSIZ = 1024
ADDR = (HOST,PORT)


tcpSerSock = socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(128)
# tcpSerSock.setsockopt(IPPROTO_IP,IP_TOS,0x04)
while True:
    print('waiting for connection...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('...connnecting from:', addr)

    while True:
        data = tcpCliSock.recv(BUFSIZ)
        # print data
        # print type(data)
        if not data:
            break
        #tcpCliSock.send('[%s] %s' %(bytes(ctime(),'utf-8'),data))
        # tcpCliSock.send(('[%s] %s' % (ctime(), data)).encode())
        tcpCliSock.send(data.encode())
    tcpCliSock.close()
    break
tcpSerSock.close()