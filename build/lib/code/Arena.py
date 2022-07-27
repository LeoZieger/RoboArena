import numpy as np
import json
import Tile
from PathUtil import getPath

ARENA_WIDTH = 1000
ARENA_HEIGHT = 1000


class Arena:
    def __init__(self,
                 _arena_width=ARENA_WIDTH,
                 _arena_height=ARENA_HEIGHT,
                 _tile_width=Tile.TILE_WIDTH,
                 _tile_height=Tile.TILE_HEIGHT):

        self.arena_width = _arena_width
        self.arena_height = _arena_height
        self.tile_width = _tile_width
        self.tile_height = _tile_height

        # Number of tiles in x and y direction
        self.tile_count_x = int(self.arena_width / self.tile_width)
        self.tile_count_y = int(self.arena_height / self.tile_height)

        self.matrix = np.empty(shape=(self.tile_count_x,
                               self.tile_count_y),
                               dtype=Tile.Tile)

        self.init_matrix_with_no_texture()

    def init_matrix_with_no_texture(self):
        for x in range(self.tile_count_x):
            for y in range(self.tile_count_y):
                self.matrix[x][y] = Tile.Tile(x, y)

    def init_matrix_with_texture(self, tile_type):
        for x in range(self.tile_count_x):
            for y in range(self.tile_count_y):
                self.set_tile(x, y, tile_type)

    def render(self, painter):
        for x in range(self.tile_count_x):
            for y in range(self.tile_count_y):
                if self.matrix[x][y] is not None:
                    painter.drawImage(self.matrix[x][y].rect(),
                                      self.matrix[x][y].texture)

    def loadMap(self, map_name):
        # loading Map from .json file

        with open(getPath("maps", (map_name + ".json"))) as f:
            data = json.load(f)
            for t in data:
                x = t["x"]
                y = t["y"]
                tile_type = t["type"]
                self.set_tile(x, y, tile_type)

    def saveMap(self, map_name):
        # saving Map to .json file

        map_file = open(getPath("maps", (map_name + ".json")), "w")
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
            self.matrix[x][y] = Tile.Dirt(x, y)
        elif tile_type == "Grass":
            self.matrix[x][y] = Tile.Grass(x, y)
        elif tile_type == "Lava":
            self.matrix[x][y] = Tile.Lava(x, y)
        elif tile_type == "Stone":
            self.matrix[x][y] = Tile.Stone(x, y)
        elif tile_type == "Wall":
            self.matrix[x][y] = Tile.Wall(x, y)
        elif tile_type == "Water":
            self.matrix[x][y] = Tile.Water(x, y)
        elif tile_type == "Sand":
            self.matrix[x][y] = Tile.Sand(x, y)
        elif tile_type == "Snow":
            self.matrix[x][y] = Tile.Snow(x, y)
        elif tile_type == "Lava-Stone":
            self.matrix[x][y] = Tile.LavaStone(x, y)
        elif tile_type == "Brick":
            self.matrix[x][y] = Tile.Brick(x, y)
        else:
            self.matrix[x][y] = Tile.Tile(x, y)

    def add_tiles_to_scene(self, scene):
        # Adding all tiles with collision to the collision scene
        # so they can be detected by other items
        for x in range(self.tile_count_x):
            for y in range(self.tile_count_y):
                if self.matrix[x][y].collision:
                    scene.addItem(self.matrix[x][y])
        return scene

    def listOfNotCollidableTiles(self):
        # Items that for example Powerups can spawn on
        notCollidableTiles = []
        for x in range(self.tile_count_x):
            for y in range(self.tile_count_y):
                if not self.matrix[x][y].collision:
                    notCollidableTiles.append(self.matrix[x][y])

        return notCollidableTiles
