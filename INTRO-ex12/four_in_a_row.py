###################################
# FILE: ex12.py
# WRITER: elia_hene, eh51195, 324502145
#        rotem_amsalem, ra260296, 207596297
# EXERCISE: intro2cs ex12 2017-2018
# DESCRIPTION: Four in a Row.
##################################

import sys
from gui import GUI
import socket


def check_argv():
    """
    :return: True if the parameters are correct and False otherwise.
    """
    if 3 <= len(sys.argv) <= 4:
        if 1000 <= int(sys.argv[2]) <= 65535:
            if sys.argv[1] == GUI.HUMAN or sys.argv[1] == GUI.COMPUTER:
                return True
    print("Illegal program arguments.")
    return False


def main():
    """
    this function creates two synchronized screens of the game at once.
    one of the server and the other of the client.
    """
    if check_argv():
        if len(sys.argv) == 3:
            gui = GUI(sys.argv[1], int(sys.argv[2]), True, ip=None)
            gui.create_board()
            gui.root.title("Server")
            if not gui.is_human():
                gui.ai.find_legal_move(gui.game, gui.update_game)
            gui.run_game()
        elif len(sys.argv) == 4:
            ip = socket.gethostbyname(socket.gethostname())
            gui = GUI(sys.argv[1], int(sys.argv[2]), False, ip)
            gui.create_board()
            gui.root.title("Client")
            if not gui.is_human():
                gui.ai.find_legal_move(gui.game, gui.update_game)
            gui.run_game()


if __name__ == '__main__':
    main()
