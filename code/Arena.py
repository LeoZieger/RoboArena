import numpy as np
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QRect
import random

ARENA_WIDTH = 1000
ARENA_HEIGHT = 1000
TILE_WIDTH = 10
TILE_HEIGHT = 10


class Tile():
    def __init__(self, pos_x, pos_y):
        grey_scale = random.randint(150, 160)  # Greyscale for 'rock' look

        self.color = QColor.fromRgb(grey_scale, grey_scale, grey_scale)
        self.rect = QRect(pos_x * TILE_WIDTH,
                          pos_y * TILE_HEIGHT,
                          TILE_WIDTH,
                          TILE_HEIGHT)


class Arena():
    def __init__(self,
                 _arena_width=ARENA_WIDTH,
                 _arena_height=ARENA_HEIGHT,
                 _tile_width=TILE_WIDTH,
                 _tile_height=TILE_HEIGHT):

        self.arena_width = _arena_width
        self.arena_height = _arena_height
        self.tile_width = _tile_width
        self.tile_height = _tile_height

        # Number of tiles in x and y direction
        self.tile_count_x = int(self.arena_width / self.tile_width)
        self.tile_count_y = int(self.arena_height / self.tile_height)

        self.matrix = np.empty(shape=(self.tile_count_x,
                               self.tile_count_y),
                               dtype=Tile)

        # Filling matrix with Tiles
        for x in range(self.tile_count_x):
            for y in range(self.tile_count_y):
                self.matrix[x][y] = Tile(x, y)
