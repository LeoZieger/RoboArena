import numpy as np
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QRect
import random
import json

ARENA_WIDTH = 1000
ARENA_HEIGHT = 1000
TILE_WIDTH = 10
TILE_HEIGHT = 10


class Tile():
    texture = QImage("res/no_texture.png")
    tile_type = "None"

    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y

        self.rect = QRect(self.x * TILE_WIDTH,
                          self.y * TILE_HEIGHT,
                          TILE_WIDTH,
                          TILE_HEIGHT)

    def to_json_string(self):
        json_str = "{"
        json_str += '"type":"{}", "x":{}, "y":{}'.format(self.tile_type,
                                                         self.x,
                                                         self.y)
        json_str += "}"
        return json_str


class Dirt(Tile):
    tile_type = "Dirt"
    texture = QImage("res/dirt_texture.png")


class Grass(Tile):
    tile_type = "Grass"
    texture = QImage("res/grass_texture.png")


class Lava(Tile):
    tile_type = "Lava"
    texture = QImage("res/lava_texture.png")


class Stone(Tile):
    tile_type = "Stone"
    texture = QImage("res/stone_texture.png")


class Wall(Tile):
    tile_type = "Wall"
    texture = QImage("res/wall_texture.png")


class Water(Tile):
    tile_type = "Water"
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

        self.init_matrix_with_no_texture()

    def init_matrix_with_no_texture(self):
        for x in range(self.tile_count_x):
            for y in range(self.tile_count_y):
                self.matrix[x][y] = Tile(x, y)

    def init_matrix_random(self):
        for x in range(self.tile_count_x):
            for y in range(self.tile_count_y):
                self.matrix[x][y] = random.choices([Dirt(x, y), Grass(x, y),
                                                    Lava(x, y), Stone(x, y),
                                                    Wall(x, y), Water(x, y)],
                                                   weights=[0.8, 0.05, 0,
                                                            0.1, 0, 0.05]
                                                   )[0]

    def init_matrix_from_map(self, map_filepath):
        data = self.load_map(map_filepath)
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

    def render(self, painter):
        for x in range(self.tile_count_x):
            for y in range(self.tile_count_y):
                if self.matrix[x][y] is not None:
                    painter.drawImage(self.matrix[x][y].rect,
                                      self.matrix[x][y].texture)

    def load_map(self, map_filepath):
        with open(map_filepath) as f:
            return json.load(f)

    def save_current_map(self, map_filepath):
        map_file = open("maps/" + map_filepath + ".json", "w")
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
