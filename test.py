from socket import *
import threading
import time

# import chess_gui


def send(sock, data):
    print(data)
    sock.send(((str)(data)).encode())


def receive(sock):
    while True:
        recvData = sock.recv(1024)
        decode = recvData.decode('utf-8')
        print('상대방 :', decode)
        send(sock, decode)

def connector():
    port = 8082
    serverSock = socket(AF_INET, SOCK_STREAM)
    serverSock.bind(('', port))
    serverSock.listen(1)


    print('%d번 포트로 접속 대기중...' % port)

    # connecting = threading.Thread(target=serverSock.accept(), args=())
    connectionSock, addr = serverSock.accept()


    receiver = threading.Thread(target=receive, args=(connectionSock,))
    print(str(addr), '에서 접속되었습니다.')

    # sender.start()
    decode = receiver.start()

    # sender = threading.Thread(target=send, args=(connectionSock,))


def mainMethod():
    connector = threading.Thread(target=connector(), args=())
    connector.start()
    while True:
        time.sleep(1)
        pass



mainMethod()