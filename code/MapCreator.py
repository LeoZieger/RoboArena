from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QTimer, Qt
import Arena
import NameInput

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000


class MapCreator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Arena und all robots that are kept track
        self.arena = Arena.Arena()

        self.current_draw_tile = "Grass"
        self.current_draw_size = 1

        self.initUI()

        # Timer for ticks
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1)

    def initUI(self):
        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.painter = QtGui.QPainter(self.label.pixmap())

        self.show()

    def tick(self):
        self.arena.render(self.painter)
        self.update()

    def mousePressEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:
            tile_pos_x = int(e.x() / self.arena.tile_width)
            tile_pos_y = int(e.y() / self.arena.tile_width)

            offset = (self.current_draw_size - 1)

            if offset == 0:
                self.arena.set_tile(tile_pos_x,
                                    tile_pos_y,
                                    self.current_draw_tile)
            else:
                for i in range(-offset, offset):
                    for j in range(-offset, offset):
                        if ((0 <= (tile_pos_x + i) < self.arena.tile_count_x)
                           and
                           (0 <= (tile_pos_y + j) < self.arena.tile_count_y)):
                            self.arena.set_tile(tile_pos_x + i,
                                                tile_pos_y + j,
                                                self.current_draw_tile)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_1:
            self.current_draw_tile = "Dirt"
        elif e.key() == Qt.Key_2:
            self.current_draw_tile = "Grass"
        elif e.key() == Qt.Key_3:
            self.current_draw_tile = "Lava"
        elif e.key() == Qt.Key_4:
            self.current_draw_tile = "Stone"
        elif e.key() == Qt.Key_5:
            self.current_draw_tile = "Wall"
        elif e.key() == Qt.Key_6:
            self.current_draw_tile = "Water"
        elif e.key() == Qt.Key_Up:
            self.current_draw_size = min(20, self.current_draw_size+1)
        elif e.key() == Qt.Key_Down:
            self.current_draw_size = max(1, self.current_draw_size-1)
        elif e.key() == Qt.Key_S:
            popup = NameInput.NameInput()
            ok = popup.exec_()
            name = popup.textValue()

            while ok and (name == "" or len(name.split(" ")) > 1):
                popup.close()
                ok = popup.exec_()
                name = popup.textValue()
            popup.close()

            self.arena.saveMap(name)
            self.close()
            exit()
