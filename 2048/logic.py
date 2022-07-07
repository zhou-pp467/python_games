# by zhou_pp

import copy
import random


class Matrix2048():
    """ core logic of the game"""

    def __init__(self, column=4):
        self.column = column
        self.matrix = [[0 for _ in range(self.column)]
                       for _ in range(self.column)]
        self.score = 0
        self.init()

    # generate new number
    def __generate_number(self):

        # choose a number 10% 4; 90% 2
        def get_number():
            random_int = random.randint(1, 100)
            if random_int > 90:
                number = 4
            else:
                number = 2
            return number

        matrix = self.matrix
        zero_coordinates = [(x, y) for x in range(self.column)
                            for y in range(self.column) if matrix[x][y] == 0]
        if zero_coordinates:
            x, y = random.choice(zero_coordinates)
            matrix[x][y] = get_number()

    # check if game is over
    def game_over(self):
        matrix = copy.deepcopy(self.matrix)
        # if there is 0 in matrix, game is not over
        if 0 in [i for li in matrix for i in li]:
            return False

        # if same numbers exist adjacently in one row, game is not over
        for i in range(self.column):
            for j in range(self.column - 1):
                if matrix[i][j] == matrix[i][j + 1]:
                    return False

        # if same numbers exist adjacently in one col, game is not over
        for i in range(self.column):
            for j in range(self.column - 1):
                if matrix[j][i] == matrix[j + 1][i]:
                    return False

        # else game is over
        return True

    # init game
    def init(self):
        self.score = 0
        self.matrix = [[0 for _ in range(self.column)]
                       for _ in range(self.column)]
        self.__generate_number()
        self.__generate_number()

    # make a movement
    def matrix_move(self, direction):
        original_matrix = copy.deepcopy(self.matrix)
        match direction:
            case 'U':
                self.__move_up()
            case 'D':
                self.__move_down()
            case 'L':
                self.__move_left()
            case 'R':
                self.__move_right()
        if self.matrix != original_matrix:
            self.__generate_number()

    # move left and merge
    def __move_left(self):
        matrix = self.matrix

        def move_left_(matrix):
            for row in matrix:
                while 0 in row:
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
    def __move_right(self):
        self.matrix = [row[::-1] for row in self.matrix]
        self.__move_left()
        self.matrix = [row[::-1] for row in self.matrix]

    # move up and merge
    def __move_up(self):
        self.matrix = [[self.matrix[y][x]
                        for y in range(self.column)]
                       for x in range(self.column)]
        self.__move_left()
        self.matrix = [[self.matrix[y][x]
                        for y in range(self.column)]
                       for x in range(self.column)]

    # move down and merge
    def __move_down(self):
        self.matrix = self.matrix[::-1]
        self.__move_up()
        self.matrix = self.matrix[::-1]


