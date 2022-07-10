# by zhou_pp

import random
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


# computer player
class AI():
    def __init__(self, lines, player):
        pass

    def get_opponent_drop(self, point):
        pass

    def drop(self):
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        return Point(x, y)