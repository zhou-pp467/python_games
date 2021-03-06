# by zhou_pp

import sys
import random
import copy
import pygame
from pygame.locals import QUIT, KEYDOWN, K_RETURN, MOUSEBUTTONDOWN
import pygame.gfxdraw
from tkinter import messagebox
from collections import namedtuple

# board size
DOTS_IN_A_LINE = 19

# board style
GRID_SIZE = 30
OUTER_BORDER_WIDTH = 4
MARGIN_BETWEEN_BORDERS = 4
MARGIN_BETWEEN_BORDER_AND_WINDOW = 20
BORDER_LENGTH = (DOTS_IN_A_LINE - 1) * GRID_SIZE \
                + 2 * (MARGIN_BETWEEN_BORDERS + OUTER_BORDER_WIDTH)
INNER_BORDER_X_START = INNER_BORDER_Y_START = \
    OUTER_BORDER_WIDTH + MARGIN_BETWEEN_BORDER_AND_WINDOW \
    + MARGIN_BETWEEN_BORDERS + int(OUTER_BORDER_WIDTH / 2)

# stone radius
STONE_RADIUS = GRID_SIZE // 2 - 3

# window size
SCREEN_HEIGHT = BORDER_LENGTH + 2 * MARGIN_BETWEEN_BORDER_AND_WINDOW
SCREEN_WIDTH = SCREEN_HEIGHT + 200

# colors
BOARD_COLOR = (0xE3, 0x92, 0x65)
BLACK_STONE_COLOR = (45, 45, 45)
WHITE_STONE_COLOR = (219, 219, 219)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (200, 30, 30)
BLUE_COLOR = (30, 30, 200)

# info section style
STONE_ICON_RADIUS = GRID_SIZE // 2 + 3
INFO_POS_X = SCREEN_HEIGHT + 2 * STONE_ICON_RADIUS + 12

# to get nearby stone
pos_diffs = [(1, 0), (0, 1), (1, 1), (1, -1)]

# set player
Player = namedtuple('Player', ['Name', 'Stone_val', 'Color'])
player1 = None
player2 = None

# point
Point = namedtuple('Point', ['x', 'y'])


# chess board logic
class Board():
    def __init__(self, lines):
        self.lines = lines
        self.board_matrix = [[0] * lines for _ in range(lines)]
        self.last_move = None

    def winner(self, point, player):
        board_matrix = self.board_matrix
        val = player.Stone_val

        # check if five-in-a-row in each direction
        for pos_diff in pos_diffs:
            count = 1
            for i in range(1, 5):
                x = point.x + pos_diff[0] * i
                y = point.y + pos_diff[1] * i
                if 0 <= x < self.lines and 0 <= y < self.lines and board_matrix[y][x] == val:
                    count += 1
                else:
                    break
            for i in range(1, 5):
                x = point.x - pos_diff[0] * i
                y = point.y - pos_diff[1] * i
                if 0 <= x < self.lines and 0 <= y < self.lines and board_matrix[y][x] == val:
                    count += 1
                else:
                    break
            if count >= 5:
                return player.Name

    def is_empty(self, point):
        return self.board_matrix[point.y][point.x] == 0

    def drop(self, point, player):
        self.board_matrix[point.y][point.x] = player.Stone_val
        self.last_move = point


