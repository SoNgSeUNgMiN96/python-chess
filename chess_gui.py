#
# The GUI engine for Python Chess
#
# Author: Boo Sung Kim, Eddie Sharick
# Note: The pygame tutorial by Eddie Sharick was used for the GUI engine. The GUI code was altered by Boo Sung Kim to
# fit in with the rest of the project.
#
import chess_engine
import pygame as py
import server.common

import ai_engine
import chess_server
import select_server_client
from server.network import Network
from enums import Player
import threading
from _thread import *

"""Variables"""
WIDTH = HEIGHT = 512  # width and height of the chess board
DIMENSION = 8  # the dimensions of the chess board
SQ_SIZE = HEIGHT // DIMENSION  # the size of each of the squares in the board
MAX_FPS = 15  # FPS for animations
IMAGES = {}  # images for the chess pieces
colors = [py.Color("white"), py.Color("gray")]

# TODO: AI black has been worked on. Mirror progress for other two modes
def load_images():
    '''
    Load images for the chess pieces
    '''
    for p in Player.PIECES:
        IMAGES[p] = py.transform.scale(py.image.load("images/" + p + ".png"), (SQ_SIZE, SQ_SIZE))


def draw_game_state(screen, game_state, valid_moves, square_selected):
    ''' Draw the complete chess board with pieces

    Keyword arguments:
        :param screen       -- the pygame screen
        :param game_state   -- the state of the current chess game
    '''
    draw_squares(screen)
    highlight_square(screen, game_state, valid_moves, square_selected)
    draw_pieces(screen, game_state)


def draw_squares(screen):
    ''' Draw the chess board with the alternating two colors

    :param screen:          -- the pygame screen
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            py.draw.rect(screen, color, py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, game_state):
    ''' Draw the chess pieces onto the board

    :param screen:          -- the pygame screen
    :param game_state:      -- the current state of the chess game
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = game_state.get_piece(r, c)
            if piece is not None and piece != Player.EMPTY:
                screen.blit(IMAGES[piece.get_player() + "_" + piece.get_name()],
                            py.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlight_square(screen, game_state, valid_moves, square_selected):
    if square_selected != () and game_state.is_valid_piece(square_selected[0], square_selected[1]):
        row = square_selected[0]
        col = square_selected[1]

        if (game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_1)) or \
                (not game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_2)):
            # hightlight selected square
            s = py.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(py.Color("blue"))
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

            # highlight move squares
            s.fill(py.Color("green"))

            for move in valid_moves:
                screen.blit(s, (move[1] * SQ_SIZE, move[0] * SQ_SIZE))


def main():
    # Check for the number of players and the color of the AI

    network_game()
    # normal_game()


def network_game():
    pygame_start("", True)


def normal_game():
    human_player = ""
    while True:
        try:
            number_of_players = input("How many players (1 or 2)?\n")
            if int(number_of_players) == 1:
                number_of_players = 1
                while True:
                    human_player = input("What color do you want to play (w or b)?\n")
                    if human_player == "w" or human_player == "b":
                        break
                    else:
                        print("Enter w or b.\n")
                break
            elif int(number_of_players) == 2:
                number_of_players = 2
                break
            else:
                print("Enter 1 or 2.\n")
        except ValueError:
            print("Enter 1 or 2.")
    pygame_start(human_player, False)


