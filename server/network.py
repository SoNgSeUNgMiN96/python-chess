import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = (0, 0, 0, 0)
        self.turn = self.connect()

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            return self.getMessage()
        except:
            pass

    def getMessage(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
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
