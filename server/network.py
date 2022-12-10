import socket
import server.common


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "115.137.252.201"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = None
        self.client.connect(self.addr)
        self.isStart = False
        self.turn = 0
        self.startMessege = None

    def getPos(self):
        return self.pos

    def getMessage(self):
        try:
            data = self.client.recv(2048).decode()
            if data.__contains__("start"):
                self.isStart = True
                print("game ", data)
                self.startMessege = data
            return data
        except:
            pass

    def getPosMessage(self):
        try:
            data = self.client.recv(2048).decode()
            data = server.common.read_pos(data)
            self.pos = data
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            print(data)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def sendOnly(self, data):
        try:
            self.client.send(str.encode(data))
            print(data)
        except socket.error as e:
            print(e)

    def getTurn(self):
        return self.turn
