from socket import *
import threading
import time

# import chess_gui


class server:
    serverSock = None
    isStarted = False

    @staticmethod
    def send(sock, data):
        print(data)
        sock.send(((str)(data)).encode())


    @staticmethod
    def receive(sock):
        while True:
            recvData = sock.recv(1024)
            decode = recvData.decode('utf-8')
            print('상대방 :', decode)
            server.send(sock, decode)

    @staticmethod
    def connector():
        port = 8083
        serverSock = socket(AF_INET, SOCK_STREAM)
        serverSock.bind(('', port))
        serverSock.listen(1)


        print('%d번 포트로 접속 대기중...' % port)

        # connecting = threading.Thread(target=serverSock.accept(), args=())
        connectionSock, addr = serverSock.accept()


        receiver = threading.Thread(target=server.receive, args=(connectionSock,))
        receiver.start()
        print(str(addr), '에서 접속되었습니다.')
        isStarted = True


    @staticmethod
    def mainMethod():
        conn = threading.Thread(target=server.connector, args=())
        print("chess_server_start. con !")
        conn.start()

        while True:
            time.sleep(1)
            pass
