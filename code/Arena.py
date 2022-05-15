import numpy as np
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QRect
import random

ARENA_WIDTH = 1000
ARENA_HEIGHT = 1000
TILE_WIDTH = 10
TILE_HEIGHT = 10


class Tile():
    texture = QImage("res/no_texture.png")

    def __init__(self, pos_x, pos_y):
        self.rect = QRect(pos_x * TILE_WIDTH,
                          pos_y * TILE_HEIGHT,
                          TILE_WIDTH,
                          TILE_HEIGHT)


class Dirt(Tile):
    texture = QImage("res/dirt_texture.png")


class Grass(Tile):
    texture = QImage("res/grass_texture.png")


class Lava(Tile):
    texture = QImage("res/lava_texture.png")


class Stone(Tile):
    texture = QImage("res/stone_texture.png")


class Wall(Tile):
    texture = QImage("res/wall_texture.png")


class Water(Tile):
    texture = QImage("res/water_texture.png")


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

        self.init_matrix()

    def init_matrix(self):
        for x in range(self.tile_count_x):
            for y in range(self.tile_count_y):
                self.matrix[x][y] = random.choices([Dirt(x, y), Grass(x, y),
                                                    Lava(x, y), Stone(x, y),
                                                    Wall(x, y), Water(x, y)],
                                                   weights=[0.3, 0.5, 0.05,
                                                            0.05, 0.05, 0.05]
                                                   )[0]

    def render(self, painter):
        for x in range(self.tile_count_x):
            for y in range(self.tile_count_y):
                painter.drawImage(self.matrix[x][y].rect,
                                  self.matrix[x][y].texture)
