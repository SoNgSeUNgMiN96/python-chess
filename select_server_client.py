import chess_client
import chess_server
import threading

def mainMethod():
    while True:
        try:
            server_client = input("choose >> (server or client)?\n")
            if server_client == "server":
                chess_server_main_thread = threading.Thread(target=chess_server.mainMethod, args=())
                chess_server_main_thread.start()
                break
            elif server_client == "client":
                chess_client_main_thread = threading.Thread(target=chess_client.mainMethod, args=())
                chess_client_main_thread.start()
                break
            else:
                print("Enter server or client.\n")
        except ValueError:
            print("Enter server or client.")
    print("select_server_client_exit")
    return

