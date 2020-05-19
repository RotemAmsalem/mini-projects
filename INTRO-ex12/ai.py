###################################
# FILE: ex12.py
# WRITER: elia_hene, eh51195, 324502145
#        rotem_amsalem, ra260296, 207596297
# EXERCISE: intro2cs ex12 2017-2018
# DESCRIPTION: Four in a Row.
##################################
import random

class AI():
    """
    this class responsible about the computer's moves.
    """
    MSG_NO_AI_MOVES = "No possible AI moves."

    def find_legal_move(self, g, func, timeout=None):
        """
        this function place the disc at a column it founds as possible. If
        there are no such columns, the function raise an exception.
        :param g: an object from the Game class that describe the logic of
        the game
        :param func: a 2nd order function that activating at the col the
        function founds
        :param timeout:
        :return: a legal move, means a col the disc would be placed at as a
        number between 0 to 6 that represent a column that is not full.
        """
        legal_col = []
        for index, col in enumerate(g.col_lst):
            if col < g.BOARD_COL - 1:
                legal_col.append(index)
        chosen_col = random.sample(legal_col, k=1)[0]
        if len(legal_col) == 0:
            raise Exception(self.MSG_NO_AI_MOVES)
        func(chosen_col)
        return chosen_col
