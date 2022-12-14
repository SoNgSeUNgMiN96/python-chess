#
# The GUI engine for Python Chess
#
# Author: Boo Sung Kim, Eddie Sharick
# Note: The pygame tutorial by Eddie Sharick was used for the GUI engine. The GUI code was altered by Boo Sung Kim to
# fit in with the rest of the project.
#
import chess_engine
import pygame as py
import time
import sys
import server.common
import ai_engine
from server.network import Network
from enums import Player
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

class Button:
    def __init__(self, img_in, x, y, width, height, action=None, main_menu_display=None):
        mouse = py.mouse.get_pos()
        click = py.mouse.get_pressed()
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            main_menu_display.blit(img_in, (x, y))
            if click[0] and action is not None:
                time.sleep(1)
                action()
        else:
            main_menu_display.blit(img_in, (x, y))

class Button2:
    def __init__(self, img_in, x, y, width, height, player, main_menu_display=None):
        mouse = py.mouse.get_pos()
        click = py.mouse.get_pressed()
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            main_menu_display.blit(img_in, (x, y))
            if click[0] and player is not None:
                time.sleep(1)
                start_game(player)
        else:
            main_menu_display.blit(img_in, (x, y))

def start_game(human_player):
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
    if human_player is 'b':
        py.time.wait(2000)
        ai_move = ai.minimax_black(game_state, 3, -100000, 100000, True, Player.PLAYER_1)
        now = py.time.get_ticks()
        game_state.move_piece(ai_move[0], ai_move[1], True)

    while running:
        for e in py.event.get():
            if e.type == py.QUIT:
                running = False
            elif e.type == py.MOUSEBUTTONDOWN:
                if not game_over:
                    location = py.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if square_selected == (row, col):
                        square_selected = ()
                        player_clicks = []
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
                            square_selected = ()
                            player_clicks = []
                            valid_moves = []

                            if human_player is 'w':
                                py.time.wait(2000)
                                ai_move = ai.minimax_white(game_state, 3, -100000, 100000, True, Player.PLAYER_2)
                                game_state.move_piece(ai_move[0], ai_move[1], True)
                            elif human_player is 'b':
                                py.time.wait(2000)
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
                elif e.key == py.K_q:
                    running = False
                    start_main_menu()

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

def start_1p():
    select = True

    while select:
        background_image = py.image.load("images/background.png")
        background_image = py.transform.scale(background_image, (800, 600))
        
        button_white_image = py.image.load("images/white_n.png")
        button_white_image = py.transform.scale(button_white_image, (200, 200))
        button_black_image = py.image.load("images/black_n.png")
        button_black_image = py.transform.scale(button_black_image, (200, 200))
        button_back_image = py.image.load("images/back.png")
        button_back_image = py.transform.scale(button_back_image, (100, 100))

        select_menu_display_width, select_menu_display_height = 800, 600
        select_menu_display = py.display.set_mode((select_menu_display_width, select_menu_display_height))
        clock = py.time.Clock()

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

        select_menu_display.blit(background_image, (0, 0))
        button_white = Button2(button_white_image, 150, 200, 200, 200, "w", select_menu_display)
        button_black = Button2(button_black_image, 450, 200, 200, 200, "b", select_menu_display)
        button_back = Button(button_back_image, 650, 450, 100, 100, start_main_menu, select_menu_display)
        py.display.update()
        clock.tick(MAX_FPS)

def start_2p():
    human_player = ""
    start_game(human_player)

