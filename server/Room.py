import random

from server.Player import Player


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
        return self.isFull
