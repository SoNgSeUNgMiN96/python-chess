import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = (0, 0, 0, 0)
        self.client.connect(self.addr)
        self.isStart = False
        self.turn = None
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

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def getTurn(self):
        return self.turn
