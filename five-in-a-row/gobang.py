# by zhou_pp

import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, K_RETURN, MOUSEBUTTONDOWN
import pygame.gfxdraw
from collections import namedtuple

# board size
DOTS_IN_A_LINE = 19

# board style
SPACE_BETWEEN_DOTS = 30
OUTER_BORDER_WIDTH = 4
MARGIN_BETWEEN_BORDERS = 4
MARGIN_BETWEEN_BORDER_AND_WINDOW = 20
BORDER_LENGTH = (DOTS_IN_A_LINE - 1) * SPACE_BETWEEN_DOTS \
                + 2 * (MARGIN_BETWEEN_BORDERS + OUTER_BORDER_WIDTH)
INNER_BORDER_X_START = INNER_BORDER_Y_START = \
    OUTER_BORDER_WIDTH + MARGIN_BETWEEN_BORDERS + int(OUTER_BORDER_WIDTH / 2)

# stone radius
STONE_RADIUS = SPACE_BETWEEN_DOTS // 2 - 3

# window size
SCREEN_HEIGHT = BORDER_LENGTH + 2 * MARGIN_BETWEEN_BORDER_AND_WINDOW
SCREEN_WIDTH = SCREEN_HEIGHT + 200

# colors
BOARD_COLOR = (0xE3, 0x92, 0x65)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (200, 30, 30)
BLUE_COLOR = (30, 30, 200)

# info section style
STONE_ICON_RADIUS = SPACE_BETWEEN_DOTS // 2 + 3
INFO_POS_X = SCREEN_HEIGHT + 2 * STONE_ICON_RADIUS + 12

# to get next stone
offset = [(1, 0), (0, 1), (1, 1), (1, -1)]

# set player
Player = namedtuple('Player', ['Name', 'Stone_val', 'Color'])
black_player = Player('肥肥', 1, BLACK_COLOR)
white_player = Player('电脑', 2, WHITE_COLOR)


# chess board
class Board():
    pass


# computer player
class AI():
    pass


def draw_board(screen):
    """Draw board."""



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
               BLACK_COLOR)
    draw_stone(screen,
               (SCREEN_HEIGHT + STONE_ICON_RADIUS,
                INNER_BORDER_Y_START + STONE_ICON_RADIUS * 4),
               STONE_ICON_RADIUS,
               WHITE_COLOR)

    print_text(screen, font, SCREEN_HEIGHT + STONE_ICON_RADIUS * 3,
               INNER_BORDER_Y_START + 3,
               f'{black_player.Name} {"走" if cur_runner == black_player else ""}', BLUE_COLOR)
    print_text(screen, font, SCREEN_HEIGHT + STONE_ICON_RADIUS * 3,
               INNER_BORDER_Y_START + 3 + 3 * STONE_ICON_RADIUS,
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
               BLACK_COLOR)
    draw_stone(screen,
               (SCREEN_HEIGHT + STONE_ICON_RADIUS,
                SCREEN_HEIGHT - MARGIN_BETWEEN_BORDER_AND_WINDOW - STONE_ICON_RADIUS),
               STONE_ICON_RADIUS,
               WHITE_COLOR)

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


# main function
def main():
    pygame.init()

    black_win_count = 1
    white_win_count = 0
    cur_runner = black_player

    info_font = pygame.font.Font('Kaiti.ttf', 32)
    res_msg_font = pygame.font.Font('Kaiti.ttf', 74)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('肥肥的五子棋')

    draw_board(screen)
    draw_info(screen, info_font, cur_runner, black_win_count, white_win_count)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()


if __name__ == '__main__':
    main()