def pygame_start(human_player, is_multi):
    py.init()
    screen = py.display.set_mode((WIDTH, HEIGHT))
    clock = py.time.Clock()
    game_state = chess_engine.game_state()
    load_images()
    running = True
    square_selected = ()  # keeps track of the last selected square
    player_clicks = []  # keeps track of player clicks (two tuples)
    valid_moves = []
    game_over = False
    ai = ai_engine.chess_ai()
    game_state = chess_engine.game_state()

    my_color = None
    n = None

    isStart = False


    #게임시작은 쓰레드로 돌려야함. 누군가 들어와서 시작할 때 까진 대기해야함.
    if is_multi:
        n = Network()
        start_new_thread(n.getMessage, ())

    isFirst = True
    turn = None
    myPlayerNum = None

    if human_player == 'b':
        ai_move = ai.minimax_black(game_state, 3, -100000, 100000, True, Player.PLAYER_1)
        game_state.move_piece(ai_move[0], ai_move[1], True)

    while running:


        #멀티모드에서 턴을 계속해서 받아온다?
        #if is_multi:
            #turn = n.getMessageessage()

        if is_multi:
            if n.isStart:
                if isFirst:
                    temp = str(n.startMessege)
                    temp = temp.split(" ")
                    turn = int(temp[1])
                    myPlayerNum = int(temp[2])
                    isFirst = False
                    print("turn : "+str(turn))
                    print("myPlayerNum : "+str(myPlayerNum))

        #멀티모드가 아니거나, 멀티모드이지만 시작한 경우.
        if not is_multi or (is_multi and n.isStart):
            game_state, running, square_selected, valid_moves = click_method(ai, game_over, game_state, human_player,
                                                                         is_multi, myPlayerNum, n, player_clicks,
                                                                         running, square_selected, turn, valid_moves)

        draw_game_state(screen, game_state, valid_moves, square_selected)
        endgame = game_state.checkmate_stalemate_checker()
        if endgame == 0:
            game_over = True
            draw_text(screen, "Black wins.")
        elif endgame == 1:
            game_over = True
            draw_text(screen, "White wins.")
        elif endgame == 2:
            game_over = True
            draw_text(screen, "Stalemate.")

        clock.tick(MAX_FPS)
        py.display.flip()


def click_method(ai, game_over, game_state, human_player, is_multi, myPlayerNum, n, player_clicks, running,
                 square_selected, turn, valid_moves):
    for e in py.event.get():

        if e.type == py.QUIT:
            running = False

        # 멀티모드에서 최초의 초기화 부분이라고 볼 수 있음. 이 부분에서 차례와 모든것을 정한다.

        elif is_multi and (not n.isStart or (turn % 2 != myPlayerNum)):
            pass

        elif e.type == py.MOUSEBUTTONDOWN:
            if not game_over:
                location = py.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                # 같은 클릭은 이동 취소를 의미한다.
                if square_selected == (row, col):
                    square_selected = ()
                    player_clicks = []
                # 현재 클릭한 좌표를 담아준다.
                else:
                    square_selected = (row, col)
                    player_clicks.append(square_selected)

                if len(player_clicks) == 2:
                    # this if is useless right now
                    if (player_clicks[1][0], player_clicks[1][1]) not in valid_moves:
                        square_selected = ()
                        player_clicks = []
                        valid_moves = []
                    else:
                        game_state.move_piece((player_clicks[0][0], player_clicks[0][1]),
                                              (player_clicks[1][0], player_clicks[1][1]), False)
                        n.sendOnly(server.common.make_pos(player_clicks))
                        print(server.common.make_pos(player_clicks))
                        square_selected = ()
                        player_clicks = []
                        valid_moves = []

                        if human_player == 'w':
                            ai_move = ai.minimax_white(game_state, 3, -100000, 100000, True, Player.PLAYER_2)
                            game_state.move_piece(ai_move[0], ai_move[1], True)
                        elif human_player == 'b':
                            ai_move = ai.minimax_black(game_state, 3, -100000, 100000, True, Player.PLAYER_1)
                            game_state.move_piece(ai_move[0], ai_move[1], True)
                else:
                    valid_moves = game_state.get_valid_moves((row, col))
                    if valid_moves is None:
                        valid_moves = []
        elif e.type == py.KEYDOWN:
            if e.key == py.K_r:
                game_over = False
                game_state = chess_engine.game_state()
                valid_moves = []
                square_selected = ()
                player_clicks = []
                valid_moves = []
            elif e.key == py.K_u:
                game_state.undo_move()
                print(len(game_state.move_log))
    return game_state, running, square_selected, valid_moves


def draw_text(screen, text):
    font = py.font.SysFont("Helvitca", 32, True, False)
    text_object = font.render(text, False, py.Color("Black"))
    text_location = py.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2,
                                                      HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)


if __name__ == "__main__":
    main()
