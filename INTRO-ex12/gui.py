###################################
# FILE: ex12.py
# WRITER: elia_hene, eh51195, 324502145
#        rotem_amsalem, ra260296, 207596297
# EXERCISE: intro2cs ex12 2017-2018
# DESCRIPTION: Four in a Row.
##################################

from game import Game
import tkinter as tk
import tkinter.messagebox
from communicator import Communicator
import ai
import sys


class GUI():
    """
    A class representing the game Graphical User Interface including all the
    graphics of the game and the visual parts, including popping messages,
    and painting ovals
    """

    HUMAN = "human"
    COMPUTER = "ai"
    OPENING_MSG = "WELCOME!"
    GAME_INSTRUCTIONS = "Please press at the button of the column you would " \
                        "like to put your disc in it."
    EXIT_MSG = "Exit"
    CANVAS_BACKGROUND = "MediumPurple1"
    EMPTY_OVAL = "white"
    SERVER_COLOR = "blue"
    CLIENT_COLOR = "red"
    WINNER_MARK = "gold"
    TITLE_MSG = "MESSAGE"
    WIN_MSG = "Congratulation, you won!"
    LOSE_MSG = "That's too bad, you lost!"
    DRAW_MSG = "It's a draw!"
    BOARD_HEIGHT = int(544)
    BOARD_WIDTH = int(634)
    FRAME_HEIGHT = int(1000)
    FRAME_WIDTH = int(1000)
    WIDGET_LOCATION = int(90)

    def __init__(self, player, port, server, ip=None):
        """
        a constructor of the graphics of the game
        :param player: either human of computer
        :param port: a number between 1000 and 65535
        :param server: a boolean value that is True for the server and False
        for the client.
        :param ip: None for the server and an ip for the client
        """
        self.game = Game()
        self.ai = ai.AI()
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root, height=self.FRAME_HEIGHT,
                              width=self.FRAME_WIDTH)
        self.game_board = tk.Canvas(self.frame, bg=self.CANVAS_BACKGROUND,
                                    height=self.BOARD_HEIGHT,
                                    width=self.BOARD_WIDTH)
        self.game_board.pack()
        self.game_board.place(x=200, y=50)
        self.__communicator = Communicator(self.root, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.handle_message)
        self.player = player
        self.server = server

    def is_human(self):
        """
        this function update the player to be human or computer considering
        what was given at the args line.
        :return: True if the player is human and False if the player is ai
        """
        if sys.argv[1] == self.COMPUTER:
            self.player = self.COMPUTER
            return False
        if sys.argv[1] == self.HUMAN:
            self.player = self.HUMAN
            return True

    def show_message(self, title, msg):
        """
        This is a method used to show messages in the game.
        :param title: The title of the message box.
        :type title: str
        :param msg: The message to show in the message box.
        :type msg: str
        """
        tk.messagebox.showinfo(str(title), str(msg))

    def end_game(self):
        """
        This ends the current game.
        """
        self.root.destroy()
        self.root.quit()

    def paint_oval(self, col, color):
        """
        this function painting the ovals at the color of the current player
        :param col: get the col that the player chose to paint
        :param color: the color of the player(each player has his own color
        :return: an oval at the size of all the ovals and at the color given
        """
        row = self.game.make_move(col) + 1
        self.game_board.create_oval(5 + col * self.WIDGET_LOCATION,
                                    5 + row * self.WIDGET_LOCATION,
                                    col * self.WIDGET_LOCATION + 95,
                                    row * self.WIDGET_LOCATION + 95,
                                    fill=color)

    def paint_winner_oval(self, row, col):
        """
        this function painting a winning oval with a gold outline.
        :param row: the row of the winning oval
        :param col: the col of the winning oval
        :return: a gold outline for a winning oval
        """
        self.game_board.create_oval(5 + col * self.WIDGET_LOCATION,
                                    5 + row * self.WIDGET_LOCATION,
                                    col * self.WIDGET_LOCATION + 95,
                                    row * self.WIDGET_LOCATION + 95,
                                    outline=self.WINNER_MARK, width=5)

    def mark_win(self):
        """
        this function activates the paint_winner_oval(that marking the ovals
        with a gold outline) at each one of the winning ovals.
        """
        if self.game.check_col()[0] in [self.game.PLAYER_ONE,
                                        self.game.PLAYER_TWO]:
            for row, col in self.game.check_col()[1]:
                self.paint_winner_oval(row, col)
        if self.game.check_row()[0] in [self.game.PLAYER_ONE,
                                        self.game.PLAYER_TWO]:
            for row, col in self.game.check_row()[1]:
                col = col - 1
                self.paint_winner_oval(row, col)
        if self.game.check_diagonals()[0] in [self.game.PLAYER_ONE,
                                              self.game.PLAYER_TWO]:
            for row, col in self.game.check_diagonals()[1]:
                self.paint_winner_oval(row, col)

    def win_step(self):
        """
        this function mark the winner discs, shows the winner the message
        that he won, send message to the other player that he lose and ends
        the game.
        """
        self.mark_win()
        self.show_message(self.TITLE_MSG, self.WIN_MSG)
        self.__communicator.send_message(self.LOSE_MSG)
        self.end_game()

    def lose_step(self):
        """
        this function mark the winner discs, shows the loser the message
        that he lose and ends the game.
        """
        self.mark_win()
        self.show_message(self.TITLE_MSG, self.LOSE_MSG)
        self.end_game()

    def update_game(self, col):
        """
        this function checks if the player is the server of the client and
        than checks if it is his turn. If so, it activate the paint_oval
        function with the col given and with the player color
        :param col: a col that the player chose to place his disc at
        :return: an painted oval at the color of the player and message at
        the end of the game(win of draw)
        """
        cur_player = self.game.get_current_player()
        if self.server:
            if cur_player == self.game.PLAYER_ONE:
                self.paint_oval(col, self.SERVER_COLOR)
                self.__communicator.send_message(col)
            if self.game.get_winner() == self.game.PLAYER_ONE:
                self.win_step()
        elif not self.server:
            if cur_player == self.game.PLAYER_TWO:
                self.paint_oval(col, self.CLIENT_COLOR)
                self.__communicator.send_message(col)
            if self.game.get_winner() == self.game.PLAYER_TWO:
                self.win_step()
        if self.game.get_winner() == self.game.DRAW:
            self.show_message(self.TITLE_MSG, self.DRAW_MSG)
            self.__communicator.send_message(self.DRAW_MSG)
            self.end_game()

    def create_board(self):
        """
        this function creates the screen-  the visual board. including it's
        labels and empty ovals.
        :return: the visual initial screen
        """
        label_start = tk.Label(self.root, text=self.OPENING_MSG,
                               font=('Arial', 18))
        label_start.pack()
        label_play = tk.Label(self.root, text=self.GAME_INSTRUCTIONS,
                              font=('David', 15))
        label_play.pack()
        for j in range(5, 600, 90):
            for i in range(5, 700, 90):
                self.game_board.create_oval(i, j, i + self.WIDGET_LOCATION,
                                            j + self.WIDGET_LOCATION,
                                            fill=self.EMPTY_OVAL)

    def handle_message(self, text=None):
        """
        this function receive a message from the other player that says
        where he put his disc and if the game ends it shows the matching
        message
        :param text: the string of the location that the player want's to
        put his disc at
        :return: the painting oval at the other player's screen and if the
        game ends it shows the matching message(win, lose or draw)
        """
        if text:
            if self.server:
                color = self.CLIENT_COLOR
                self.paint_oval(int(text), color)
                if not self.is_human():
                    self.ai.find_legal_move(self.game, self.update_game)
            elif not self.server:
                color = self.SERVER_COLOR
                self.paint_oval(int(text), color)
                if not self.is_human():
                    self.ai.find_legal_move(self.game, self.update_game)
        if self.game.get_winner() == self.game.PLAYER_ONE:
            if not self.server:
                self.lose_step()
        if self.game.get_winner() == self.game.PLAYER_TWO:
            if self.server:
                self.lose_step()
        if self.game.get_winner() == self.game.DRAW:
            self.show_message(self.TITLE_MSG, self.DRAW_MSG)
            self.end_game()

    def run_game(self):
        """
        this function runs the game.
        it creates the buttons of the columns and the quit button.
        :return: the updating screen, with the buttons so pressing on them
        will paint the wanted disc
        """
        col_but_lst = []
        for index in range(1, 8):
            col_but = tk.Button(self.frame, text=("col", index),
                                command=lambda x=index: self.update_game(x-1))
            col_but.pack()
            col_but_lst.append(col_but)
        for i in range(len(col_but_lst)):
            col_but_lst[i].place(x=235 + self.WIDGET_LOCATION * i, y=25)
        quit_but = tk.Button(self.root, text=self.EXIT_MSG,
                             command=self.end_game)
        quit_but.pack()
        quit_but.place(x=950, y=30)
        self.frame.pack()
        self.root.mainloop()