def draw_board(screen):
    """Draw board."""
    screen.fill(BOARD_COLOR)

    # outer border
    pygame.draw.rect(screen, BLACK_COLOR,
                     (
                         MARGIN_BETWEEN_BORDER_AND_WINDOW + OUTER_BORDER_WIDTH // 2,
                         MARGIN_BETWEEN_BORDER_AND_WINDOW + OUTER_BORDER_WIDTH // 2,
                         BORDER_LENGTH,
                         BORDER_LENGTH
                     ), OUTER_BORDER_WIDTH)

    # inner lines
    for row in range(DOTS_IN_A_LINE):
        pygame.draw.line(screen, BLACK_COLOR,
                         (INNER_BORDER_X_START, row * GRID_SIZE + INNER_BORDER_X_START),
                         (
                             INNER_BORDER_Y_START + (DOTS_IN_A_LINE - 1) * GRID_SIZE,
                             row * GRID_SIZE + INNER_BORDER_Y_START
                         ),
                         1)
    for col in range(DOTS_IN_A_LINE):
        pygame.draw.line(screen, BLACK_COLOR,
                         (INNER_BORDER_X_START + col * GRID_SIZE, INNER_BORDER_Y_START),
                         (
                             INNER_BORDER_X_START + col * GRID_SIZE,
                             (DOTS_IN_A_LINE - 1) * GRID_SIZE + INNER_BORDER_Y_START
                         ),
                         1)

    # draw special positions
    for i in [3, 9, 15]:
        for j in [3, 9, 15]:
            if i == 9 and j == 9:
                radius = 5
            else:
                radius = 3
            pygame.gfxdraw.aacircle(
                screen,
                INNER_BORDER_X_START + i * GRID_SIZE,
                INNER_BORDER_Y_START + j * GRID_SIZE,
                radius,
                BLACK_COLOR
            )
            pygame.gfxdraw.filled_circle(
                screen,
                INNER_BORDER_X_START + i * GRID_SIZE,
                INNER_BORDER_Y_START + j * GRID_SIZE,
                radius,
                BLACK_COLOR
            )


def draw_stone(screen, pos, stone_radius, stone_color):
    """Draw stones."""
    pygame.gfxdraw.aacircle(
        screen,
        pos[0],
        pos[1],
        stone_radius,
        stone_color
    )
    pygame.gfxdraw.filled_circle(
        screen,
        pos[0],
        pos[1],
        stone_radius,
        stone_color
    )


def print_text(screen, font, x, y, text, font_color):
    img_text = font.render(text, True, font_color)
    screen.blit(img_text, (x, y))


def draw_info(screen, font, cur_runner, player1_win_count, player2_win_count):
    """Draw info section."""
    draw_stone(screen,
               (SCREEN_HEIGHT + STONE_ICON_RADIUS,
                INNER_BORDER_Y_START + STONE_ICON_RADIUS),
               STONE_ICON_RADIUS,
               BLACK_STONE_COLOR)
    draw_stone(screen,
               (SCREEN_HEIGHT + STONE_ICON_RADIUS,
                INNER_BORDER_Y_START + STONE_ICON_RADIUS * 4),
               STONE_ICON_RADIUS,
               WHITE_STONE_COLOR)

    print_text(screen, font, SCREEN_HEIGHT + STONE_ICON_RADIUS * 3,
               INNER_BORDER_Y_START + 4,
               f'{player1.Name} {"???" if cur_runner == player1 else ""}', BLUE_COLOR)
    print_text(screen, font, SCREEN_HEIGHT + STONE_ICON_RADIUS * 3,
               INNER_BORDER_Y_START + 4 + 3 * STONE_ICON_RADIUS,
               f'{player2.Name} {"???" if cur_runner == player2 else ""}', BLUE_COLOR)

    print_text(screen, font, SCREEN_HEIGHT,
               SCREEN_HEIGHT - MARGIN_BETWEEN_BORDER_AND_WINDOW - 8 * STONE_ICON_RADIUS,
               '??????:',
               BLUE_COLOR
               )

    draw_stone(screen,
               (SCREEN_HEIGHT + STONE_ICON_RADIUS,
                SCREEN_HEIGHT - MARGIN_BETWEEN_BORDER_AND_WINDOW - 4 * STONE_ICON_RADIUS),
               STONE_ICON_RADIUS,
               BLACK_STONE_COLOR)
    draw_stone(screen,
               (SCREEN_HEIGHT + STONE_ICON_RADIUS,
                SCREEN_HEIGHT - MARGIN_BETWEEN_BORDER_AND_WINDOW - STONE_ICON_RADIUS),
               STONE_ICON_RADIUS,
               WHITE_STONE_COLOR)

    print_text(screen, font, SCREEN_HEIGHT + STONE_ICON_RADIUS * 3,
               SCREEN_HEIGHT - MARGIN_BETWEEN_BORDER_AND_WINDOW - 5 * STONE_ICON_RADIUS,
               f'{player1_win_count} ???',
               BLUE_COLOR
               )
    print_text(screen, font, SCREEN_HEIGHT + STONE_ICON_RADIUS * 3,
               SCREEN_HEIGHT - MARGIN_BETWEEN_BORDER_AND_WINDOW - 2 * STONE_ICON_RADIUS,
               f'{player2_win_count} ???',
               BLUE_COLOR
               )


