import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QTimer, Qt
import Arena

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000


class NameInput(QtWidgets.QInputDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 600, 200)
        self.show()


class MapCreator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Arena und all robots that are kept track
        self.arena = Arena.Arena()

        self.current_draw_tile = "Grass"

        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

        # Painter for all Classes on main Window
        self.painter = QtGui.QPainter(self.label.pixmap())

        # Timer for ticks
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1)

    def tick(self):
        self.arena.render(self.painter)
        self.update()

    def mousePressEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:
            tile_pos_x = int(e.x() / self.arena.tile_width)
            tile_pos_y = int(e.y() / self.arena.tile_width)
            self.arena.set_tile(tile_pos_x, tile_pos_y, self.current_draw_tile)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_1:
            self.current_draw_tile = "Dirt"
        elif e.key() == Qt.Key_2:
            self.current_draw_tile = "Grass"
        elif e.key() == Qt.Key_3:
            self.current_draw_tile = "lava"
        elif e.key() == Qt.Key_4:
            self.current_draw_tile = "Stone"
        elif e.key() == Qt.Key_5:
            self.current_draw_tile = "Wall"
        elif e.key() == Qt.Key_6:
            self.current_draw_tile = "Water"
        elif e.key() == Qt.Key_S:
            popup = NameInput()
            popup.exec_()
            name = popup.textValue()

            self.arena.save_current_map(name)
            self.close()
            exit()


app = QtWidgets.QApplication(sys.argv)
window = MapCreator()
window.show()
app.exec_()
