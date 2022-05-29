import numpy as np
import json

from Tile import *

ARENA_WIDTH = 1000
ARENA_HEIGHT = 1000


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

        self.init_matrix_with_no_texture()

    def init_matrix_with_no_texture(self):
        for x in range(self.tile_count_x):
            for y in range(self.tile_count_y):
                self.matrix[x][y] = Tile(x, y)

    def render(self, painter):
        for x in range(self.tile_count_x):
            for y in range(self.tile_count_y):
                if self.matrix[x][y] is not None:
                    painter.drawImage(self.matrix[x][y].rect,
                                      self.matrix[x][y].texture)

    def loadMap(self, map_name):
        with open("maps/" + map_name + ".json") as f:
            data = json.load(f)
            for t in data:
                x = t["x"]
                y = t["y"]
                tile_type = t["type"]

                if tile_type == "Dirt":
                    self.matrix[x][y] = Dirt(x, y)
                elif tile_type == "Grass":
                    self.matrix[x][y] = Grass(x, y)
                elif tile_type == "Lava":
                    self.matrix[x][y] = Lava(x, y)
                elif tile_type == "Stone":
                    self.matrix[x][y] = Stone(x, y)
                elif tile_type == "Wall":
                    self.matrix[x][y] = Wall(x, y)
                elif tile_type == "Water":
                    self.matrix[x][y] = Water(x, y)
                else:
                    self.matrix[x][y] = Tile(x, y)

    def saveMap(self, map_name):
        map_file = open("maps/" + map_name + ".json", "w")
        map_file.write("[\n")
        for x in range(self.tile_count_x):
            for y in range(self.tile_count_y):
                if not (x == self.tile_count_x - 1
                        and y == self.tile_count_y - 1):
                    map_file.write(self.matrix[x][y].to_json_string() + ",\n")
                else:
                    map_file.write(self.matrix[x][y].to_json_string() + "\n")
        map_file.write("]")
        map_file.close()

    def set_tile(self, x, y, tile_type):
        if tile_type == "Dirt":
            self.matrix[x][y] = Dirt(x, y)
        elif tile_type == "Grass":
            self.matrix[x][y] = Grass(x, y)
        elif tile_type == "Lava":
            self.matrix[x][y] = Lava(x, y)
        elif tile_type == "Stone":
            self.matrix[x][y] = Stone(x, y)
        elif tile_type == "Wall":
            self.matrix[x][y] = Wall(x, y)
        elif tile_type == "Water":
            self.matrix[x][y] = Water(x, y)
        else:
            self.matrix[x][y] = Tile(x, y)
