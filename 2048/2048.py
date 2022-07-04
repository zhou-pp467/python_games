# by zhou_pp

import random


class Matrix2048():
    """ core logic of the game"""

    def __init__(self, column=4):
        self.column = column
        self.matrix = [[0 for _ in range(self.column)] for _ in range(self.column)]
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
        zero_coordinates = [(x, y) for x in range(self.column) for y in range(self.column) if matrix[x][y] == 0]
        if zero_coordinates:
            x, y = random.choice(zero_coordinates)
            matrix[x][y] = get_number()

    # check if game is over
    def game_over(self):
        # if there is 0 in matrix, game is not over
        if 0 in [i for li in self.matrix for i in li]:
            return False

        # if same numbers exist adjacently in one row, game is not over
        for i in range(self.column):
            for j in range(self.column - 1):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return False

        # if same numbers exist adjacently in one col, game is not over
        for i in range(self.column):
            for j in range(self.column - 1):
                if self.matrix[j][i] == self.matrix[j + 1][i]:
                    return False

        # else game is over
        return True

    # init game
    def init(self):
        self.score = 0
        self.matrix = [[0 for _ in range(self.column)] for _ in range(self.column)]
        self.generate_number()
        self.generate_number()

    # check if the movement is allowed
    def check_move(self, matrix):
        return matrix != self.matrix

    # make a movement
    def matrix_move(self, direction):
        original_matrix = self.matrix
        match direction:
            case 'U':
                self.move_up()
            case 'D':
                self.move_down()
            case 'L':
                self.move_left()
            case 'R':
                self.move_right()
        if self.matrix != original_matrix:
            self.generate_number()

    # move left and merge
    def move_left(self):
        matrix = self.matrix

        def move_left_(matrix):
            for row in matrix:
                row.remove(0)
                for _ in range(self.column - len(row)):
                    row.append(0)
            return matrix

        def merge_left(matrix):
            for row in matrix:
                for i in range(len(row) - 1):
                    if row[i] == row[i + 1] and row[i] != 0:
                        row[i] = 2 * row[i]
                        row[i + 1] = 0
                        self.score += row[i]
            return matrix

        matrix = move_left_(matrix)
        matrix = merge_left(matrix)
        matrix = move_left_(matrix)
        self.matrix = matrix

    # move right and merge
    def move_right(self):
        self.matrix = [row[::-1] for row in self.matrix]
        self.move_left()
        self.matrix = [row[::-1] for row in self.matrix]

    # move up and merge
    def move_up(self):
        self.matrix = [[self.matrix[y][x] for y in range(self.column)] for x in range(self.column)]
        self.move_left()
        self.matrix = [[self.matrix[y][x] for y in range(self.column)] for x in range(self.column)]

    # move down and merge
    def move_down(self):
        self.matrix = [self.matrix[::-1]]
        self.move_up()
        self.matrix = [self.matrix[::-1]]


class Window2048():

    def __init__(self, column=4):
        self.init_setting(column)
        self.data = Matrix2048(column)

    # init the settings
    def init_setting(self, column):
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


Window2048(4)
