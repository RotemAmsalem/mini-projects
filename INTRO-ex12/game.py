###################################
# FILE: ex12.py
# WRITER: elia_hene, eh51195, 324502145
#        rotem_amsalem, ra260296, 207596297
# EXERCISE: intro2cs ex12 2017-2018
# DESCRIPTION: Four in a Row.
##################################


class Game:
    """
    A class representing the "internal logic" of the board state, and will
    allow to perform moves on the board, when the board size is 6 row and 7
    column. A player wins when 4 discs he has inserted are a row, column or
    diagonal on the board.
    """
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    BOARD_ROW = 6
    BOARD_COL = 7
    MSG_ILLEGAL_MOVE = "Illegal move."
    FULL_BOARD = [6, 6, 6, 6, 6, 6, 6]  # six disc in every column

    def __init__(self):
        """
        A constructor for the board of the game.
        """
        self.board = {}
        for row in range(Game.BOARD_ROW):
            for col in range(Game.BOARD_COL):
                self.board[row, col] = None
        self.col_lst = []
        for i in range(Game.BOARD_COL):
            self.col_lst.append(0)

    def make_move(self, column):
        """
        Updating the board dictionary depending on the column player's
        selection.
        :param column: the column the player chose for his disc.
        :return: the row corresponding to the selected column, which the
        disc is clipped.
        """
        if self.col_lst[column] >= Game.BOARD_ROW:  # if the column is full
            raise Exception(Game.MSG_ILLEGAL_MOVE)
        else:
            self.board[self.BOARD_ROW - 1 - self.col_lst[column],
                       column] = self.get_current_player()
            self.col_lst[column] += 1
            return self.BOARD_ROW - 1 - self.col_lst[column]

    def get_current_player(self):
        """
        :return: the current player at a given moment.
        """
        counter = 0
        for disc in self.col_lst:
            counter += disc
        if counter % 2 == 0:  # checks if the number of disc is even or odd
            return self.PLAYER_ONE
        else:
            return self.PLAYER_TWO

    def get_player_at(self, row, col):
        """
        :param row: the index of the row in the board.
        :param col: the index of the col in the board.
        :return: which disc is in the selected location.
        """
        return self.board[row, col]

    def check_row(self):
        """
        this function checks if there are four disc from the same color in
        consecutively at any one of the rows.
        :return: the winner, if there is one, or None otherwise and a list
        of the locations of the winning discs as a tuple.
        """
        index_lst = []
        for row in range(Game.BOARD_ROW):
            for col in range(Game.BOARD_COL):
                if col <= Game.BOARD_COL - 4:
                    if self.board[row, col] == self.board[row, col + 1] == \
                            self.board[row, col + 2] == self.board[row,
                                                                   col + 3] \
                            is not None:  # check a row from left to right.
                        index_lst = [(row, col + 1), (row, col + 2),
                                     (row, col + 3), (row, col + 4)]
                        return self.get_player_at(row, col), index_lst
        return None, index_lst

    def check_col(self):
        """
        this function checks if there are four disc from the same color in
        consecutively at any one of the columns.
        :return: the winner, if there is one, or None otherwise and a list
        of the locations of the winning discs as a tuple.
        """
        index_lst = []
        for row in range(Game.BOARD_ROW):
            for col in range(Game.BOARD_COL):
                if row >= Game.BOARD_ROW - 3:
                    if self.board[row, col] == self.board[row - 1, col] == \
                            self.board[row - 2, col] == self.board[
                                row - 3, col] is \
                            not None:  # check a column from down to up.
                        index_lst = [(row, col), (row - 1, col),
                                     (row - 2, col),
                                     (row - 3, col)]
                        return self.get_player_at(row, col), index_lst
        return None, index_lst

    def check_diagonals(self):
        """
        this function checks if there are four disc from the same color in
        consecutively at either one of the diagonals.
        :return: the winner if there is one and None otherwise and a list
        of the locations of the winning discs.
        """
        index_lst = []
        for row in range(Game.BOARD_ROW):
            for col in range(Game.BOARD_COL):
                if row >= Game.BOARD_ROW - 3 and col <= Game.BOARD_COL - 4:
                    if self.board[row, col] == self.board[row - 1, col + 1] \
                            == self.board[row - 2, col + 2] == self.board[
                                row - 3, col + 3] is not None:  # check a
                        # diagonal from left-down to right-up.
                        index_lst = [(row, col), (row - 1, col + 1),
                                     (row - 2, col + 2), (row - 3, col + 3)]
                        return self.get_player_at(row, col), index_lst
                if row >= Game.BOARD_ROW - 3 and col >= Game.BOARD_COL - 4:
                    if self.board[row, col] == self.board[row - 1, col - 1] \
                            == self.board[row - 2, col - 2] == self.board[
                                row - 3, col - 3] is not None:  # check a
                        # diagonal from right-down to up-left.
                        index_lst = [(row, col), (row - 1, col - 1),
                                     (row - 2, col - 2),(row - 3, col - 3)]
                        return self.get_player_at(row, col), index_lst
        return None, index_lst

    def get_winner(self):
        """
        :return: the situation won: the winner in case of victory, and draw
        in case of a draw (if there is no winner neither at the rows or
        columns nor at the diagonals).
        """
        if self.check_row()[0] in [self.PLAYER_ONE, self.PLAYER_TWO]:
            return self.check_row()[0]
        elif self.check_col()[0] in [self.PLAYER_ONE, self.PLAYER_TWO]:
            return self.check_col()[0]
        elif self.check_diagonals()[0] in [self.PLAYER_ONE, self.PLAYER_TWO]:
            return self.check_diagonals()[0]
        elif self.col_lst == self.FULL_BOARD:
            return self.DRAW
        return None
