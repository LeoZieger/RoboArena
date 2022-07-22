from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QGraphicsRectItem
from PathUtil import getPath

TILE_WIDTH = 25
TILE_HEIGHT = 25


class Tile(QGraphicsRectItem):
    texture = QImage(getPath("res", "no_texture.png"))
    tile_type = "None"
    collision = False

    def __init__(self, pos_x, pos_y):
        super().__init__()

        self.x = pos_x
        self.y = pos_y

        self.setRect(self.x * TILE_WIDTH,
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
    texture = QImage(getPath("res", "dirt_texture.png"))


class Grass(Tile):
    tile_type = "Grass"
    texture = QImage(getPath("res", "grass_texture.png"))


class Lava(Tile):
    tile_type = "Lava"
    texture = QImage(getPath("res", "lava_texture.png"))


class Stone(Tile):
    tile_type = "Stone"
    texture = QImage(getPath("res", "stone_texture.png"))


class Wall(Tile):
    tile_type = "Wall"
    texture = QImage(getPath("res", "wall_texture.png"))
    collision = True


class Water(Tile):
    tile_type = "Water"
    texture = QImage(getPath("res", "water_texture.png"))
    collision = True
