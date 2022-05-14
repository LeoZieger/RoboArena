import numpy as np

ARENA_WIDTH = 1000
ARENA_HEIGHT = 1000

TILE_WIDTH = 10
TILE_HEIGHT = 10

TILE_COUNT_X = ARENA_WIDTH / TILE_WIDTH
TILE_COUNT_Y = ARENA_HEIGHT / TILE_HEIGHT

class Arena():
    self.matrix = np.zeros(TILE_COUNT_X, TILE_COUNT_Y)

    def __init__(self):
        for x in range(TILE_COUNT_X):
            for y in range(TILE_COUNT_Y):
                self.matrix[x][y] = Tile()

class Tile():
    self.color = (255, 0, 0)