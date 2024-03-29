from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QPen, QFontDatabase, QFont, QColor, QIcon
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QApplication
import Arena
import NameInput
from PathUtil import getPath

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000


class MapCreator(QtWidgets.QMainWindow):
    def __init__(self, selected_map):
        super().__init__()
        self.selected_map = selected_map

        # Set the arena to all grass if there is no map selected
        if self.selected_map == "New Map":
            self.arena = Arena.Arena()
            self.arena.init_matrix_with_texture("Grass")
        # Loading the selected map
        else:
            self.arena = Arena.Arena()
            self.arena.loadMap(selected_map)

        self.current_draw_tile = "Grass"
        self.current_draw_size = 1

        self.sidebar = True

        self.left_mouseButton_pressed = False
        self.mouse_pos = QtCore.QPoint()

        self.initUI()

        # Timer for ticks
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1)

    def initUI(self):
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.centerWindowOnScreen()
        self.setWindowTitle('RoboArena')
        self.setWindowIcon(QIcon(getPath("res", "blue_tank.png")))
        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.painter = QtGui.QPainter()

        self.show()

    def centerWindowOnScreen(self):
        outerRect = self.frameGeometry()
        centerOfScreen = QDesktopWidget().availableGeometry().center()
        outerRect.moveCenter(centerOfScreen)
        self.move(outerRect.topLeft())

    def tick(self):
        # Load font
        id = QFontDatabase.addApplicationFont(getPath("res", "PixeloidMono.ttf"))
        families = QFontDatabase.applicationFontFamilies(id)
        self.font = families[0]

        # Apply font
        QApplication.setFont(QFont(self.font))

        self.painter.begin(self.label.pixmap())
        self.arena.render(self.painter)

        # Create side-menu showing all the keyboard inputs
        if self.sidebar:
            self.painter.setBrush(QColor(77, 77, 77, 200))
            self.painter.drawRect(20, 25, 350, 440)
            self.painter.setPen(QPen(Qt.white, 10, Qt.SolidLine))
            self.painter.setFont(QFont(self.font, 18))
            self.painter.drawText(QPoint(30, 60), "1: Dirt")
            self.painter.drawText(QPoint(30, 90), "2: Grass")
            self.painter.drawText(QPoint(30, 120), "3: Lava")
            self.painter.drawText(QPoint(30, 150), "4: Stone")
            self.painter.drawText(QPoint(30, 180), "5: Wall")
            self.painter.drawText(QPoint(30, 210), "6: Water")
            self.painter.drawText(QPoint(30, 240), "7: Sand")
            self.painter.drawText(QPoint(30, 270), "8: Snow")
            self.painter.drawText(QPoint(30, 300), "9: Lava-Stone")
            self.painter.drawText(QPoint(30, 330), "0: Brick")
            self.painter.drawText(QPoint(30, 360), "↑: Increase Size")
            self.painter.drawText(QPoint(30, 390), "↓: Decrease Size")
            self.painter.drawText(QPoint(30, 420), "S: Save Map")
            self.painter.drawText(QPoint(30, 450), "⌴: Hide Menu")

        self.painter.end()

        self.check_for_paint()

        self.update()

    def mousePressEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:
            self.left_mouseButton_pressed = True
            self.mouse_pos = e.pos()

    def mouseReleaseEvent(self, e):
        self.left_mouseButton_pressed = False

    def mouseMoveEvent(self, e):
        self.mouse_pos = QtCore.QPoint(e.x(), e.y())

    def check_for_paint(self):
        if self.left_mouseButton_pressed:
            self.draw_current_tile()

    # Selecting the tile you want to draw with and setting the draw size
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
        elif e.key() == Qt.Key_7:
            self.current_draw_tile = "Sand"
        elif e.key() == Qt.Key_8:
            self.current_draw_tile = "Snow"
        elif e.key() == Qt.Key_9:
            self.current_draw_tile = "Lava-Stone"
        elif e.key() == Qt.Key_0:
            self.current_draw_tile = "Brick"
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
        elif e.key() == Qt.Key_Space:
            self.sidebar = not self.sidebar

    def draw_current_tile(self):
        tile_pos_x = int(self.mouse_pos.x() / self.arena.tile_width)
        tile_pos_y = int(self.mouse_pos.y() / self.arena.tile_width)

        offset = (self.current_draw_size - 1)

        if offset == 0 and tile_pos_x < 40 and tile_pos_y < 40:
            self.arena.set_tile(tile_pos_x,
                                tile_pos_y,
                                self.current_draw_tile)
        else:
            for i in range(-offset, offset):
                for j in range(-offset, offset):
                    if ((0 <= (tile_pos_x + i) < self.arena.tile_count_x) and
                       (0 <= (tile_pos_y + j) < self.arena.tile_count_y)):
                        self.arena.set_tile(tile_pos_x + i,
                                            tile_pos_y + j,
                                            self.current_draw_tile)