def pygame_start(human_player):
    py.init()
    screen = py.display.set_mode((512, 600))
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

    text = ""


    #??????????????? ???????????? ????????????. ????????? ???????????? ????????? ??? ?????? ???????????????.
    n = Network()
    start_new_thread(n.getMessage, ())


    isFirst = True
    myPlayerNum = None
    anotherFirst = True
    color = ""


    while running:
        if not game_over:
            draw_text(screen, text)
        if not n.connected:
            text ="disconnected"
            draw_text(screen, text)

        elif n.isStart:
            #??? ?????? ?????????
            if isFirst:
                temp = str(n.startMessege)
                print(temp)
                temp = temp.split(" ")
                n.turn = int(temp[1])
                myPlayerNum = int(temp[2])
                isFirst = False
                print("turn : "+str(n.turn))
                print("myPlayerNum : "+str(myPlayerNum))

                if myPlayerNum == n.turn % 2:
                    color = "white"
                else:
                    color = "black"

            ##
            if not n.connected:
                text ="disconnected"
                draw_text(screen, text)

            if game_over:
                game_over = end_game_action(endgame, game_over, screen)
            #?????????????????? ??????????????????
            elif n.turn % 2 != myPlayerNum:
                text = "my color is " + color + " opposing turn."
                if anotherFirst:
                    start_new_thread(n.getPosMessage, ())
                    anotherFirst = False
                else:
                    if n.pos is not None:
                        print("n pos!! ="+str(n.pos[0][0])+" "+str(n.pos[0][1])+" "+str(n.pos[1][0])+" "+str(n.pos[1][1])+" ")
                        game_state.move_piece((n.pos[0][0], n.pos[0][1]),
                                              (n.pos[1][0], n.pos[1][1]), False)
                        n.pos = None
                        anotherFirst = True
                        n.turn +=1
                        print("turn  = " + str(n.turn))
                    running, text = another_turn(n, running, screen, text)
            else:
                text = "my color is " + color + " my turn. "
                game_state, running, square_selected, valid_moves, player_clicks = click_method(ai, game_over, game_state, human_player,
                                                                        myPlayerNum, n, player_clicks,
                                                                         running, square_selected, valid_moves)
        else:
            text = "waiting player"
            running, text = another_turn(n, running, screen, text)

        draw_game_state(screen, game_state, valid_moves, square_selected)
        endgame = game_state.checkmate_stalemate_checker()
        game_over = end_game_action(endgame, game_over, screen)

        clock.tick(MAX_FPS)
        py.display.flip()

def end_game_action(endgame, game_over, screen):
    if endgame == 0:
        game_over = True
        draw_text(screen, "Black wins.")
    elif endgame == 1:
        game_over = True
        draw_text(screen, "White wins.")
    elif endgame == 2:
        game_over = True
        draw_text(screen, "Stalemate.")
    return game_over


def another_turn(n, running, screen, text):
    if not n.connected:
        text = "disconnected"
        draw_text(screen, text)
    for e in py.event.get():
        if e.type == py.QUIT:
            running = False
    return running, text


def click_method(ai, game_over, game_state, human_player, myPlayerNum, n, player_clicks, running,
                 square_selected, valid_moves):
    for e in py.event.get():

        if e.type == py.QUIT:
            running = False
        # ?????????????????? ????????? ????????? ??????????????? ??? ??? ??????. ??? ???????????? ????????? ???????????? ?????????.
        elif n.turn % 2 != myPlayerNum:
            pass
        elif e.type == py.MOUSEBUTTONDOWN:
            if not game_over:
                location = py.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                # ?????? ????????? ?????? ????????? ????????????.
                if square_selected == (row, col):
                    square_selected = ()
                    player_clicks = []
                # ?????? ????????? ????????? ????????????.
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
                        n.turn += 1
                        print("turn  = "+ str(n.turn))


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
    return game_state, running, square_selected, valid_moves, player_clicks

def network_game():
    pygame_start("")

def start_main_menu():
    menu = True

    while menu:
        background_image = py.image.load("images/background.png")
        background_image = py.transform.scale(background_image, (800, 600))
        
        button_1p_image = py.image.load("images/1p_button.png")
        button_2p_image = py.image.load("images/2p_button.png")
        online_button_image = py.image.load("images/online_button.png")

        main_menu_display_width, main_menu_display_height = 800, 600
        main_menu_display = py.display.set_mode((main_menu_display_width, main_menu_display_height))
        clock = py.time.Clock()

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

        main_menu_display.blit(background_image, (0, 0))
        button_1p = Button(button_1p_image, 280, 260, 98, 67, start_1p, main_menu_display)
        button_2p = Button(button_2p_image, 445, 260, 98, 67, start_2p, main_menu_display)
        online_button = Button(online_button_image, 330, 360, 162, 67, network_game, main_menu_display)
        py.display.update()
        clock.tick(MAX_FPS)


def main():
    # Check for the number of players and the color of the AI
    py.init()
    start_main_menu()


def draw_text(screen, text):
    font = py.font.SysFont("applegothicttf", 32, True, False)

    text_object = font.render(text, False, py.Color("white"))
    text_location = py.Rect(0, 300, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2,
                                                        HEIGHT / 2 - text_object.get_height() / 2)


    screen.fill('black', py.Rect(0, 512, 512, 88))
    screen.blit(text_object, text_location)
    py.display.update()

if __name__ == "__main__":
    main()



