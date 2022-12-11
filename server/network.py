import socket
import server.common


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "115.137.252.201"
        # self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = None
        self.connected = True
        try:
            self.client.connect(self.addr)
        except socket.error:
            self.connected = False
            pass
        self.isStart = False
        self.turn = 0
        self.startMessege = None

    def getPos(self):
        return self.pos

    def getMessage(self):
        try:
            data = self.client.recv(2048).decode()
            # print(data)
            if data.__contains__("start"):
                self.isStart = True
                self.startMessege = data
            return data
        except:
            self.connected = False
            pass

    def getPosMessage(self):
        try:
            data = self.client.recv(2048).decode()
            if data == None:
                self.connected = False
                return
            data = server.common.read_pos(data)
            self.pos = data
        except socket.error as e:
            print(e)
            self.connected = False
            pass
        except:
            self.connected = False
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            print(data)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
            self.connected = False
            print(e)
        except:
            self.connected = False
            pass
    def sendOnly(self, data):
        try:
            self.client.send(str.encode(data))
            print(data)
        except socket.error as e:
            self.connected = False
            print(e)
        except:
            self.connected = False
            pass

    def getTurn(self):
        return self.turn
