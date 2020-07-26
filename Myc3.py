from socket import *
import time
import sys
import pandas as pd


# HOST = '10.0.0.4' # or 'localhost'
# PORT = 21568
HOST = sys.argv[1]
PORT = int(sys.argv[2])
flowsize = int(sys.argv[3])
flowtype = int(sys.argv[4])
deadline = float(sys.argv[5])
src = int(sys.argv[6])
dst = int(sys.argv[7])



BUFSIZ =1024
ADDR = (HOST,PORT)
tcpCliSock = socket(AF_INET,SOCK_STREAM)
# flowsize = 7
tcpCliSock.connect(ADDR)

# pri = 0x08
# tcpCliSock.setsockopt(IPPROTO_IP,IP_TOS,pri)


flowStartTime = time.time()
for i in range(flowsize):
    # data1 = input('>')
    # data = str(data)

    payload = "0" * 1024
    data1 = payload
    # print type(data1)
    if not data1:
        break
    tcpCliSock.send(data1.encode())
    data1 = tcpCliSock.recv(BUFSIZ)
    if not data1:
        break
    # print(data1.decode('utf-8'))
FCT = time.time() - flowStartTime
result = [flowsize, FCT]
# print result
tcpCliSock.close()


if flowtype == 1:
    if deadline/1000.0 >= FCT:
        meetrate = True
    else:
        meetrate = False

else:
    meetrate = None


# flowsize, FCT, flowtype, src, dst
headers = ['src', 'dst','flowtype', 'flowsize', 'FCT', 'meetrate']
df = pd.DataFrame([[src, dst, flowtype, flowsize, FCT, meetrate]])
df.to_csv("2.csv", mode='a',header=False,index=False)




