# by zhou_pp

import sys
import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_RETURN, MOUSEBUTTONDOWN
import pygame.gfxdraw
from collections import namedtuple

from AI import AI

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
    OUTER_BORDER_WIDTH + MARGIN_BETWEEN_BORDER_AND_WINDOW\
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

# to get next stone
offset = [(1, 0), (0, 1), (1, 1), (1, -1)]

# set player
Player = namedtuple('Player', ['Name', 'Stone_val', 'Color'])
black_player = Player('肥肥', 1, BLACK_STONE_COLOR)
white_player = Player('电脑', 2, WHITE_STONE_COLOR)

# point
Point = namedtuple('Point', ['x', 'y'])


# chess board logic
class Board():
    def __init__(self, lines):
        self.lines = lines
        self.board_matrix = [[0] * lines for _ in range(lines)]

    def winner(self, point, player):
        pass

    def is_empty(self, point):
        return self.board_matrix[point.y][point.x] == 0

    def drop(self, point, player):
        self.board_matrix[point.y][point.x] = player.Stone_val


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


def draw_info(screen, font, cur_runner, black_win_count, white_win_count):
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
               f'{black_player.Name} {"走" if cur_runner == black_player else ""}', BLUE_COLOR)
    print_text(screen, font, SCREEN_HEIGHT + STONE_ICON_RADIUS * 3,
               INNER_BORDER_Y_START + 4 + 3 * STONE_ICON_RADIUS,
               f'{white_player.Name} {"走" if cur_runner == white_player else ""}', BLUE_COLOR)

    print_text(screen, font, SCREEN_HEIGHT,
               SCREEN_HEIGHT - MARGIN_BETWEEN_BORDER_AND_WINDOW - 8 * STONE_ICON_RADIUS,
               '战况:',
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
               f'{black_win_count} 胜',
               BLUE_COLOR
               )
    print_text(screen, font, SCREEN_HEIGHT + STONE_ICON_RADIUS * 3,
               SCREEN_HEIGHT - MARGIN_BETWEEN_BORDER_AND_WINDOW - 2 * STONE_ICON_RADIUS,
               f'{white_win_count} 胜',
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
    if cur_player == black_player:
        return white_player
    else:
        return black_player


# main function
def main():
    pygame.init()

    black_win_count = 0
    white_win_count = 0

    cur_player = black_player
    winner = None

    info_font = pygame.font.Font('Kaiti.ttf', 32)
    res_msg_font = pygame.font.Font('Kaiti.ttf', 74)

    # create window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('肥肥的五子棋')

    # init board
    board = Board(DOTS_IN_A_LINE)

    # init computer player
    computer_player = AI(DOTS_IN_A_LINE, white_player)

    def restart_game():
        nonlocal winner, cur_player, board, computer_player
        winner = None
        cur_player = black_player
        board = Board(DOTS_IN_A_LINE)
        computer_player = AI(DOTS_IN_A_LINE, white_player)

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
                                    case '黑方':
                                        black_win_count += 1
                                    case '白方':
                                        white_win_count += 1
                                    case _:
                                        cur_player = get_next(cur_player)

        # draw UI
        draw_board(screen)
        draw_info(screen, info_font, cur_player, black_win_count, white_win_count)
        # draw stones
        for y in range(board.lines):
            for x in range(board.lines):
                match board.board_matrix[y][x]:
                    case black_player.Stone_val:
                        draw_stone(screen,
                                   (INNER_BORDER_X_START + x * GRID_SIZE, INNER_BORDER_Y_START + y * GRID_SIZE),
                                   STONE_RADIUS,
                                   black_player.Color
                                   )
                    case white_player.Stone_val:
                        draw_stone(screen,
                                   (INNER_BORDER_X_START + x * GRID_SIZE, INNER_BORDER_Y_START + y * GRID_SIZE),
                                   STONE_RADIUS,
                                   white_player.Color
                                   )
                    case _:
                        pass

        if winner:
            msg_width, msg_height = res_msg_font.size('某方获胜')
            print_text(screen,
                       res_msg_font,
                       (SCREEN_WIDTH - msg_width) // 2,
                       (SCREEN_HEIGHT - msg_height) // 2,
                       winner + "获胜",
                       RED_COLOR
                       )

        pygame.display.flip()


if __name__ == '__main__':
    main()
