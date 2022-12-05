class Player:
    def __init__(self, connection, room, playerNumber):
        self.color = 0
        self.connection = connection
        self.room = room
        self.playerNumber = playerNumber

    def send(self, message):
        self.connection.send(str.encode(message))
