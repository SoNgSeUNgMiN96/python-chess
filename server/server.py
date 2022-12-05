import random
import socket
from _thread import *
import common

import random

from server.Player import Player
from server.Room import Room

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

# Todo pos를 룸단위로 구분하기
## 좌표는 2차원 튜플로 구분한다.

pos = [[(0, 0), (0, 0)], [(0, 0), (0, 0)]]

turn = ['w', 'b']

roomList = []

randomTurn = random.randint(0, 2)


def isRoomExist():
    room_list = Room(roomList)
    for room in room_list:
        if room.isEnterable():
            return room
    return None


def sendEncode(conn, message):
    conn.send(str.encode(message))


def threaded_client(conn):
    room = Room(isRoomExist())

    # 룸이 없다면 룸 생성 후 리스트 추가
    if room is None:
        room = Room()
        roomList.append(room)

    # Player 생성.
    player = Player(conn, room, room.playerNumber)
    player.room = room
    room.add_player(player)

    #startable 일 때 전송해줘야함.
    

    while True:
        try:
            data = common.read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(common.make_pos(reply)))
        except:
            break

    print("Lost connection")
    conn.close()



# 차례번호 대로
# 커넥션 리스트를 관리하기?

# 우선 2명 모드만 지원하고, 업데이트 하는 방식으로 바꾸기.
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn))