def get_click_point(click_pos):
    """Get point from position."""
    pos_x = click_pos[0] - INNER_BORDER_X_START
    pos_y = click_pos[1] - INNER_BORDER_Y_START
    if pos_x < - MARGIN_BETWEEN_BORDERS or pos_x > (DOTS_IN_A_LINE - 1) * GRID_SIZE or \
            pos_y < - MARGIN_BETWEEN_BORDERS or pos_y > (DOTS_IN_A_LINE - 1) * GRID_SIZE:
        return None
    x = pos_x // GRID_SIZE
    y = pos_y // GRID_SIZE
    if pos_x % GRID_SIZE > STONE_RADIUS:
        x += 1
    if pos_y % GRID_SIZE > STONE_RADIUS:
        y += 1
    return Point(x, y)


def get_next(cur_player):
    """Get next player."""
    if cur_player == player1:
        return player2
    else:
        return player1


# computer player
class AI():
    def __init__(self, lines, player):
        self.lines = lines
        self.my = player
        self.opponent = player1 if player == player2 else player2
        self.board_matrix = [[0] * lines for _ in range(lines)]

    def get_opponent_drop(self, point):
        self.board_matrix[point.y][point.x] = self.opponent.Stone_val

    def drop(self):
        board_matrix = copy.deepcopy(self.board_matrix)
        # if first move drop in center
        if board_matrix == [[0] * self.lines for _ in range(self.lines)]:
            self.board_matrix[9][9] = self.my.Stone_val
            return Point(9, 9)
        # choose a point to drop
        point = None
        score = 0
        for i in range(self.lines):
            for j in range(self.lines):
                if board_matrix[j][i] == 0:
                    _score = self.get_point_score(Point(i, j))
                    if _score > score:
                        score = _score
                        point = Point(i, j)
                    elif _score == score:
                        if random.randint(0, 1):
                            point = Point(i, j)
        self.board_matrix[point.y][point.x] = self.my.Stone_val
        return point

    def get_point_score(self, point):
        score = 0
        for pos_diff in pos_diffs:
            score += self.get_direction_score(point, pos_diff[0], pos_diff[1])
        return score

    def get_stone_color(self, point, x_diff, y_diff, next):
        """Return side of point, my:1, opponent:2."""
        x = point.x + x_diff
        y = point.y + y_diff
        if 0 <= x < self.lines and 0 <= y < self.lines:
            if self.board_matrix[y][x] == self.my.Stone_val:
                return 1
            elif self.board_matrix[y][x] == self.opponent.Stone_val:
                return 2
            else:
                # if blank, return side of next point
                if next:
                    return self.get_stone_color(Point(x, y), x_diff, y_diff, False)
                else:
                    return 0

    def get_direction_score(self, point, x_diff, y_diff):
        # continuous stones of my
        count = 0
        # continuous stones of opponent
        _count = 0
        # if space exists between my continuous stones
        space = None
        # if space exists between opponent continuous stones
        _space = None
        # blocked at ends of my continuous stones
        end = 0
        # blocked at ends of opponent continuous stones
        _end = 0

        # check one side of stone in direction
        flag = self.get_stone_color(point, x_diff, y_diff, True)
        if flag != 0:
            for step in range(1, 6):
                x = point.x + step * x_diff
                y = point.y + step * y_diff
                if 0 <= x < self.lines and 0 <= y < self.lines:
                    if flag == 1:
                        if self.board_matrix[y][x] == self.my.Stone_val:
                            count += 1
                            # space exists
                            if space is False:
                                space = True
                        elif self.board_matrix[y][x] == self.opponent.Stone_val:
                            # can block opponent
                            _end += 1
                            break
                        else:
                            # maybe generate a space
                            if space is None:
                                space = False
                            # two blanks, break
                            else:
                                break
                    elif flag == 2:
                        if self.board_matrix[y][x] == self.my.Stone_val:
                            _end += 1
                            break
                        elif self.board_matrix[y][x] == self.opponent.Stone_val:
                            _count += 1
                            # space exists
                            if _space is False:
                                _space = True
                        else:
                            # maybe generate a space
                            if _space is None:
                                _space = False
                            else:
                                # two blanks, break
                                break
                else:
                    # blocked by edges
                    if flag == 1:
                        end += 1
                    elif flag == 2:
                        _end += 1

        # did not generate space, reset
        if space is False:
            space = None
        if _space is False:
            space = None

        # check other side of stone in direction
        _flag = self.get_stone_color(point, -x_diff, -y_diff, True)
        if _flag != 0:
            for step in range(1, 6):
                x = point.x - step * x_diff
                y = point.y - step * y_diff
                if 0 <= x < self.lines and 0 <= y < self.lines:
                    if _flag == 1:
                        if self.board_matrix[y][x] == self.my.Stone_val:
                            count += 1
                            if space is False:
                                space = True
                        elif self.board_matrix[y][x] == self.opponent.Stone_val:
                            _end += 1
                            break
                        else:
                            if space is None:
                                space = False
                            else:
                                break
                    elif _flag == 2:
                        if self.board_matrix[y][x] == self.my.Stone_val:
                            _end += 1
                            break
                        elif self.board_matrix[y][x] == self.opponent.Stone_val:
                            _count += 1
                            if _space is False:
                                _space = True
                        else:
                            if _space is None:
                                _space = False
                            else:
                                break
                else:
                    if _flag == 1:
                        end += 1
                    elif _flag == 2:
                        _end += 1
        # my four-in-a-row
        if count == 4:
            score = 10000
        # opponent four-in-a-row
        elif _count == 4:
            score = 9000
        elif count == 3:
            # my three-in-a-row with no block
            if end == 0:
                score = 1000
            # my three-in-a-row with one block
            elif end == 1:
                score = 100
            # my three-in-a-row with two blocks
            else:
                score = 0
        elif _count == 3:
            # opponent three-in-a-row with no block
            if _end == 0:
                score = 900
            # opponent three-in-a-row with one block
            elif _end == 1:
                score = 90
            # opponent three-in-a-row with two blocks
            else:
                score = 0
        elif count == 2:
            # my two-in-a-row with no block
            if end == 0:
                score = 100
            # my two-in-a-row with one block
            elif end == 1:
                score = 10
            # my two-in-a-row with two blocks
            else:
                score = 0
        elif _count == 2:
            # opponent two-in-a-row with no block
            if _end == 0:
                score = 100
            # opponent two-in-a-row with one block
            elif _end == 1:
                score = 10
            # opponent two-in-a-row with two blocks
            else:
                score = 0
        elif count == 1:
            score = 10
        elif _count == 1:
            score = 9
        else:
            score = 0

        # half of score if space exists
        if space or _space:
            score /= 2

        return score


