import random

from Player import Player


class Room:

    def __init__(self):
        self.playerList = []
        self.turn = 0
        self.playerNumber = 0
        self.isFull = False

    def add_player(self, player):
        self.playerList.append(player)
        self.playerNumber += 1
        if self.playerNumber == 2:
            self.isFull = True

    def isEnterable(self):
        return not self.isFull

    def broadcast(self, message):
        for player in self.playerList:
            player.send(str(message))

    def gamestart(self):
        self.turn = random.randint(0,10)

    def sendAnotherPlayer(self, playerNum, message):
        self.playerList[(playerNum+1)%2].send(str(message))