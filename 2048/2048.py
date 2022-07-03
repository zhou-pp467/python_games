# by zhou_pp

import random


class Matrix2048():
    """ core logic of the game"""

    def __init__(self):
        self.matrix = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.init()

    # generate new number
    def generate_number(self):

        # choose a number 10% 4; 90% 2
        def get_number():
            random_int = random.randint(1, 100)
            if random_int > 90:
                number = 4
            else:
                number = 2
            return number

        matrix = self.matrix
        zero_coordinates = [(x, y) for x in range(4) for y in range(4) if matrix[x][y] == 0]
        if zero_coordinates:
            x, y = random.choice(zero_coordinates)
            matrix[x][y] = get_number()

    # check if game is over
    def game_over(self):
        # if there is 0 in matrix, game is not over
        if 0 in [i for li in self.matrix for i in li]:
            return False

        # if same numbers exist adjacently in one row, game is not over
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j+1]:
                    return False

        # if same numbers exist adjacently in one col, game is not over
        for i in range(4):
            for j in range(3):
                if self.matrix[j][i] == self.matrix[j+1][i]:
                    return False

        # else game is over
        return True

    # init game
    def init(self):
        self.score = 0
        self.matrix = [[0 for _ in range(4)] for _ in range(4)]
        self.generate_number()
        self.generate_number()

    # move and merge
    def matrix_move(self):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass

    def move_down(self):
        pass

    def move_up(self):
        pass


class Window2048():

    def __init__(self):
        pass

    # init the settings
    def init_setting(self):
        pass

    # init the window
    def init_window(self):
        pass

    # update UI data
    def update_ui(self):
        pass

    # accept keyboard input
    def key_event(self):
        pass

    # reset the game
    def reset_game(self):
        pass

    # main function
    def main(self):
        pass


Matrix2048()