# main function
def main():
    # choose mode
    is_ai_mode = messagebox.askokcancel(title='????????????', message='??????????????????????')
    is_black_player = messagebox.askokcancel(title='????????????', message='?????????????????????????')

    pygame.init()

    player1_win_count = 0
    player2_win_count = 0

    winner = None

    info_font = pygame.font.Font('Kaiti.ttf', 32)
    res_msg_font = pygame.font.Font('Kaiti.ttf', 74)

    # create window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('??????????????????')

    # init board
    board = Board(DOTS_IN_A_LINE)

    # create players
    computer_player = None
    global player2, player1
    match (is_ai_mode, is_black_player):
        case (True, True):
            player1 = Player('??????', 1, BLACK_STONE_COLOR)
            player2 = Player('??????', 2, WHITE_STONE_COLOR)
            computer_player = AI(DOTS_IN_A_LINE, player2)
        case (True, False):
            player1 = Player('??????', 1, BLACK_STONE_COLOR)
            player2 = Player('??????', 2, WHITE_STONE_COLOR)
            computer_player = AI(DOTS_IN_A_LINE, player1)
        case (False, False):
            player1 = Player('??????', 1, BLACK_STONE_COLOR)
            player2 = Player('??????', 2, WHITE_STONE_COLOR)
        case (False, True):
            player1 = Player('??????', 1, BLACK_STONE_COLOR)
            player2 = Player('??????', 2, WHITE_STONE_COLOR)

    cur_player = player1

    def restart_game():
        global player1, player2
        nonlocal winner, cur_player, board, computer_player
        winner = None
        cur_player = player1
        board = Board(DOTS_IN_A_LINE)
        if computer_player and is_black_player:
            computer_player = AI(DOTS_IN_A_LINE, player2)
        elif computer_player and not is_black_player:
            computer_player = AI(DOTS_IN_A_LINE, player1)
            computer_drop = computer_player.drop()
            board.drop(computer_drop, cur_player)
            cur_player = get_next(cur_player)

    # if computer drop first
    if computer_player and not is_black_player:
        computer_drop = computer_player.drop()
        board.drop(computer_drop, cur_player)
        cur_player = get_next(cur_player)

    while True:
        for event in pygame.event.get():
            # exit game
            if event.type == QUIT:
                sys.exit()
            # press enter to restart game when game over
            elif event.type == KEYDOWN and event.key == K_RETURN:
                if winner:
                    restart_game()
            # click mouse to drop stone
            elif event.type == MOUSEBUTTONDOWN:
                if not winner:
                    pressed_buttons = pygame.mouse.get_pressed()
                    if pressed_buttons[0]:
                        pos = pygame.mouse.get_pos()
                        point = get_click_point(pos)
                        # point is valid
                        if point:
                            # point is empty
                            if board.is_empty(point):
                                board.drop(point, cur_player)
                                # winner name as str
                                winner = board.winner(point, cur_player)
                                match winner:
                                    case player1.Name:
                                        player1_win_count += 1
                                    case player2.Name:
                                        player2_win_count += 1
                                    case _:
                                        cur_player = get_next(cur_player)

                                        if computer_player:
                                            computer_player.get_opponent_drop(point)
                                            # get computer drop
                                            computer_drop = computer_player.drop()
                                            # drop computer drop on board
                                            board.drop(computer_drop, cur_player)
                                            # winner name as str
                                            winner = board.winner(computer_drop, cur_player)
                                            match winner:
                                                case player1.Name:
                                                    player1_win_count += 1
                                                case player2.Name:
                                                    player2_win_count += 1
                                                case _:
                                                    cur_player = get_next(cur_player)

        # draw UI
        draw_board(screen)
        draw_info(screen, info_font, cur_player, player1_win_count, player2_win_count)
        # draw stones
        for y in range(board.lines):
            for x in range(board.lines):
                match board.board_matrix[y][x]:
                    case player1.Stone_val:
                        draw_stone(screen,
                                   (INNER_BORDER_X_START + x * GRID_SIZE, INNER_BORDER_Y_START + y * GRID_SIZE),
                                   STONE_RADIUS,
                                   player1.Color
                                   )
                    case player2.Stone_val:
                        draw_stone(screen,
                                   (INNER_BORDER_X_START + x * GRID_SIZE, INNER_BORDER_Y_START + y * GRID_SIZE),
                                   STONE_RADIUS,
                                   player2.Color
                                   )
                    case _:
                        pass
        # draw last move
        if board.last_move:
            draw_stone(screen,
                       (board.last_move[0] * GRID_SIZE + INNER_BORDER_X_START,
                        board.last_move[1] * GRID_SIZE + INNER_BORDER_Y_START),
                       5,
                       RED_COLOR
                       )

        if winner:
            msg_width, msg_height = res_msg_font.size('????????????')
            print_text(screen,
                       res_msg_font,
                       (SCREEN_WIDTH - msg_width) // 2,
                       (SCREEN_HEIGHT - msg_height) // 2,
                       winner + "??????",
                       RED_COLOR
                       )

        pygame.display.flip()


if __name__ == '__main__':
    main()
